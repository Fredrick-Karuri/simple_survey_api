from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Survey, Question, Response, Choice, User
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer, ChoiceSerializer, QuestionResponseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, HttpResponse
from django.utils import timezone
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


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionResponseView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user__email']

    def get(self, request, format=None):
        queryset = Response.objects.all()
        filtered_queryset = DjangoFilterBackend().filter_queryset(request, queryset, self)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = ResponseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ResponseSerializer(queryset, many=True)
        return Response(serializer.data)


    def put(self, request, format=None):
        # get the request data
        data = request.data

        # get the use from the request data
        user_email = data.get('user_email')
        # user, _ = User.objects.get_or_create(email=user_email)

        # iterate over the questions in the request data
        for question_name, response_text in data.items():
            if question_name == 'user_email':
                continue
            try:
                # get the question from the database
                question = Question.objects.get(name=question_name)

                # if the question is a choice question, get the choice from the database
                if question.question_type == Question.CHOICE:
                    # if the question allows multiple choices, response_text will be a list
                    if question.multiple_choices:
                        choices = Choice.objects.filter(
                            question=question, text__in=response_text)
                        for choice in choices:
                            _, _ = Response.objects.update_or_create(
                                question=question, defaults={'choice': choice})
                    else:
                        # otherwise handle a single choice
                        choice = Choice.objects.get(
                            question=question, text=response_text)
                        _, _ = Response.objects.update_or_create(
                            question=question, defaults={'choice': choice})
                elif question.question_type == Question.FILE:
                    # if the question is a file upload question, get the files from the request
                    if question_name in request.FILES:
                        files = request.FILES.getlist(question_name)
                        for file in files:
                            _, _ = Response.objects.update_or_create(
                                question=question, defaults={'file': file})

                else:
                    # otherwise create or update a text response
                    _, _ = Response.objects.update_or_create(
                        question=question, defaults={'text': response_text})
            except Question.DoesNotExist:
                raise ValidationError(
                    f"Question '{question_name}' does not exist.")
            except Choice.DoesNotExist:
                raise ValidationError(
                    f"Choice '{response_text}' does not exist for question '{question_name}'.")

        return APIResponse({"detail": "Responses created or updated successfully."}, status=status.HTTP_201_CREATED)

    print([q.name for q in Question.objects.all()])


def download_response_file(request, id):
    # Fetch the response based on the provided id
    response = Response.objects.get(id=id)

    # Check if the response has a file associated with it
    if response.file:
        # Open the file in binary mode
        file = open(response.file.path, 'rb')

        # Create a response with the file's content and the correct MIME type
        response = FileResponse(file)

        # Set the Content-Disposition header to prompt the browser to download the file
        response['Content-Disposition'] = f'attachment; filename="{response.file.name}"'

        return response
    else:
        return HttpResponse('No file associated with this response', status=404)


def create_response(request):
    # Get the user
    user_email = request.data.get('email')
    user, created = User.objects.get_or_create(email=user_email)

    # Get the responses
    responses_data = request.data.get('responses')

    # Iterate over the responses data
    for response_data in responses_data:
        # Get the question id and response text
        question_id = response_data.get('question_id')
        response_text = response_data.get('response_text')

        # Get the question
        question = Question.objects.get(id=question_id)

        # Create the response
        response = Response.objects.create(
            user=user, question=question, text=response_text)

    return APIResponse({"detail": "Responses created successfully."}, status=status.HTTP_201_CREATED)


def submit_survey(request):
    # Get the survey
    survey_id = request.data.get('survey_id')
    survey = Survey.objects.get(id=survey_id)

    # Handle the survey submission...

    # When all questions have been answered, update the submitted_at field
    survey.submitted_at = timezone.now()
    survey.save()

    return APIResponse({"detail": "Survey submitted successfully."}, status=status.HTTP_201_CREATED)


# class QuestionResponseView(APIView):
#     def put(self, request, format=None):
#         serializer = QuestionResponseSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             responses = []
#             for question in Question.objects.all():
#                 response = self.create_response(question, data)
#                 if response is not None:
#                     responses.append(response)
#             serializer = ResponseSerializer(responses, many=True)
#             return APIResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return APIResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def create_response(self, question, data):
#         if question.text in data:
#             response = APIResponse(question=question)
#             if question.question_type == Question.CHOICE:
#                 choice_text = data[question.text]
#                 choice = Choice.objects.get(
#                     question=question, text=choice_text)
#                 response.choice = choice
#             else:
#                 response.text = data[question.text]
#             response.save()
#             return response
#         return None
