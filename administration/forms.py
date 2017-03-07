from django.forms import CheckboxInput, CharField, BooleanField, TextInput, Textarea, FileField,SelectMultiple,IntegerField,FileInput,ChoiceField,NumberInput,Select
from django.contrib.auth.forms import *
from .choices import *

class courses(forms.Form):
    course_title = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'course_title'}))
    #course_faculty = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'course_faculty'}))
    course_faculty = ChoiceField(choices=faculty_list,widget=Select(attrs={'class':'form-control','id':'course_faculty'}))
    course_type = ChoiceField(choices=STATUS_CHOICES,widget=Select(attrs={'class':'form-control','id':'course_type'}))
    course_credits = IntegerField(max_value=16,widget=NumberInput(attrs={'class' : 'form-control','id':'course_credits'}))
    coursefor_ug1 = BooleanField(widget=CheckboxInput(attrs={'class':'checkbox-inline','id':'ug1'}),required=False,)
    coursefor_ug2 = BooleanField(widget=CheckboxInput(attrs={'class':'checkbox-inline','id':'ug2'}),required=False)
    coursefor_ug3 = BooleanField(widget=CheckboxInput(attrs={'class':'checkbox-inline','id':'ug3'}),required=False)
    coursefor_ug4 = BooleanField(widget=CheckboxInput(attrs={'class':'checkbox-inline','id':'ug4'}),required=False)
    course_sem = ChoiceField(choices=sem_choices,widget=Select(attrs={'class':'form-control','id':'course_sem'}))


class Notice(forms.Form):
    notice_title = CharField(widget=TextInput(attrs={'class':'form-control','id':'notice_title'}))
    notice_decsription = CharField(widget=Textarea(attrs={'class':'form-control','id':'notice_decsription'}))


class add_almanac(forms.Form):
    almanac = FileField()

