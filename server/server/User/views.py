import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .Utils import BodyData, ModelToJson
from .models import UserModel


def FetchUsers():
    return list(UserModel.objects.values())


class Users(View):

    # get all the Users
    def get(self, request, *args, **kwargs):
        users = FetchUsers()
        if len(users):
            return JsonResponse({'users_data': users}, status=200)
        else:
            return HttpResponse('Zero Users', status=204)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        content = BodyData(request)

        if content is None:
            return HttpResponse('You can\'t create user without name and description', status=204)

        "Validate what is required and what is not"
        fname = content['fname']
        lname = content['lname']
        birth_date = content['birth_date']
        email = content['email']
        password = content['password']

        c = UserModel(first_name=fname, last_name=lname, birth_date=birth_date, email=email, password=password)
        c.save()

        return JsonResponse({"User": model_to_dict(c)})


class User(View):

    def get(self, request, *args, **kwargs):

        fetcheduser = UserModel.objects.filter(id=kwargs['user_id']).values()

        if not fetcheduser:
            return HttpResponse('User is Not found', status=404)
        else:
            return JsonResponse(data=fetcheduser[0])

    @csrf_exempt
    def put(self, request, *args, **kwargs):

        fetcheduser = UserModel.objects.filter(id=kwargs['user_id'])[0]
        content = BodyData(request)

        if not fetcheduser:
            return HttpResponse('User is Not found', status=404)
        elif content is None:
            return HttpResponse('You can\'t Update user without its info', status=204)
        else:

            fname = content['fname']
            lname = content['lname']
            birth_date = content['birth_date']
            email = content['email']
            password = content['password']

            fetcheduser.first_name = fname
            fetcheduser.last_name = lname
            fetcheduser.birth_date = birth_date
            fetcheduser.email = email
            fetcheduser.password = password

            fetcheduser.save()
            return JsonResponse({"user": model_to_dict(fetcheduser)})

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        fetchedUser = UserModel.objects.filter(id=kwargs['user_id'])[0]

        if not fetchedUser:
            return HttpResponse('User is Not found', status=404)
        else:
            fetchedUser.delete()
            return HttpResponse('User {} deleted'.format(kwargs['user_id']), status=200)
