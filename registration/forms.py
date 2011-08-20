from django import forms
from django.contrib.auth.models import User

from austin_python_profiles.models import AustinPythonProfile


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = AustinPythonProfile
        fields = ('email', 'name',)

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u'Sorry, your passwords did not match.')
        return cleaned_data

    def save(self, force_insert=False, force_update=False, commit=True):
        austin_python_profile = super(RegistrationForm, self).save(commit=False)
        if not austin_python_profile.id:
            cleaned_data = austin_python_profile.cleaned_data
            new_user = User()
            new_user.username = cleaned_data.get('email')
            new_user.password = new_user.set_password(cleaned_data.get('password'))
            new_user.save()

            austin_python_profile.user = new_user
            austin_python_profile.is_default = True

        if commit:
            austin_python_profile.save()
        return austin_python_profile
