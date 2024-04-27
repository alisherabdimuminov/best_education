import random
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import (
    Course,
    Question,
    Quiz,
    Lesson,
    Module,
    Check,
    Subject,
    Answer
)
from users.models import User
from config.settings import BASE_DIR

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def courses(request: HttpRequest):
    courses = Course.objects.all()
    c = []
    for course in courses:
        aimage = course.author.image
        if aimage:
            aimage = request.build_absolute_uri(aimage.url)
        else:
            aimage = None
        image = course.image
        if image:
            image = request.build_absolute_uri(image.url)
        else:
            image = None
        c.append({
            "id": course.pk,
            "name": course.name,
            "subject": course.subject.name,
            "image": image,
            "teacher": {
                "phone": course.author.username,
                "first_name": course.author.first_name,
                "last_name": course.author.last_name,
                "description": course.author.description,
                "image": aimage
            },
            "description": course.description,
            "feedback": course.feedback,
            "students": course.students.count(),
            "price": course.price,
            "count_modules": course.count_modules(),
            "count_lessons": course.count_lessons(),
            "count_quizzes": course.count_quizzes(),
            "created_at": course.created_at,
        })
    return Response({
        "status": "success",
        "message": "",
        "courses": c
    })

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def course(request: HttpRequest, pk):
    course = None
    try:
        course = Course.objects.get(pk=pk)
    except Exception as e:
        print("courses:views:course", e)
        return Response({
            "status": "error",
            "message": "course not found"
        })
    modules = []
    module_counter = 1
    for module in course.modules().all():
        lessons = []
        lesson_counter = 1
        for lesson in module.lessons():
            lessons.append({
                "id": lesson.pk,
                "counter": lesson_counter,
                "name": lesson.name,
                "duration": lesson.duration
            })
            lesson_counter += 1
        required = module.required
        if required:
            required = required.name
        else:
            required = None
        modules.append({
            "module": {
                "id": module.pk,
                "counter": module_counter,
                "name": module.name,
                "course": module.course.name,
                "required": required,
                "lessons": lessons
            }
        })
        module_counter += 1
    aimage = course.author.image
    if aimage:
        aimage = request.build_absolute_uri(aimage.url)
    else:
        aimage = None
    image = course.image
    if image:
        image = request.build_absolute_uri(image.url)
    else:
        image = None
    return Response({
        "id": course.pk,
        "name": course.name,
        "subject": course.subject.name,
        "image": image,
        "teacher": {
            "first_name": course.author.first_name,
            "last_name": course.author.last_name,
            "description": course.author.description,
            "image": aimage
        },
        "description": course.description,
        "feedback": course.feedback,
        "price": course.price,
        "count_lessons": course.count_lessons(),
        "count_quizzes": course.count_quizzes(),
        "lessons": modules,
        "created_at": course.created_at,
    })

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_course(request: HttpRequest):
    name = request.data.get("name")
    author = request.user
    image = request.FILES.get("image")
    subject = request.data.get("subject")
    description = request.data.get("description")
    price = request.data.get("price")
    # print(image.read())
    course = Course.objects.create(
        name=name,
        author=User.objects.get(pk=1),
        image=image,
        subject=Subject.objects.get(pk=int(subject)),
        description=description,
        price=int(price),
    )
    return Response()

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def update_course(request: HttpRequest, course_id):
    name = request.data.get("name")
    image = request.FILES.get("image")
    subject = request.data.get("subject")
    description = request.data.get("description")
    price = request.data.get("price")
    # print(image.read())
    course = None
    try:
        course = Course.objects.get(pk=course_id)
        course.name = name
        course.description = description
        course.image = image
        course.price = price
        course.save()
        modules = []
        module_counter = 1
        for module in course.modules().all():
            lessons = []
            lesson_counter = 1
            for lesson in module.lessons():
                lessons.append({
                    "id": lesson.pk,
                    "counter": lesson_counter,
                    "name": lesson.name,
                    "duration": lesson.duration
                })
                lesson_counter += 1
            required = module.required
            if required:
                required = required.name
            else:
                required = None
            modules.append({
                "module": {
                    "id": module.pk,
                    "counter": module_counter,
                    "name": module.name,
                    "course": module.course.name,
                    "required": required,
                    "lessons": lessons
                }
            })
            module_counter += 1
        aimage = course.author.image
        if aimage:
            aimage = aimage.url
        else:
            aimage = None
        image = course.image
        if image:
            image = image.url
        else:
            image = None
        return Response({
            "id": course.pk,
            "name": course.name,
            "subject": course.subject.name,
            "image": image,
            "author": {
                "first_name": course.author.first_name,
                "last_name": course.author.last_name,
                "description": course.author.description
            },
            "description": course.description,
            "feedback": course.feedback,
            "price": course.price,
            "count_lessons": course.count_lessons(),
            "count_quizzes": course.count_quizzes(),
            "lessons": modules,
            "created_at": course.created_at,
        })
    except Exception as e:
        print("courses:views:update_course", e)
    return Response()

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def add_module(request: HttpRequest, pk):
    try:
        name = request.data.get("name")
        course = Course.objects.get(pk=pk)
        required = None
        try:
            required = Module.objects.get(pk=request.data.get("module"))
        except Exception as e:
            print(e)
        passing_score = request.data.get("passing_score")
        Module.objects.create(
            name=name,
            course=course,
            required=required,
            passing_score=passing_score
        )
        return Response({
            "status": "success",
            "message": ""
        })
    except Exception as e:
        print("courses:views:add_module", e)
        return Response({
            "status": "error",
            "message": "Course is not defined"
        })
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def edit_module(request: HttpRequest, pk):
    try:
        name = request.data.get("name")
        course = Course.objects.get(pk=pk)
        required = None
        try:
            required = Module.objects.get(pk=request.data.get("module"))
        except Exception as e:
            print(e)
        passing_score = request.data.get("passing_score")
        Module.objects.create(
            name=name,
            course=course,
            required=required,
            passing_score=passing_score
        )
        return Response({
            "status": "success",
            "message": ""
        })
    except Exception as e:
        print("courses:views:edit_module", e)
        return Response({
            "status": "error",
            "message": "Course is not defined"
        })
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def modules(request: HttpRequest, pk):
    try:
        course = Course.objects.get(pk=pk)
        modules = Module.objects.filter(course=course)
        m = []
        for module in modules:
            m.append({
                "id": module.pk,
                "name": module.name
            })
        return Response({
            "status": "success",
            "message": "",
            "modules": m
        })
    except Exception as e:
        print("courses:views:modules", e)
        return Response({
            "status": "error",
            "message": "course is not found"
        })

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def add_lesson(request: HttpRequest, pk):
    try:
        module = Module.objects.get(pk=pk)
        name = request.data.get("name")
        video = request.data.get("video")
        duration = request.data.get("duration")
        resource = request.FILES.get("resource")
        score = request.data.get("score")
        previous = request.data.get("previous")
        next = request.data.get("next")
        type = request.data.get("type")
        
    except Exception as e:
        print("courses:views:add_lesson")
        return Response({
            "status": "error",
            "message": ""
        })
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_question(request: HttpRequest):
    quiz = request.data.get("quiz")
    data = request.data.get("data")
    name = request.data.get("name")
    question = data.get("question")
    print(quiz)
    try:
        quiz = Quiz.objects.get(pk=quiz)
    except Exception as e:
        print("courses:views:create_question")
        quiz = Quiz.objects.create(name=name)
    type = data.get("type")
    if type == None:
        return Response({
            "status": "error",
            "message": "question type is required"
        })
    elif type == "writeable":
        writeable = data.get("writeable")
        if writeable == None:
            return Response({
                "status": "error",
                "message": "writeable is required",
                "quiz": quiz.pk
            })
        answer = Answer.objects.create(
            value_1=writeable,
            is_correct=True
        )
        q = Question.objects.create(
            question=question,
            type=type
        )
        q.answers.add(answer)
        q.save()
        quiz.questions.add(q)
        quiz.save()
    elif type == "one_select":
        one_select = data.get("one_select")
        print(one_select)
        if one_select == None:
            return Response({
                "status": "error",
                "message": "one_select is required",
                "quiz": quiz.pk
            })
        q = Question.objects.create(question=question, type=type)
        correct_answer_found = False
        for ans in one_select:
            if correct_answer_found:
                answer = Answer.objects.create(
                    value_1=ans.get("value"),
                    is_correct=False
                )
                q.answers.add(answer)
                q.save()
            else:
                answer = Answer.objects.create(
                    value_1=ans.get("value"),
                    is_correct=ans.get("is_correct")
                )
                q.answers.add(answer)
                q.save()
            if ans.get("is_correct"):
                correct_answer_found = True
            quiz.questions.add(q)
            quiz.save()
    elif type == "many_select":
        many_select = data.get("many_select")
        if many_select == None:
            return Response({
                "status": "error",
                "message": "many_select is required"
            })
        print(many_select)
        q = Question.objects.create(question=question, type=type)
        for ans in many_select:
            answer = Answer.objects.create(
                value_1=ans.get("value"),
                is_correct=ans.get("is_correct")
            )
            q.answers.add(answer)
            q.save()
        quiz.questions.add(q)
        quiz.save()
    elif type == "matchable":
        matchable = data.get("matchable")
        print(matchable)
        if matchable == None:
            return Response({
                "status": "error",
                "message": "matchable is required"
            })
        q = Question.objects.create(question=question, type=type)
        for ans in matchable:
            answer = Answer.objects.create(value_1=ans.get("value_1"), value_2=ans.get("value_2"), is_correct=True)
            q.answers.add(answer)
            q.save()
        quiz.questions.add(q)
        quiz.save()
    return Response({
        "status": "success",
        "message": "",
        "quiz": quiz.pk
    })

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def quiz_questions(request: HttpRequest, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for question in quiz.questions.all():
        answers = []
        if question.type == "writeable":
            answers.append({
                "answer": question.answers.first().value_1,
                "is_correct": True
            })
        if question.type == "many_select":
            for answer in question.answers.all():
                answers.append({
                    "answer": answer.value_1,
                    "is_correct": answer.is_correct
                })
            random.shuffle(answers)
        if question.type == "one_select":
            for answer in question.answers.all():
                answers.append({
                    "answer": answer.value_1,
                    "is_correct": answer.is_correct
                })
            random.shuffle(answers)
        if question.type == "matchable":
            for answer in question.answers.all():
                answers.append({
                    "value_1": answer.value_1,
                    "value_2": answer.value_2
                })
            d = []
            keys = [i.get("value_1") for i in answers]
            values = [i.get("value_2") for i in answers]
            random.shuffle(keys)
            random.shuffle(values)
            for i, j in zip(keys, values):
                d.append({
                    "value_1": i,
                    "value_2": j
                })
            answers = d
        questions.append({
            "question": question.question,
            "type": question.type,
            "answers": answers
        })
    return Response({
        "status": "success",
        "message": "",
        "questions": questions
    })

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def module_lessons(request: HttpRequest, pk):
    module = Module.objects.get(pk=pk)
    lessons = Lesson.objects.filter(module=module)
    l = []
    for lesson in lessons:
        l.append({
            "id": lesson.pk,
            "name": lesson.name
        })
    return Response({
        "status": "success",
        "message": "",
        "course": {
            "name": module.course.name,
            "id": module.course.pk
        },
        "name": module.name,
        "lessons": l
    })  


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(["GET"])
def subjects(request: HttpRequest):
    subjects = Subject.objects.all()
    s = []
    for subject in subjects:
        s.append({
            "name": subject.name,
            "id": subject.pk
        })
    return Response({
        "status": "success",
        "message": "",
        "subjects": s
    })

