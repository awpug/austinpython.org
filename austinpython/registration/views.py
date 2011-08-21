""" Basic registration POST controller(s). """

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from austinpython.registration.forms import RegistrationForm

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
