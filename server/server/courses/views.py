import json
import os
import uuid

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django import forms
from .forms import NameForm,DescriptionForm, CustomNameForm, CustomDescriptionForm

dbPath = os.path.join(os.getcwd(), 'courses/db.json')


def ReadCoursesDB():
    file = open(dbPath)
    courses = json.load(file)
    file.close()
    return courses['courses']


def write_courses_db(courses):
    DictCourses = {"courses": courses}
    with open(dbPath, "w") as outfile:
        json.dump(DictCourses, outfile)
    return DictCourses


def BodyData(request):
    content = None
    if request.body:
        content = json.loads(request.body.decode('utf-8'))
    return content


class Courses(TemplateView, forms.Form):

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
        name = ''
        description = ''
        if 'name' in content:
            name = content['name']
        if 'description' in content:
            description = content['description']

        name_validator = NameForm({"name": name})
        description_validator = CustomDescriptionForm({"description": description})

        if name_validator.is_valid() and description_validator.is_valid():
            course_id = str(uuid.uuid4())
            courses.append({"id": course_id, "name": name, "description": description})

            DictCourses = write_courses_db(courses)
            return JsonResponse(DictCourses)
        elif name_validator.is_valid():
            return HttpResponse(description_validator.errors, status=206)
        else:
            return HttpResponse(name_validator.errors, status=206)

class Course(TemplateView):

    def get(self, request, *args, **kwargs):
        courses = ReadCoursesDB()
        fetchedCourse = None
        for course in courses:
            if str(course['id']) == str(kwargs['course_id']):
                fetchedCourse = course
                break

        if fetchedCourse is None:
            return HttpResponse('Course is Not found', status=404)
        else:
            return JsonResponse(data=fetchedCourse)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        courses = ReadCoursesDB()
        content = BodyData(request)

        if content is None:
            return HttpResponse('You can\'t Update course without name and description', status=204)

        name = ''
        description = ''
        if 'name' in content:
            name = content['name']
        if 'description' in content:
            description = content['description']

        name_validator = CustomNameForm({"name": name})
        description_validator = DescriptionForm({"description": description})
        fetchedCourse = None
        for course in courses:
            if str(course['id']) == str(kwargs['course_id']):
                if name_validator.is_valid():
                    course['name'] = name
                if description_validator.is_valid():
                    course['description'] = description
                fetchedCourse = course
                break

        if fetchedCourse is None:
            return HttpResponse('Course is Not found', status=404)
        else:
            write_courses_db(courses)
            return JsonResponse(fetchedCourse)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        courses = ReadCoursesDB()
        UpdatedCourses = []
        isFound = False
        for course in courses:
            if str(course['id']) != str(kwargs['course_id']):
                UpdatedCourses.append(course)
            else:
                isFound = True

        if not isFound:
            return HttpResponse('Course is Not found', status=404)
        else:
            DictCourses = write_courses_db(UpdatedCourses)
            return JsonResponse(DictCourses)
