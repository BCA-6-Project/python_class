from django.contrib import admin
from student.models import Student
from student.models import Gender
from .models import Student_Past_Academics, Student_Documents

# Register your models here.

class Student_DocumentsInline(admin.TabularInline):
    model = Student_Documents
    extra = 1

class Student_Past_AcademicsInline(admin.TabularInline):
    model = Student_Past_Academics
    extra = 1

@admin.register(Student)
class Student_InfoAdmin(admin.ModelAdmin):
    list_display = ('full_name','contact','email')
    search_field = ('full_name','contact','email')
    inlines = [Student_DocumentsInline, Student_Past_AcademicsInline]


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_field = ('name',)

