import django
from question_site.models import Question, User, Tag, Answer
import random
import string

django.setup()

num_users = 10
users = []

num_questions_per_user = 10
num_answer_per_question = 2

tags = ("cat", "dog", "whiskers", "on", "kittens", "a", "b", "c")
# fill tags
for tag in tags:
    t = Tag.objects.create(name=tag)
    t.save()

# fill Users
for i in range(num_users):
    nickname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    user = User.objects.create_user(nickname, nickname+'@gmail.com', password)
    users.append(user)
    user.save()
    for ii in range(num_questions_per_user):
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        question = Question.objects.create(author=user, title=title, text=text, votes=i*ii)  # no tag
        question.save()
        for _ in range(num_answer_per_question):
            text_answer = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            answer = Answer.objects.create(author=user, question=question, text=text_answer)
            answer.save()

