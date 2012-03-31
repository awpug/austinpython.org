from django.db import models


class Hero(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    pub_date = models.DateTimeField()
    action_text = models.CharField(max_length=200, default="RSVP on Meetup")
    action_url = models.URLField()

    def __unicode__(self):
        return self.title
