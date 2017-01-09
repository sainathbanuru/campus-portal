from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput
from django.contrib.auth.forms import *


class formRequest(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    fathersName = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'fathersName'}))
    formRequired = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'formRequired'}))
    reason = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'reason'}))