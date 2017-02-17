from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput,ChoiceField,Select,IntegerField,EmailField
from django.contrib.auth.forms import *
from portal.choices import *

class RequestForm(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    fathersName = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'fathersName'}))
    formRequired = ChoiceField(choices=forms_type,widget=Select(attrs={'class':'form-control','id':'formRequired'}))
    reason = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'reason'}))

class RegisterForm(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    roll_no = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'roll_name'}))
    phone_no = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'phone_no'}))
    parent_phone = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'parent_phone'}))
    address = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'address'}))


class SignupForm(forms.Form):
    name = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'name'}))
    fname = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'fname'}))
    roll = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'roll'}))
    email = EmailField(widget=TextInput(attrs={'class' : 'form-control','id':'email'}))
    password = CharField(widget=PasswordInput(attrs={'class' : 'form-control','id':'pass'}))
    cpassword = CharField(widget=PasswordInput(attrs={'class' : 'form-control','id':'cpass'}))
    phone = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'phone'}))
    branch = ChoiceField(choices=branch,widget=Select(attrs={'class':'form-control','id':'branch'}))
    year = ChoiceField(choices = year,widget=Select(attrs={'class' : 'form-control','id':'year'}))

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords must be identical.")

        return cleaned_data



