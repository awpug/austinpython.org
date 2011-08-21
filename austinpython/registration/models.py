""" The "generic" profile for a new Austin Python member. """

from austinpython.profiles.models import Profile, profile

@profile
class AustinPython(Profile):

    @classmethod
    def populate_from_request(cls, request):
        """
        Need to populate the profile properties with values from
        the request that comes back from the oAuth provider
        """
        name = request.POST.get('name')
        austin_python_profile = cls(name=name)
        return austin_python_profile
