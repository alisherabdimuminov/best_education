from django.contrib import admin

from .models import (
    Course,
    Module,
    Lesson,
    Subject,
    Question,
    Quiz,
)


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Module)
class ModuleModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["question"]

@admin.register(Quiz)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
