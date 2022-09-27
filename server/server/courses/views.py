import json
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Courses as CoursesModel
from django.core import serializers
dbPath = os.path.join(os.getcwd(), 'courses/db.json')


def ReadCoursesDB():
    return list(CoursesModel.objects.values())


def BodyData(request):
    content = None
    if request.body:
        content = json.loads(request.body.decode('utf-8'))
    return content


def ModelToJson(model):
    return json.loads(serializers.serialize('json', [model, ]))[0]['fields']


class Courses(TemplateView):

    def get(self, request, *args, **kwargs):
        courses = ReadCoursesDB()
        if len(courses):
            return JsonResponse({'courses': courses})
        else:
            return HttpResponse('Zero courses', status=204)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        courses = ReadCoursesDB()
        content = BodyData(request)

        if content is None:
            return HttpResponse('You can\'t create course without name and description', status=204)

        name = content['name']
        description = content['description']
        c = CoursesModel(name=name, description=description)
        c.save()

        return JsonResponse(ModelToJson(c))


class Course(TemplateView):

    def get(self, request, *args, **kwargs):

        fetchedCourse = CoursesModel.objects.filter(id=kwargs['course_id']).values()

        if not fetchedCourse:
            return HttpResponse('Course is Not found', status=404)
        else:
            return JsonResponse(data=fetchedCourse[0])

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
            return JsonResponse(ModelToJson(fetchedCourse))

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        fetchedCourse = CoursesModel.objects.filter(id=kwargs['course_id'])[0]

        if not fetchedCourse:
            return HttpResponse('Course is Not found', status=404)
        else:
            fetchedCourse.delete()
            return HttpResponse('Course {} deleted'.format(kwargs['course_id']), status=404)
