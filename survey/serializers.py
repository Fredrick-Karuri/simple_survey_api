from rest_framework import serializers
from .models import *
from .models import Survey, Question, Response, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'



class QuestionResponseSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email_address = serializers.EmailField()
    gender = serializers.CharField()
    programming_stack = serializers.ListField(child=serializers.CharField())
    certificates = serializers.ListField(child=serializers.FileField())
    date_responded = serializers.DateTimeField()

    
    # description = serializers.CharField()

