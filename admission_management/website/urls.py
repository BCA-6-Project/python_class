from django.urls import path
from . import views

urlpatterns = [
    path('', views.websiteIndex, name="web_home_page"),

    path('about/', views.aboutIndex, name="web_about_us"),

    path('registration/', views.registrationIndex, name="web_registration"),
    path('ajax/get-program-level/', views.getLevelByProgramId, name='get_program_level'),

    path('contact/', views.contactIndex, name="web_contact_page"),
    path('student_verification/', views.verificationIndex, name="student_verification"),
    path('result/', views.resultIndex, name="result"),
    path('mcq/', views.mcqIndex, name="mcq"),
    path('save_mcq/', views.mcqSave, name="save_mcq"),
]