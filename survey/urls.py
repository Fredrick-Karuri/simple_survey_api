from django.urls import path
from . import views
from .views import QuestionResponseView, ResponseDetail, ResponseList

urlpatterns = [
    path('api/questions', views.QuestionList.as_view()),
    path('api/questions/responses', QuestionResponseView.as_view()),
    path('api/questions/responses/update/<int:pk>', ResponseDetail.as_view()),
    path('api/questions/responses/create/', ResponseList.as_view()),
    path('api/questions/responses/<int:pk>', views.ResponseDetail.as_view()),
    path('api/questions/responses/uploads/<int:id>', views.download_response_file),

]
