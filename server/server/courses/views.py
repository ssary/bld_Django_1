import json
import os
import uuid

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django import forms
from .forms import CourseForm, CustomCourseForm

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

        name = content['name']
        description = content['description']

        courseValidator = CourseForm({"name": name, "description": description})
        courseCustomValidator = CustomCourseForm({"name": name, "description": description})

        print(courseCustomValidator.is_valid())
        if courseValidator.is_valid():
            course_id = str(uuid.uuid4())
            courses.append({"id": course_id, "name": name, "description": description})

            DictCourses = write_courses_db(courses)
            return JsonResponse(DictCourses)


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

        name = content['name']
        description = content['description']
        courseCustomValidator = CustomCourseForm({"name": name, "description": description})

        fetchedCourse = None
        for course in courses:
            if str(course['id']) == str(kwargs['course_id']):
                if 'name' not in courseCustomValidator.errors.as_data():
                    course['name'] = name
                if 'description' not in courseCustomValidator.errors.as_data():
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
