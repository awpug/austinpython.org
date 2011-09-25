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

@profile
class Twitter(Profile):

    @classmethod
    def populate_from_request(cls, request):
        """
        Grab results from a successful OAuth callback.
        """
        pass

@profile
class GitHub(Profile):

    @classmethod
    def populate_from_request(cls, request):
        """
        Grab results from a successful OAuth callback.
        """
        name = request.POST.get("name")
        username = request.POST.get("login")
        email = request.POST.get("email")
        github_profile = cls(name=name, email=email, username=username)
        return github_profile

    @classmethod
    def populate_from_user_profile(cls, user_profile):
        """
        Generate a new profile from the API call result.
        """
        name = user_profile["user"]["name"]
        username = user_profile["user"]["login"]
        email = user_profile["user"]["email"]
        github_profile = cls(name=name, email=email, username=username)
        return github_profile

