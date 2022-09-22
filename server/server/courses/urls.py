from django.urls import path
from .views import AllCourses, FetchCourse

urlpatterns=[
    path('', AllCourses.as_view()),
    path('<int:course_id>/', FetchCourse.as_view()),
]

