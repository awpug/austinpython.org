from django.test import TestCase, Client
from django.db import IntegrityError
from django.utils.unittest import skipUnless
from django.contrib.auth.models import User
from django.forms import ValidationError
from austinpython.tests import Mock
from austinpython.registration.forms import RegistrationForm
from austinpython.registration.models import AustinPython
from austinpython.registration.models import GitHub
from austinpython.registration import twitter
from austinpython.registration import github
from austinpython import settings
import urlparse
import httplib2
import oauth2

class TestRegistrationForm(TestCase):

    def test_registration_form(self):
        """ Test that a registration form validates properly. """
        data = {"name": "TESTING", "email": "test@foo.com",
                "password": "foobar", "confirm_password": "foobar"}
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(data, form.clean())
        profile = form.save()
        self.assertEqual(profile.email, profile.user.username)
        self.assertTrue(profile.user.check_password(data["password"]))
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        self.assertRaises(IntegrityError, form.save)

    def test_invalid_registration_form(self):
        """ Test that invalid registration data raises Validation errors. """
        form = RegistrationForm({})
        self.assertRaises(ValidationError, form.clean)
        form = RegistrationForm({"name": "TESTING", "email": "test@foo.com",
            "password": "foobar", "confirm_password": "foobaz"})
        self.assertRaises(ValidationError, form.clean)


class TestAustinPythonProfile(TestCase):

    def test_new_austin_python_profile(self):
        """ Test that a new profile is saved with proper information. """
        user = User(username="test@foo.com", password="password")
        user.save()

        profile = AustinPython(user=user, name="Testing", email="test@foo.com")
        profile.save()

        self.assertEqual(user.profile.id, profile.id)
        self.assertEqual(profile.data, {})

        profile = AustinPython(user=user, name="duplicate",
                               email="test@foo.com")
        self.assertRaises(IntegrityError, profile.save)

    def test_new_austin_python_profile_from_request(self):
        """ Test a new profile from a mock request object. """
        request = Mock(POST={"name": "testing"})
        profile = AustinPython.populate_from_request(request)
        self.assertEqual(profile.name, "testing")


class TestGitHubProfile(TestCase):

    def test_new_github_profile_from_request(self):
        """ Test that a new profile is saved with info from a request. """
        request = Mock(POST={"name": "testing", "email": "foo@bar.com",
            "login": "foobar"})
        profile = GitHub.populate_from_request(request)
        self.assertEqual(profile.name, "testing")
        self.assertEqual(profile.username, "foobar")

    def test_new_github_profile_from_api_request(self):
        """ Test that a new profile is saved with info from the API. """
        profile = GitHub.populate_from_user_profile({
            "user" : {
                "name": "testing",
                "email": "foo@bar.com",
                "login": "foobar"
            }
        })
        self.assertEqual(profile.name, "testing")
        self.assertEqual(profile.username, "foobar")


