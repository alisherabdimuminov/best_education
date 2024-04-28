from django.urls import path

from .views import (
    courses,
    course,
    create_course,
    update_course,
    subjects,
    add_module,
    modules,
    module_lessons,
    create_question,
    quiz_questions,
    module,
    lesson,
    end_lesson,
)


urlpatterns = [
    path("", courses, name="courses"),
    path("course/<int:pk>/", course, name="course"),
    path("create/", create_course, name="create_course"),
    path("course/<int:course_id>/update/", update_course, name="update_course"),
    path("course/<int:pk>/add/module/", add_module, name="add_module"),
    path("course/<int:pk>/modules/", modules, name="modules"),
    path("course/<int:course_id>/modules/module/<int:module_id>/", module, name="module"),
    path("course/<int:course_id>/modules/module/<int:module_id>/lesson/<int:lesson_id>/", lesson, name="lesson"),
    path("course/<int:course_id>/modules/module/<int:module_id>/lesson/<int:lesson_id>/end/", end_lesson, name="end_lesson"),
    path("modules/module/<int:pk>/lessons/", module_lessons, name="module_lessons"),
    path("subjects/", subjects, name="subjects"),
    path("create_question/", create_question, name="create_question"),
    path("quiz/<int:pk>/questions/", quiz_questions, name="quiz_questions"),
]
