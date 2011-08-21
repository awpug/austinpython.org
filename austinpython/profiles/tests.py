from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from austinpython.profiles.models import Profiles, Profile, profile

@profile
class Testing(Profile):

    @classmethod
    def populate_from_request(cls, request):
        instance = cls(name=request.POST.get("name"))
        return instance

    def get_default_data(self):
        return {"foo": "bar"}

class TestProfiles(TestCase):

    def test_decorator(self):
        """ Tests that a new profile is in the Profiles singleton. """
        profiles = Profiles.instance()
        self.assertTrue("testing" in profiles._profiles)
        self.assertEqual(("Testing", Testing),
            profiles._profiles["testing"])
        # testing double-adding a profile
        self.assertRaises(KeyError, profile, Testing)

    def test_new_profile(self):
        """ Test creating a new profile. """
        user = User(first_name="Testing", last_name="Testing",
            username="test@foo.com", password="testing")
        user.save()
        start = datetime.datetime.now()
        new_profile = Testing(name="Testing", email="test@foo.com",
            is_default=True, user=user)
        new_profile.save()
        self.assertTrue(start <= new_profile.added_date)
        self.assertEqual(new_profile.user, user)
        self.assertEqual(user.profile.id, new_profile.id)
        self.assertEqual(user.profile.data, {"foo": "bar"})

    def test_new_user(self):
        """ Test creating a new user from a profile. """
        profile = Testing(name="Testing Roger", email="test@foo.com",
            is_default=True)
        user = User.create_from_profile(profile)
        user.set_password("foobar")
        user.save()
        profile.user = user
        profile.save()
        self.assertEqual(user.email, "test@foo.com")
        self.assertEqual(user.first_name, "Testing")
        self.assertEqual(user.last_name, "Roger")
        self.assertEqual(user.profile.id, profile.id)

