from django.db import models


class Hero(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.TextField()
    default_action_text = models.CharField(max_length=200, default="RSVP")

    def __unicode__(self):
        return self.title


class HeroAction(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_default = models.BooleanField()
    hero = models.ForeignKey(Hero, related_name="actions")

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.url)
