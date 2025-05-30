from django.db import models
from program.models  import Program

# Create your models here.
class Program_Level(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'program_level'

    def __str__(self):
        return self.name

    