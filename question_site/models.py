from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from question_site.managers import UserManager, TagManager, QuestionManager, AnswerManager

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(default="uploads/default_user.png", upload_to="uploads/",
                               verbose_name="User's Avatar")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="User's Registration Date")
    rating = models.IntegerField(default=0, verbose_name="User's Rating")
    objects = UserManager()

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=20, default="404", verbose_name="Question's Tag")
    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, default=True, related_name='questions', verbose_name="Question's Tags")
    votes = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Answer's Owner", on_delete=models.CASCADE)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    approved = models.BooleanField(default=False, verbose_name="Approved by author")
    date = models.DateTimeField(default=timezone.now)
    objects = AnswerManager()

    def __str__(self):
        return self.text
