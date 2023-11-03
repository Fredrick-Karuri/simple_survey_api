from django.urls import path
from . import views

urlpatterns = [
    path('api/questions', views.QuestionList.as_view()),
    path('api/questions/responses', views.ResponseList.as_view()),
    path('api/questions/responses/<int:pk>', views.ResponseDetail.as_view())
]
