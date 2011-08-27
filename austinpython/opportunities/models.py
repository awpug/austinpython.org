from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid

def generate_uid(length=10):
    """ Generate a hex UID """
    uid = uuid.uuid4().hex[0:length]
    return uid

class Opportunity(models.Model):
    """ Information about an Opportunity (Job Posting, etc.) """

    text = models.TextField()
    uid = models.CharField(default=generate_uid, max_length=10)
    user = models.ForeignKey(User)

    @property
    def slug(self):
        """ Generates the URL "slug" -- not predefined due changing titles  """
        slug = slugify(self.text)
        return "%s/%s" % (self.uid, slug[:36]) # max 24 characters

