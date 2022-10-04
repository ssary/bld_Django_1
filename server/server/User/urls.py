from django.urls import path
from .views import Users, User

urlpatterns=[
    path('', Users.as_view()),
    path('<int:user_id>/',User.as_view()),
]

