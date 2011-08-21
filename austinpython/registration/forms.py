from django import forms
from django.contrib.auth.models import User

from austinpython.registration.models import AustinPython


class RegistrationForm(forms.ModelForm):
    """ Used for creating an AustinPython profile / user. """

    class Meta:
        model = AustinPython
        fields = ('email', 'name', "password", "confirm_password")

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """ Check the password matches after basic validation """
        try:
            cleaned_data = super(RegistrationForm, self).clean()
        except AttributeError:
            # not sure if this is a "good" catch?
            raise forms.ValidationError("One or more fields were invalid.")
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u'Sorry, your passwords did not match.')
        return cleaned_data

    def save(self, force_insert=False, force_update=False, commit=True):
        """ Create a new user and new default profile. """
        new_profile = super(RegistrationForm, self).save(commit=False)
        if not new_profile.id:
            new_user = User.create_from_profile(new_profile)
            new_user.set_password(self.data.get("password"))
            new_user.save()

            new_profile.user = new_user
            new_profile.is_default = True

        if commit:
            new_profile.save()
        return new_profile
