from django.contrib import admin
from level.models import Program_Level

# Register your models here.
@admin.register(Program_Level)
class Program_LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'program')
    search_field = ('name','program')
