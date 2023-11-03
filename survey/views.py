from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Survey, Question, Response, Choice
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer, ChoiceSerializer

# defining views for my api endpoints


class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ResponseList(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    # calling the clean method

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            instance.clean()
        except ValidationError as e:
            instance.delete()
            raise ValidationError(e)

    # calling the clean method


class ResponseDetail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        try:
            instance.clean()
        except ValidationError as e:
            instance.delete()
            raise ValidationError(e)
