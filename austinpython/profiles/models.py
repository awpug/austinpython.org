from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime

class Profile(models.Model):
    """
    The (abstract) base for all profile data. Subclass this
    to create internal / external profile information,
    such as Twitter or Facebook data.
    """

    type = models.CharField(max_length=40, default="halfway")
    name = models.CharField(max_length=200) # user's full name
    email = models.EmailField(max_length=200)
    url = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    added_date = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        ordering = ["-default", "-added_date"]
        abstract = True

    def __unicode__(self):
        return self.name

    @classmethod
    def populate_from_request(self, request):
        raise NotImplementedError('Classes that subclass Profile need to implement this method')


class Profiles(object):
    """ The singleton for all profile models. """

    _instance = None

    def __init__(self):
        self._profiles = {}

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def get_user_profile_by_name(self, user, key):
        """
        Retrieve a profile instance for a user for the given
        profile 'key' name (i.e. "github", etc.) if it exists.
        """
        profile_name, profile_class = self._profiles[key]
        return self.get_user_profile(user, profile_class)

    def get_user_profile(self, user, profile_class):
        """ Retrieve a profile instance for a user (if it exists) """
        try:
            result = profile_class.objects.get(user=user, is_default=True)
        except profile_class.DoesNotExist:
            result = None
        return result

    def add_profile(self, key, name, profile_class):
        """ Add a profile to the profiles dictionary """
        if key in self._profiles:
            raise KeyError("Profile short name %s already exists" % key)
        self._profiles[key] = (name, profile_class)

def profile(name=None, short_name=None):
    """
    This decorator identifies a model as a Profile class,
    suitable for searching, etc.

    Example usage:

    @profile("GitHub") # short name will be 'github'
    class GitHub(Profile):
        repos = models.ForeignKey(GitRepository)
        #... extra stuff ...

    """
    def wrapper(cls):
        if not issubclass(cls, Profile):
            raise ValueError("A profile must be subclassed from Profile.")
        # hate using 'global'...
        cls_name = name
        cls_short_name = short_name
        if not cls_name:
            cls_name = cls.__name__
        if not cls_short_name:
            cls_short_name = slugify(cls_name)
        cls.type.default = short_name
        if not hasattr(cls, "Meta"):
            class Meta:
                proxy = True
            cls.Meta = Meta
        Profiles.instance().add_profile(cls_short_name, cls_name, cls)
        return cls
    if issubclass(name, Profile):
        # decorator with no arguments / ()
        klass = name
        name = None
        return wrapper(klass)
    return wrapper


def get_user_profiles(self, **kwargs):
    """ Retrieve a user's external profile """
    kwargs.setdefault(user=self)
    return Profile.objects.filter(**kwargs)

def user_profile_shortcut(self):
    """ The profile 'attribute' on a User model -- returns first profile. """
    results = self.get_user_profiles()
    if results:
        return results[0]
    return None

# If the User already has a .profile attribute, we don't
# want to monkey patch it.

if hasattr(User, "profile") or hasattr(User, "get_user_profiles"):
    raise Exception("Cannot use halfway profiles -- User model already has "
                    "profile attributes.")
User.get_user_profiles = get_user_profiles
User.profile = property(user_profile_shortcut)
