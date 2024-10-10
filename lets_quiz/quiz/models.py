from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    text = models.TextField("Question Text")
    published = models.BooleanField("Is Published", default=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField("Choice Text", max_length=200, default="Default Choice")
    is_correct = models.BooleanField("Is Correct", default=False)

    def __str__(self):
        return self.text


class AttemptedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Unknown User"
        return f"{username} attempted {self.question.text}"


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'joined_at']

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"
