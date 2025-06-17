from django.db import models
from student.models import Student
from program.models import Program
from level.models import Program_Level

# Create your models here.
class Mcq(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=1)
    level = models.ForeignKey(Program_Level, on_delete=models.CASCADE, default=1)
    difficulty = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'mcq'

    def __str__(self):
        return self.name
    
class Mcq_Question(models.Model):
    name = models.CharField(max_length=255)
    mcq = models.ForeignKey(Mcq, on_delete=models.CASCADE)
    is_correct = models.SmallIntegerField(default=0)
    
    class Meta:
        db_table = 'mcq_question'

    def __str__(self):
        return self.name
    
class McqAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='options')
    answer = models.ForeignKey(Mcq_Question, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'mcq_answer'

    def __str__(self):
        return self.answer.name