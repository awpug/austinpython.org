"""
The test cases for the Poll model, the Vote model, and all their
mischievous behavior.
"""

from django.test import TestCase
from polls.models import Poll, Vote
from django.contrib.auth.models import User

class BaseUserCase(object):
    """ Useful methods for testing user-related models """

    _users = []
    _user_numbers = range(0, 1000)

    def new_user(self, **kwargs):
        """ Creates a random user, saves it for deletion later """
        num = self._user_numbers.pop()
        kwargs.setdefault("first_name", "FIRST%04d" % num)
        kwargs.setdefault("last_name", "LAST%04d" % num)
        kwargs.setdefault("username", "user%04d" % num)
        user = User(**kwargs)
        user.save()
        self._users.append(user)
        return user


class BasePollCase(BaseUserCase):
    """ Several useful methods for testing polls """

    _polls = []
    _votes = []
    _poll_numbers = range(0, 1000)
    _vote_numbers = range(0, 1000)

    def new_poll(self, **kwargs):
        """ Generate a new poll """
        number = self._poll_numbers.pop()
        kwargs.setdefault("subject", "Poll Subject %s" % number)
        kwargs.setdefault("description", "Poll Description %s" % number)
        if "author" not in kwargs:
            kwargs["author"] = self.new_user()
        poll = Poll(**kwargs)
        poll.save()
        self._polls.append(poll)
        return poll

    def new_vote(self, poll, value=1, **kwargs):
        """ Generate a new vote """
        kwargs["poll"] = poll
        if not "user" in kwargs:
            kwargs["user"] = self.new_user()
        kwargs["value"] = value
        vote = Vote(**kwargs)
        vote.save()
        self._votes.append(vote)
        return vote


class TestVoting(BasePollCase, TestCase):
    """ Test a poll, and vote creation / updating """

    def test_base_poll(self):
        poll = self.new_poll()
        self.assertEqual(poll.tally, 0)
        self.assertEqual(poll.up_votes, 0)
        self.assertEqual(poll.down_votes, 0)
        self.assertEqual(poll.total_votes, 0)

    def test_single_vote(self):
        poll = self.new_poll()
        self.new_vote(value=1, poll=poll)
        self.assertEqual(poll.tally, 1)
        self.assertEqual(poll.total_votes, 1)
        self.assertEqual(poll.up_votes, 1)
        self.assertEqual(poll.down_votes, 0)

    def test_vote_change(self):
        poll = self.new_poll()
        vote = self.new_vote(value=1, poll=poll)
        vote.value = 0
        vote.save()
        self.assertEqual(poll.tally, -1)
        self.assertEqual(poll.total_votes, 1)
        self.assertEqual(poll.down_votes, 1)
        self.assertEqual(poll.up_votes, 0)

    def test_multiple_votes(self):
        poll = self.new_poll()
        for i in range(10):
            # ten up votes
            self.new_vote(poll, value=1)
        for i in range(5):
            self.new_vote(poll, value=0)
        self.assertEqual(poll.tally, 5)
        self.assertEqual(poll.total_votes, 15)
        self.assertEqual(poll.up_votes, 10)
        self.assertEqual(poll.down_votes, 5)

    def test_multiple_votes_changing(self):
        poll = self.new_poll()
        for i in range(10):
            vote = self.new_vote(poll, value=1)
            if i % 2:
                vote.value = 0
                vote.save()
                if i % 3:
                    vote.value = 1
                    vote.save()
        self.assertEqual(poll.tally, 6)
        self.assertEqual(poll.total_votes, 10)
        self.assertEqual(poll.down_votes, 2)
        self.assertEqual(poll.up_votes, 8)

