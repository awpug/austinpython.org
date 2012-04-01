from django.db import models
import urllib


class Hero(models.Model):
    title = models.CharField(max_length=200,
            help_text=u"Shows up at the top")
    summary = models.TextField(
            help_text=u"Shows up along side the events ")
    pub_date = models.DateTimeField(
            help_text=u"The date this should show up on the site")
    action_text = models.CharField(max_length=200, default="RSVP on Meetup",
            help_text=u"Text of the action button")
    action_url = models.URLField(
            help_text=u"URL to send people to when they want to sign up")
    location = models.CharField(max_length=200,
            help_text=u"Where is the meeting going to be?")
    datetime = models.DateTimeField(
            help_text=u"When does the event happen?")

    @property
    def location_map_url(self):
        """ Return the Google Map link. """
        location_encoded = urllib.quote(self.location)
        location_map_url = "http://map.google.com/?q=%s" % location_encoded
        return location_map_url

    def __unicode__(self):
        return self.title
