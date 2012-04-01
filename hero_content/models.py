from django.db import models
import urllib


class Hero(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    pub_date = models.DateTimeField()
    action_text = models.CharField(max_length=200, default="RSVP on Meetup")
    action_url = models.URLField()
    location = models.CharField(max_length=200)
    datetime = models.DateTimeField()

    @property
    def location_map_url(self):
        """ Return the Google Map link. """
        location_encoded = urllib.quote(self.location)
        location_map_url = "http://map.google.com/?q=%s" % location_encoded
        return location_map_url

    def __unicode__(self):
        return self.title
