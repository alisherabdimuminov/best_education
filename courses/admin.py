from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Course,
    Module,
    Lesson,
    Subject,
    Question,
    Quiz,
    Answer,
)


@admin.register(Course)
class CourseModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(Module)
class ModuleModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(Lesson)
class LessonModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(Subject)
class SubjectModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(Question)
class QuestionModelAdmin(ModelAdmin):
    list_display = ["question"]

@admin.register(Quiz)
class QuizModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(Answer)
class AnswerModelAdmin(ModelAdmin):
    list_display = ["value_1", "value_2", "is_correct"]
