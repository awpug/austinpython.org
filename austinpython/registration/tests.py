from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.forms import ValidationError
from austinpython.tests import Mock
from austinpython.registration.forms import RegistrationForm
from austinpython.registration.models import AustinPython

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

