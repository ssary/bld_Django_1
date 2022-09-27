from django.urls import path
from .views import Courses, Course

urlpatterns=[
    path('', Courses.as_view()),
    path('<int:course_id>/', Course.as_view()),
    path('', Courses.as_view()),
    path('<int:course_id>/', Course.as_view()),

]

