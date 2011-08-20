"""
This is just a basic up / down vote poll like Dell IdeaStorm or
UserVoice.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Poll(models.Model):
    """ The basic poll object """
    subject = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(editable=False)
    expires = models.DateTimeField("date expires", null=True, 
                                   blank=True, default=None)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    author = models.ForeignKey(User)

    @property
    def votes(self):
        """ Retrieve a list of votes for this poll """
        return Vote.objects.filter(poll=self)

    @property
    def tally(self):
        """ Return the sum of the votes """
        return self.up_votes - self.down_votes

    @property
    def total_votes(self):
        """ Return the total number of votes """
        return self.up_votes + self.down_votes

    @property
    def users(self):
        """ Retrieve a list of users for this poll """
        return self.votes.values("user")

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(Poll, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Delete all votes and the poll """
        Vote.objects.filter(poll=self).delete()
        super(Poll, self).delete(*args, **kwargs)

    def remove_vote(self, vote):
        """ Updates up_votes, etc. to reflect removed vote """
        # BAH! Atomic decrements, plz!
        if vote.value == 1:
            self.up_votes -= 1
        else:
            self.down_votes -= 1
        self.save()

    def add_vote(self, vote):
        """ Updates up_votes, etc. to reflect new vote """
        # Bah, these need to be atomic updates, by golly!
        if vote.value == 1:
            self.up_votes += 1
        else:
            self.down_votes += 1
        self.save()

    def __unicode__(self):
        return self.subject

class Vote(models.Model):
    """ An entry for each actual vote -- could get a bit noisy """
    user = models.ForeignKey(User, null=True, blank=True) # null = anonymous
    poll = models.ForeignKey(Poll)
    date = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(editable=False)
    value = models.IntegerField(choices=((1, "Yes"), (0, "No")))

    def save(self, *args, **kwargs):
        """ Update vote on poll, then save changes """
        self.updated = datetime.now()
        if self.id:
            # Exists, removing prior vote tally
            vote = Vote.objects.get(id=self.id)
            self.poll.remove_vote(vote)
        super(Vote, self).save(*args, **kwargs)
        self.poll.add_vote(self)

    def delete(self, *args, **kwargs):
        """ Remove vote from poll, then delete """
        self.poll.remove_vote(self)
        super(Vote, self).delete(*args, **kwargs)

    def __unicode__(self):
        vote_type = "Yes"
        if self.value == 0:
            vote_type = "No"
        return u"%s - %s" % (self.poll.subject, vote_type)
