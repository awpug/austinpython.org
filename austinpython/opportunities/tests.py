"""
Tests for the Opportunities postings app.
"""

from django.test import TestCase
from austinpython.opportunities.models import Opportunity
from django.contrib.auth.models import User
import re

class TestOpportunites(TestCase):

    def setUp(self):
        self.user = User(first_name="Foo", last_name="Bar",
            username="foo@bar.com")
        self.user.save()

    def create_opportunity(self, **kwargs):
        """ Create a new opportunity and return it """
        kwargs.setdefault("user", self.user)
        kwargs.setdefault("text", "This is an awesome new opportunity "
            "for anyone who likes opportunities with the opportunity of "
            "success")
        opp = Opportunity(**kwargs)
        opp.save()
        return opp

    def test_opportunity_model(self):
        """ Test that we can create a new Opportunity. """
        opp = self.create_opportunity()
        # just making sure uid got set automatically
        self.assertTrue(len(opp.uid) == 10)
        self.assertEqual(opp.user, self.user)

    def test_opportunity_slug(self):
        """ Test that an Opportunity has a slug """
        uid = "abcde12345"
        opp = self.create_opportunity(uid="abcde12345")
        self.assertTrue(re.match(r"%s\/[a-z0-9\-]{36}$" % uid, opp.slug))
