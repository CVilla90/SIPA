# Portfolio/SIPA/courses/forms.py

from django import forms
from .models import Course, Competency, CourseCompetency
from django.forms import inlineformset_factory

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'hours', 'credits', 'semester', 'major']

CourseCompetencyFormSet = inlineformset_factory(
    Course, CourseCompetency, fields=('competency', 'occurrence'), extra=1, can_delete=True
)

class CompetencyForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['name', 'description', 'category']

class CourseCompetencyForm(forms.ModelForm):
    class Meta:
        model = CourseCompetency
        fields = ['competency', 'occurrence']
