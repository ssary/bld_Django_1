from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json,os,uuid

dbPath = os.path.join(os.getcwd(), 'courses/db.json')
file = open(dbPath)
courses = json.load(file)
file.close()
courses = courses['courses']

class AllCourses(TemplateView):
    def get(self, request, *args, **kwargs):
        if len(courses):
            return JsonResponse({'courses': courses})
        else:
            return HttpResponse('Zero courses', status=204)

    @csrf_exempt
    def post (self, request, *args, **kwargs):
        content = None
        if request.body:
            content = json.loads(request.body.decode('utf-8'))

        if content is None:
            return HttpResponse('You can\'t create course without name and description', status=400)

        name = content['name']
        description = content['description']
        course_id = str(uuid.uuid4())
        courses.append({"id":course_id, "name": name, "description": description})

        DictCourses = {"courses": courses}
        with open(dbPath, "w") as outfile:
            json.dump(DictCourses, outfile)
        return JsonResponse(DictCourses)


class FetchCourse(TemplateView):

    def get(self, request, *args, **kwargs):
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
    def put (self, request, *args, **kwargs):

        name = request.GET.get('name')
        description = request.GET.get('description')

        fetchedCourse = None
        for course in courses:
            if str(course['id']) == str(kwargs['course_id']):
                if name is not None:
                    course['name'] = name
                if description is not None:
                    course['description'] = description
                fetchedCourse = course
                break

        if fetchedCourse is None:
            return HttpResponse('Course is Not found', status=404)
        else:
            DictCourses = {"courses": courses}
            with open(dbPath, "w") as outfile:
                json.dump(DictCourses, outfile)
            return JsonResponse(fetchedCourse)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        UpdatedCourses = []
        isFound = False
        for course in courses:
            if str(course['id']) != str(kwargs['course_id']):
                UpdatedCourses.append(course)
            else:
                isFound=True

        if not isFound:
            return HttpResponse('Course is Not found', status=404)
        else:
            DictCourses = {"courses": UpdatedCourses}
            with open(dbPath, "w") as outfile:
                json.dump(DictCourses, outfile)
            return JsonResponse(DictCourses)
