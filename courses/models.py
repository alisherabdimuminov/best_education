from django.db import models

from users.models import User


QUESTION_TYPE = (
    ("one_select", "One select"),
    ("many_select", "Many select"),
    ("writable", "Writable"),
    ("matchable", "Matchable")
)
LESSON_TYPE = (
    ("lesson", "Lesson"),
    ("quiz", "Quiz")
)

class Answer(models.Model):
    value_1 = models.TextField()
    value_2 = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.value_1

class Question(models.Model):
    question = models.TextField()
    type = models.CharField(max_length=20, )
    answers = models.ManyToManyField(Answer, related_name="question_answers", null=True, blank=True)

    def __str__(self):
        return self.question
    
class Quiz(models.Model):
    name = models.CharField(max_length=500)
    questions = models.ManyToManyField(Question, related_name="quiz_questions")

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_author")
    image = models.ImageField(upload_to="images/courses")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="course_subject")
    description = models.TextField()
    feedback = models.FloatField(null=True, default=0)
    feedbackers = models.ManyToManyField(User, related_name="course_feedbackers", null=True, blank=True)
    price = models.IntegerField()
    students = models.ManyToManyField(User, related_name="course_students", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def count_modules(self):
        return Module.objects.filter(course=self).count()
    
    def modules(self):
        return Module.objects.filter(course=self)
    
    def count_lessons(self):
        count = 0
        modules = Module.objects.filter(course=self)
        for i in modules:
            count += i.count_lessons()
        return count

    def count_quizzes(self):
        count = 0
        modules = Module.objects.filter(course=self)
        for i in modules:
            count += i.count_quizzes()
        return count
    
class Module(models.Model):
    name = models.CharField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    required = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    passing_score = models.IntegerField()
    students = models.ManyToManyField(User, related_name="module_students", null=True, blank=True)
    finishers = models.ManyToManyField(User, related_name="module_finishers", null=True, blank=True)

    def __str__(self):
        return self.name
    
    def count_lessons(self):
        return Lesson.objects.filter(module=self, type="lesson").count()
    
    def lessons(self):
        return Lesson.objects.filter(module=self)
    
    def count_quizzes(self):
        return Lesson.objects.filter(module=self, type="quiz").count()

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    video = models.URLField(max_length=1000, null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)
    resource = models.FileField(upload_to="files/lessons/", null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=30, choices=LESSON_TYPE)
    previous = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="previous_lesson")
    next = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="next_lesson")
    finishers = models.ManyToManyField(User, related_name="lesson_finishers", null=True, blank=True)
    score = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Check(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="check_user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="check_course")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="check_module")
    active = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.course.name + " - " + self.module.name + " - " + self.author.username
