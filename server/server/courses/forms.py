from django import forms
from django.core.exceptions import ValidationError


def validate_name(value):
    if 'django' in value:
        return value
    else:
        raise ValidationError("the course name must contain django")


def validate_description(value):
    if len(value) >= 10:
        return value
    else:
        raise ValidationError("the description must be >= 10 chars")


class CourseForm(forms.Form):
    name = forms.CharField(min_length=3)
    description = forms.CharField(min_length=10)

class CustomCourseForm(forms.Form):
    name = forms.CharField(validators=[validate_name])
    description = forms.CharField(validators=[validate_description])