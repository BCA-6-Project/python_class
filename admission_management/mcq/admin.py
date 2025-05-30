from django.contrib import admin
from .models import Mcq, Mcq_Question

class McqQuestionInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = Mcq_Question
    extra = 4  # default number of option inputs shown
    fields = ['name', 'is_correct']  # what fields to show for each choice

class McqAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [McqQuestionInline]

admin.site.register(Mcq, McqAdmin)
