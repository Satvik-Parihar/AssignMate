from django.urls import path
from .views import task_assignment_view

urlpatterns = [
    path('', task_assignment_view, name='upload_audio'),
]