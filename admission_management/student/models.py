from django.db import models
from program.models import Program
from level.models import Program_Level

class Gender(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'gender'

    def __str__(self):
        return self.name

# Create your models here.
class Student(models.Model):
    full_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255) 
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.ForeignKey(Program_Level, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.full_name+" ("+self.contact+")("+self.email+")"

class Student_Past_Academics(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    school_college = models.CharField(max_length=255)
    board = models.CharField(max_length=255) 
    status = models.CharField(max_length=255) 
    percentage = models.CharField(max_length=255) 
    
    class Meta:
        db_table = 'student_academics'

    def __str__(self):
        return self.school_college+" ("+self.board+")("+self.status+")"


class Student_Documents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    document_name = models.CharField(max_length=255)
    document_attachment = models.CharField(max_length=255) 
    
    class Meta:
        db_table = 'student_documents'
