from django.db import models
import re
from rest_framework.exceptions import ValidationError
# A Survey has a name and a description.

class User(models.Model):
    email = models.EmailField(unique=True )

    def __str__(self):
        return self.name

class Survey (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

# A Question is associated with a Survey (a survey can have multiple questions). Each question has some text.


class Question (models.Model):
    TEXT = 'TX'
    LONGTEXT = 'LT'
    CHOICE = 'CH'
    EMAIL = 'EM'
    FILE = 'FL'
    QUESTION_TYPES = [
        (TEXT, 'Short Text'),
        (LONGTEXT, 'Long Text'),
        (CHOICE, 'Choice'),
        (EMAIL, 'Email'),
        (FILE, 'File Upload')
    ]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    name=models.CharField(max_length=50, default='name')
    required = models.BooleanField(default=False)
    question_type = models.CharField(
        max_length=2, choices=QUESTION_TYPES, default=TEXT,)
    text = models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    multiple_choices = models.BooleanField(default=False)
    file_format = models.CharField(max_length=200, null=True, blank=True)
    max_file_size = models.IntegerField(null=True, blank=True)
    multiple_files = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# The Choice model is associated with a Question and represents the different options for a multiple choice question. Each Choice has some text that represents the option.


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    value =models.CharField(max_length=200, default='value')
    # multiple_choices = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# A File model is associated with a Question and represents a file uploaded by a user.


class File(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.FileField


# A Response is associated with a Question (a question can have multiple responses). Each response has some text.


class Response (models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True)

    text = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='uploads/',  null=True, blank=True)
    date_responded =models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.text:
            return self.text
        elif self.choice:
            return str(self.choice)
        elif self.file:
            return self.file.name
        else:
            return "No response"

    def clean(self):
        if self.question.question_type == Question.CHOICE and self.choice is None:
            raise ValidationError('Please select a choice')
        
        if self.question.question_type == Question.FILE:
            if not self.file:
                raise ValidationError('Please upload a file')
            if self.text or self.choice:
                raise ValidationError('Text and choice fields must be empty for file type questions')
            if self.file.size > self.question.max_file_size:
                raise ValidationError('File size exceeds maximum allowed size')
            if not self.file.name.endswith(self.question.file_format):
                raise ValidationError('File format must be ' + self.question.file_format)
            
        if self.question.question_type == Question.EMAIL and self.text is None:
            raise ValidationError('Please enter an email address')
        if self.question.question_type in [Question.TEXT, Question.LONGTEXT] and self.text is None:
            raise ValidationError('Please enter a text response')
        if self.question.question_type == Question.TEXT and self.text is not None:
            if len(self.text) > 200:
                raise ValidationError(
                    'Text response cannot exceed 200 characters')
        if self.question.question_type == Question.LONGTEXT and self.text is not None:
            if len(self.text) > 1000:  # Assuming a max length of 1000 for long text
                raise ValidationError(
                    'Long text response cannot exceed 1000 characters')
        if self.question.question_type == Question.EMAIL and self.text is not None:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.text):
                raise ValidationError('Please enter a valid email address')

    # def clean(self):
    #     if self.question.question_type == Question.CHOICE:
    #         if not self.choice:
    #             raise ValidationError(
    #                 'Choice field must be selected for choice type question')
    #         if self.text:
    #             raise ValidationError(
    #                 'Text field must be empty for choice type question')
    #     else:
    #         if not self.text:
    #             raise ValidationError(
    #                 'Text field must be filled for non-choice type question')
    #         if self.choice:
    #             raise ValidationError(
    #                 'Choice field must be empty for non-choice type question')

        # if self.question.question_type == Question.FILE and self.text is not None:
            # raise ValidationError('Please upload a file')