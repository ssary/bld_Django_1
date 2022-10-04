import json


from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django import forms
from .forms import NameForm,DescriptionForm, CustomNameForm, CustomDescriptionForm

from .Utils import BodyData, ModelToJson
from .models import Courses as CoursesModel


def FetchCourses():
    return list(CoursesModel.objects.values())


class Courses(TemplateView, forms.Form):

    def get(self, request, *args, **kwargs):
        courses = FetchCourses()
        if len(courses):
            return JsonResponse({'courses': courses}, status=200)
        else:
            return HttpResponse('Zero courses', status=204)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        content = BodyData(request)

        if content is None:
            return HttpResponse('You can\'t create course without name and description', status=204)


        name = content['name']
        description = content['description']
        c = CoursesModel(name=name, description=description)
        c.save()

        return JsonResponse(ModelToJson(c), status=201)
        

class Course(TemplateView):

    def get(self, request, *args, **kwargs):

        fetchedCourse = CoursesModel.objects.filter(id=kwargs['course_id']).values()

        if not fetchedCourse:
            return HttpResponse('Course is Not found', status=404)
        else:
            return JsonResponse(data=fetchedCourse[0], status=200)

    @csrf_exempt
    def put(self, request, *args, **kwargs):


        fetchedCourse = CoursesModel.objects.filter(id=kwargs['course_id'])[0]
        content = BodyData(request)

        if not fetchedCourse:
            return HttpResponse('Course is Not found', status=404)
        elif content is None:
            return HttpResponse('You can\'t Update course without name and description', status=204)
        else:
            name = content['name']
            description = content['description']

            fetchedCourse.name = name
            fetchedCourse.description = description
            fetchedCourse.save()
            return JsonResponse(ModelToJson(fetchedCourse),status=201)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        fetchedCourse = CoursesModel.objects.filter(id=kwargs['course_id'])[0]

        if not fetchedCourse:
            return HttpResponse('Course is Not found', status=404)
        else:
            fetchedCourse.delete()
            return HttpResponse('Course {} deleted'.format(kwargs['course_id']), status=200)
