""" Basic registration POST controller(s). """

from django.shortcuts import render_to_response, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.generic import RedirectView
from austinpython.registration.forms import RegistrationForm
from austinpython.registration import twitter
from austinpython.registration import github
from austinpython.registration.models import GitHub

def register_austinpython_get(request):
    """ Handle GET requests for registration. """
    form = RegistrationForm()
    return render_to_response("registration/austinpython.html",
        {"form": form }, context_instance=RequestContext(request))

def register_austinpython_post(request):
    """ Handle PUT requests for registration. """
    form = RegistrationForm(request.POST)
    profile = form.save()
    url = "/profiles/%s" % profile.user.id
    return redirect(url)

class TwitterRegistrationLink(RedirectView):
    """ Redirect to Twitter to authorize user """

    permanent = False

    def get_redirect_url(self, **kwargs):
        """ Generate the twitter redirect url """
        return twitter.get_twitter_redirect_url()


class GitHubRegistrationLink(RedirectView):
    """ Redirect to GitHub to authorize user """

    permanent = False

    def get_redirect_url(self, **kwargs):
        """ Generate the github redirect url """
        return github.get_github_redirect_url()

class GitHubRegistrationCallback(RedirectView):
    """ Create a profile and redirect to login on successful callback """

    permanent = False

    def get_redirect_url(self, **kwargs):
        """ Generate the github profile and redirect to login """
        if "code" not in self.request.GET:
            raise Exception("Invalid GitHub callback: %s", self.request.GET)
        token = github.get_github_access_token(
            code=self.request.GET["code"])

        user_profile = github.get_github_user_profile(token=token)
        username = user_profile["user"]["login"]
        github_results = GitHub.objects.filter(username=username)
        if not github_results:
            # Assuming this is a new user
            profile = GitHub.populate_from_user_profile(user_profile)
            user = User.create_from_profile(profile)
            user.save()
            profile.user = user
            profile.save()
        else:
            profile = github_results[0]
            user = profile.user
        # MAN, this is a dirty, dirty hack. Seriously Django?
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(self.request, user)
        return "/login"

