from django.test import TestCase, Client
from django.utils.unittest import skipUnless
from django.contrib.auth.models import User
from django.forms import ValidationError
from austinpython.tests import Mock
from austinpython.registration.forms import RegistrationForm
from austinpython.registration.models import AustinPython
from austinpython.registration import twitter
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

    def test_new_austin_python_profile_from_request(self):
        """ Test a new profile from a mock request object. """
        request = Mock(POST={"name": "testing"})
        profile = AustinPython.populate_from_request(request)
        self.assertEqual(profile.name, "testing")

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
        "Twitter request token test not requested.")
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
