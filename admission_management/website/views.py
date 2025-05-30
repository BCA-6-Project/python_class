from django.shortcuts import render

from student.models import Gender, Student, Student_Past_Academics
from program.models import Program
from level.models import Program_Level
from mcq.models import Mcq, Mcq_Question, McqAnswer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

from django.http import JsonResponse
import random
import string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

def websiteIndex(request):
    return render(request, 'web_index.html')

def aboutIndex(request):
    return render(request, 'about_us.html')

def contactIndex(request):
    return render(request, 'contact.html')

def registrationIndex(request):
    gender = Gender.objects.all()
    program = Program.objects.all()

    errors = []  # Store validation errors

    if request.method == "POST":
        name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        gender = request.POST.get('gender', '').strip()
         
        program = request.POST.get('program', '').strip()
        level = request.POST.get('level', '').strip()

        past_program = request.POST.get('past_program', '').strip()
        school_college = request.POST.get('school_college', '').strip()
        board = request.POST.get('board', '').strip()
        status = request.POST.get('status', '').strip()
        percentage = request.POST.get('percentage', '').strip()

        # **Validation Logic**
        if not name:
            errors.append("Name is required.")
        
        if not email:
            errors.append("Email is required.")
        else:
            try:
                validate_email(email)  # Check valid email format
                if Student.objects.filter(email=email).exists():
                    errors.append("Email already exists.")
            except ValidationError:
                errors.append("Invalid email format.")

        if not phone.isdigit() or len(phone) < 10:
            errors.append("Phone number must be at least 10 digits.")

        if not address:
            errors.append("Address is required.")

        if not gender:
            errors.append("Gender is required.")

        if not program:
            errors.append("Program is required.")

        if not level:
            errors.append("Level is required.")

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(8))

        # If no errors, save the data
        if not errors:
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password,
                first_name=name,
                last_name=name
            )

            student = Student.objects.create(
                full_name=name, 
                email=email, 
                contact=phone, 
                address=address, 
                gender_id=gender, 
                program_id=program, 
                level_id=level, 
            )

            Student_Past_Academics.objects.create(
                student_id=student.id, 
                school_college=school_college, 
                program_id=past_program, 
                board= board, 
                status=status, 
                percentage=percentage, 
            )

            return redirect('web_registration')  # Redirect after success
     
    return render(request, 'entrance_registration.html', {'genderList':gender, 'programList': program})

def getLevelByProgramId(request):
    category_id = request.GET.get('program_id')
    data = []
    if category_id:
        subcategories = Program_Level.objects.filter(program_id=category_id).values('id', 'name')
        data = list(subcategories)
    
    return JsonResponse({'levelData': data})

def verificationIndex(request):
    return render(request, 'verify.html')

def resultIndex(request):
    student_id = 1
    answers = McqAnswer.objects.filter(student_id=student_id).select_related('answer__mcq')
    questions = []

    for ans in answers:
        user_answer_obj = ans.answer
        question_group = user_answer_obj.mcq
        question_text = question_group.name  # the main question text

        correct_option = Mcq_Question.objects.filter(mcq=question_group, is_correct=1).first()
        correct_answer = correct_option.name if correct_option else "Unknown"

        questions.append({
            "q": question_text,
            "correct": correct_answer,
            "user": user_answer_obj.name
        })

    return render(request,'result.html', {'questionAnswer':questions})

def mcqIndex(request):
    mcq = list(Mcq.objects.all())  # convert queryset to list so we can shuffle
    random.shuffle(mcq)  # shuffle the questions

    question_data = []

    for val in mcq:
        options = Mcq_Question.objects.filter(mcq_id=val)

        question = {
            'text': val.name,
            'options': [opt.name for opt in options],
            'answer': next((i for i, opt in enumerate(options) if opt.is_correct), None)
        }  

        question_data.append(question)

    return render(request,'mcq.html', {'mcqData': question_data})

@csrf_exempt
def mcqSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        student_id = data.get('student_id')
        answers = data.get('answers', [])

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid student'}, status=400)

        for ans in answers:
            question_text = ans['questionText']
            selected_option_text = ans['selectedOptionText']

            # Get the correct Mcq object
            try:
                mcq = Mcq.objects.get(name=question_text)
            except Mcq.DoesNotExist:
                continue

            # Get the selected Mcq_Question
            try:
                selected = Mcq_Question.objects.get(mcq=mcq, name=selected_option_text)
            except Mcq_Question.DoesNotExist:
                continue

            # Save the answer
            McqAnswer.objects.create(
                student=student,
                answer=selected,
                is_correct=bool(selected.is_correct)
            )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid method'}, status=405)

