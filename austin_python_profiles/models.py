from django.db import models

from profiles.models import Profile, profile

@profile('AustinPython')
class AustinPythonProfile(Profile):

    @classmethod
    def populate_from_request(cls, request):
        """
        Need to populate the profile properties with values from
        the request that comes back from the oAuth provider
        """
        name = request.POST.get('name')
        austin_python_profile, created = cls.get_or_create(name=name,
                                                           defaults={'name' : name})
        return austin_python_profile
