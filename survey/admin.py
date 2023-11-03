from django.contrib import admin
from .models import Survey, Question, Response, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Survey)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Response)