class TestRegistrationController(TestCase):

    def test_get_new_user_profile(self):
        """ Test that a GET for the registration works. """
        client = Client()
        response = client.get("/register/austinpython")
        self.assertEqual(response.status_code, 200)

    def test_post_new_user_profile(self):
        """ Test a POST to the registration controller. """
        client = Client()
        response = client.post("/register/austinpython/submit",
            {"name": "Test Name", "email": "test@foo.com",
                "password": "testing",
                "confirm_password": "testing"})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get()
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Name")
        self.assertEqual(user.email, "test@foo.com")
        self.assertTrue(user.check_password("testing"))

    def test_post_failed_new_user_profile(self):
        """ Test that an invalid POST fails. """
        client = Client()
        data = {"name": "Test Name", "email": "test@foo.com",
                "password": "testing", "confirm_password": "fail"}
        self.assertRaises(ValueError, client.post,
            "/register/austinpython/submit", data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(AustinPython.objects.count(), 0)


""" TWITTER """

class TestTwitterRegistrationRequest(TestCase):

    def setUp(self):
        """ Overwrite settings for the tests. """
        self.original_key = settings.TWITTER_CONSUMER_KEY
        self.original_secret = settings.TWITTER_CONSUMER_SECRET
        self.original_callback = settings.TWITTER_CALLBACK_URL
        settings.TWITTER_CONSUMER_KEY = "foobar"
        settings.TWITTER_CONSUMER_SECRET = "foobarfoobar"
        settings.TWITTER_CALLBACK_URL = "http://localhost/foobar"

    def test_get_twitter_redirect_url(self):
        """ Test that we get a properly signed redirect URL. """
        # overwriting settings
        request_token = oauth2.Token(key="foobar", secret="foobarfoobar")
        request_token.set_callback(settings.TWITTER_CALLBACK_URL)
        redirect_url = twitter.get_twitter_redirect_url(request_token)

        parts = urlparse.urlparse(redirect_url)
        args = urlparse.parse_qs(parts.query)

        test_args = {"oauth_token": [request_token.key,],
                     "oauth_callback": ["http://localhost/foobar",]}
        test_path = "/oauth/authorize"

        self.assertEqual(args, test_args)
        self.assertEqual(parts.path, test_path)

    def test_get_twitter_consumer(self):
        """ Test the returned URL for a request token """
        consumer = twitter.get_twitter_consumer()
        self.assertEqual(consumer.key, "foobar")
        self.assertEqual(consumer.secret, "foobarfoobar")

    def tearDown(self):
        """ Restore original settings. """
        settings.TWITTER_CONSUMER_KEY = self.original_key
        settings.TWITTER_CONSUMER_SECRET = self.original_secret
        settings.TWITTER_CALLBACK_URL = self.original_callback

class TestTwitterActualCalls(TestCase):
    """ If the settings allow it, test calls to the Twitter API. """

    @skipUnless(settings.TWITTER_TEST_REQUEST_TOKEN,
        "Twitter request token test not enabled.")
    def test_get_request_token(self):
        """ Test that we get a valid request token. """
        token = twitter.get_twitter_request_token()
        self.assertEqual(token.get_callback_url(),
                settings.TWITTER_CALLBACK_URL)

        redirect_url = twitter.get_twitter_redirect_url()
        args = urlparse.parse_qs(urlparse.urlparse(redirect_url).query)
        self.assertEqual(token.callback, args["oauth_callback"][0])
        response, content = httplib2.Http().request(redirect_url)
        self.assertEqual(response.status, 200)

    @skipUnless(settings.TWITTER_TEST_REQUEST_TOKEN,
        "Twitter request token test not enabled -- skipping error test.")
    def test_get_invalid_request_token(self):
        """ Test that invalid credentials fails to get token """
        consumer = twitter.get_twitter_consumer("NO", "NO")
        self.assertRaises(Exception, twitter.get_twitter_request_token,
            consumer)

    @skipUnless(settings.TWITTER_TEST_REQUEST_TOKEN,
        "Twitter request token not enabled -- skipping redirect test.")
    def test_get_twitter_registration_redirect(self):
        """ Test that the /register/twitter page redirects to Twitter """
        client = Client()
        response = client.get("/register/twitter")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.has_header("Location"))
        location = response.get("Location", "")
        self.assertTrue(location.startswith(
            "https://twitter.com/oauth/authorize"))


class TestGithubActualCalls(TestCase):
    """ If the settings allow it, test calls to the GitHub API. """

    @skipUnless(settings.GITHUB_TEST_REDIRECT_URL,
        "GitHub request url test not enabled.")
    def test_get_github_redirect_url(self):
        """ Test that we get a valid GitHub request token. """
        redirect_url = github.get_github_redirect_url()
        args = urlparse.parse_qs(urlparse.urlparse(redirect_url).query)
        self.assertEqual(settings.GITHUB_CALLBACK_URL,
            args["redirect_uri"][0])
        # GitHub SSL is failing... should fix this danger eventually
        response, content = httplib2.Http(
            disable_ssl_certificate_validation=True
        ).request(redirect_url)
        self.assertEqual(response.status, 200)

    @skipUnless(settings.GITHUB_TEST_REDIRECT_URL,
        "Github request url test not enabled.")
    def test_get_github_registration_redirect(self):
        """ Test that the /register/github page redirects to Github """
        client = Client()
        response = client.get("/register/github")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.has_header("Location"))
        location = response.get("Location", "")
        self.assertTrue(location.startswith(
            "https://github.com/login/oauth/authorize"
        ))

    @skipUnless(settings.GITHUB_TEST_REDIRECT_URL,
        "Github request url test not enabled")
    def test_get_github_access_token_with_invalid_code(self):
        """ Test that the get_github_access_token fails with invalid code """
        self.assertRaises(Exception, github.get_github_access_token,
            code="FOOBAR")

    @skipUnless(settings.GITHUB_TEST_REDIRECT_URL,
        "Github request url test not enabled")
    def test_get_github_user_profile_with_invalid_token(self):
        """ Test that the get_github_user_profile fails with invalid token """
        self.assertRaises(Exception, github.get_github_user_profile,
            token="FOOBAR")

class TestGitHubRegistrationWorkflow(TestCase):

    def test_get_github_registration_callback(self):
        """ Test that the /register/github/callback page processes tokens """
        CODE = "FOOBAR"
        # Monkey patching the token request function
        original_token_func = github.get_github_access_token
        original_user_func = github.get_github_user_profile
        github.get_github_access_token = lambda code: "BAZ"
        github.get_github_user_profile = lambda token: {
            "user": {
                "name": "Foo bar",
                "email": "foo@bar.com",
                "login": "foobar"
            }
        }
        try:
            client = Client()
            response = client.get("/register/github/callback?code="+CODE)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.has_header("Location"))
            profile = GitHub.objects.get(username="foobar")
            user = profile.user
            self.assertEqual(profile.name, "Foo bar")
            self.assertEqual(user.email, "foo@bar.com")
            self.assertEqual(response["vary"], "Cookie")
        finally:
            github.get_github_access_token = original_token_func
            github.get_github_user_profile = original_user_func

