from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", related_name="user_accounts")
    name = models.CharField(max_length=20)
    secondname = models.CharField(max_length=20)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    def __str__(self):
        return f"{self.name}{self.description}"

class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="предмет")
    def __str__(self):
        return f'{self.name}'

class Diary(models.Model):
    student = models.ForeignKey(Accounts, on_delete=models.CASCADE, verbose_name='Студент', related_name='user_diary')
    grade = models.PositiveIntegerField(verbose_name="оцінка", validators=[MinValueValidator(1), MaxValueValidator(100)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="student_subject")
    def __str__(self):
        return f'{self.student}-{self.grade}-{self.subject}'


