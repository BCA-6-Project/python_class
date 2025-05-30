from django.contrib import admin
from program.models import Program

# Register your models here.

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
     list_display = ('name',)
     search_field = ('name',)


