#Portfolio\SIPA\courses\models.py

from django.db import models

# Create your models here.


class Competency(models.Model):
    CATEGORY_CHOICES = [
        ('basic', 'Basic'),
        ('professional', 'Professional'),
        ('specific', 'Specific'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    hours = models.IntegerField()
    credits = models.IntegerField()
    semester = models.CharField(max_length=20)
    major = models.CharField(max_length=255)
    competencies = models.ManyToManyField(Competency, through='CourseCompetency')

    def __str__(self):
        return self.name

class CourseCompetency(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    occurrence = models.IntegerField(default=1)
