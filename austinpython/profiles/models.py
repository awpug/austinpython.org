from django.db import models
from django.core import exceptions
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
import json
import hashlib

class DictField(models.TextField):
    """ Serializes JSON on save and load. """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """ Returns the dictionary saved. """
        if value is None:
            return None
        if type(value) is dict:
            # still a dictionary, hasn't been encoded
            return value
        try:
            return json.loads(value)
        except ValueError:
            raise exceptions.ValidationError("Invalid JSON in JSONField.")

    def get_db_prep_save(self, value, connection):
        """ Translate to JSON """
        if value is not None:
            assert(type(value) is dict)
            value = json.dumps(value)
        return super(DictField, self).get_db_prep_save(value=value,
                connection=connection)


class Profile(models.Model):
    """
    The (abstract) base for all profile data. Subclass this
    to create internal / external profile information,
    such as Twitter or Facebook data.
    """
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=200) # user's full name
    email = models.EmailField(max_length=200, blank=True)
    username = models.CharField(max_length=128, blank=True)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    added_date = models.DateTimeField(default=datetime.now, editable=False)
    data = DictField() # for platform-specific data.

    class Meta:
        ordering = ["-is_default", "-added_date"]
        unique_together = ('user', 'type')

    def __init__(self, *args, **kwargs):
        """ Sets type automatically """
        kwargs.setdefault("type", slugify(self.__class__.__name__))
        kwargs.setdefault("data", self.get_default_data())
        super(Profile, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.type+"|"+self.name

    def get_default_data(self):
        """ Returns a default dictionary of data. Overwrite in subclasses. """
        return {}

    def get_image(self, **kwargs):
        """ Retrieves a Gravatar by default -- should be overwritten
        on each subclass profile. May not be the best place for this...?
        """
        base = "//www.gravatar.com/avatar/"
        email_hash = hashlib.md5(self.email.strip().lower()).hexdigest()
        if "size" in kwargs:
            email_hash += "?s=%d" % kwargs["size"]
        return base + email_hash

    @classmethod
    def populate_from_request(self, request):
        raise NotImplementedError("Classes that subclass Profile need "
            "to implement this method")


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

def profile(cls):
    """
    This decorator identifies a model as a Profile class,
    suitable for searching, etc.

    Example usage:

    @profile # short name will be 'github'
    class GitHub(Profile):
        repos = models.ForeignKey(GitRepository)
        #... extra stuff ...

    """
    if not issubclass(cls, Profile):
        raise ValueError("A profile must be subclassed from Profile.")
    cls_short_name = slugify(cls.__name__)

    if not hasattr(cls, "Meta"):
        class Meta:
            proxy = True
        cls.Meta = Meta
    Profiles.instance().add_profile(cls_short_name, cls.__name__, cls)
    return cls


def get_user_profiles(self, **kwargs):
    """ Retrieve a user's external profile """
    kwargs.setdefault("user", self)
    return Profile.objects.filter(**kwargs)

def get_user_profile(user, **kwargs):
    """ Returns the first matching profile for the user """
    kwargs["user"] = user
    return Profile.objects.get(**kwargs)

def user_profile_shortcut(self):
    """ The profile 'attribute' on a User model """
    return get_user_profile(self)

def create_user_from_profile(self, profile):
    """ Sets up a basic user from the provided profile. """
    kwargs = {"email": profile.email, "username": profile.email}
    name_parts = profile.name.split(" ")
    if name_parts:
        kwargs["first_name"] = name_parts[0]
    if len(name_parts) > 1:
        kwargs["last_name"] = " ".join(name_parts[1:])
    user = User(**kwargs)
    return user


# monkey patching the user profiles
User.get_user_profiles = get_user_profiles
User.profile = property(user_profile_shortcut)
User.create_from_profile = classmethod(create_user_from_profile)
