from django.db import models


class Hero(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.TextField()
    action_text = models.CharField(max_length=200, default="RSVP on Meetup")
    action_url = models.URLField()
    source_id = models.CharField(max_length=250)

    def __unicode__(self):
        return self.title
