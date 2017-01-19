from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput,SelectMultiple,Select,IntegerField
from django.contrib.auth.forms import *


class formRequest(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    fathersName = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'fathersName'}))
    formRequired = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'formRequired'}))
    reason = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'reason'}))
    def clean(self):
        name = self.cleaned_data.get('name')
        return self.cleaned_data

class registerForm(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    roll_no = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'roll_name'}))
    phone_no = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'phone_no'}))
    parent_phone = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'parent_phone'}))
    address = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'address'}))
