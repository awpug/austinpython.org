from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

import hashlib

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    summary = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User)

    @property
    def author_avatar_url(self):
        """
        Returns the gravatar URL.
        Should be on the user model, but I'm being lazy.
        """
        hashed_email = hashlib.md5(self.author.email).hexdigest()
        url = "http://www.gravatar.com/avatar/%s" % hashed_email
        return url

    @property
    def date_string(self):
        print self.pub_date
        return "%s" % self.pub_date.date

    @property
    def time_string(self):
        return "%s" % self.pub_date.time

    def __unicode__(self):
        return self.title

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
