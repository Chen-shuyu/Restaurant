from django import forms

from allenapp.models import Dreamreal


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        dbuser = Dreamreal.objects.filter(name = username)

        if not dbuser:
            return 'db does not have %s' %username
        else:
            username

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    picture = forms.ImageField()

class PostForm(forms.Form):
    boardname = forms.CharField(max_length = 20, initial = '')
    boardsubject = forms.CharField(max_length = 100, initial = '')
    boardmessage = forms.CharField(widget = forms.Textarea)
