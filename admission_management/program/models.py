from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'program'

    def __str__(self):
        return self.name

