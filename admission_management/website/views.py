from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from student.models import Gender, Student, Student_Past_Academics
from program.models import Program
from level.models import Program_Level
from mcq.models import Mcq, Mcq_Question, McqAnswer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
import math
import random
from collections import Counter
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
import random
import string
from django.db.models import Count
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
        password = '12345'
        # password = ''.join(random.choice(characters) for _ in range(8))

        # If no errors, save the data
        if not errors:
            user = User.objects.create_user(
                username=email,
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

@csrf_exempt
def sendStudentOtp(request):
    data = json.loads(request.body)
    email = data.get('email')

    if not email:
        return JsonResponse({'message': 'Email is required'}, status=400)

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))

        # Send email
    subject = "Your OTP Code"
    from_email = 'kiranjethara470@gmail.com'
    to = [email]

    html_content = render_to_string('email/otp_email.html', {'otp': otp})

    email_msg = EmailMultiAlternatives(subject, '', from_email, to)
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

    # Optionally save the OTP in session or DB
    # Get the user (by email, username, or id)
    user = User.objects.get(username=email)  # or .get(email='...')
    user.set_password(otp)
    user.save()

    return JsonResponse({'message': 'OTP sent successfully!'})

def checkVerificationIndex(request):
   email = request.POST.get('email') 
   otp = request.POST.get('otp') 

   user = authenticate(request, username=email, password=otp)

   if user is not None:
       login(request, user)
       return redirect('mcq')
   else:
       return render(request, 'verify.html', {'error':'Invalid Credentials'})

@login_required
def userLogout(request):
    logout(request)
    return redirect('web_home_page')

@login_required
def resultIndex(request):
    student_id = request.user.id
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

@login_required
def mcqIndex(request):
    studentPreferences = Student.objects.get(email=request.user.username)

    mcq_list = list(
        Mcq.objects.filter(
            program_id=studentPreferences.program_id,
            level_id=studentPreferences.level_id
        ).values_list('id', 'difficulty')
    )

    selected_mcqs = select_balanced_mcqs(mcq_list, num=25)

    # If you need full objects:
    selected_ids = [mcq_id for mcq_id, _ in selected_mcqs]
    questions = Mcq.objects.filter(id__in=selected_ids)

    # mcq = list(Mcq.objects.filter(program_id=studentPreferences.program_id, level_id=studentPreferences.level_id))  # convert queryset to list so we can shuffle
    # random.shuffle(mcq)  # shuffle the questions

    question_data = []

    for val in questions:
        options = Mcq_Question.objects.filter(mcq_id=val)

        # Step 1: Prepare options as a list of (option_text, is_correct) tuples
        option_list = [(opt.name, opt.is_correct) for opt in options]

        # Step 2: Shuffle the options randomly
        random.shuffle(option_list)

        # Step 3: Extract the option texts
        shuffled_option_texts = [opt[0] for opt in option_list]

        # Step 4: Find the new index of the correct answer
        correct_index = next((i for i, opt in enumerate(option_list) if opt[1]), None)

        question = {
            'text': val.name,
            'options': shuffled_option_texts,
            'answer': correct_index
        }  

        question_data.append(question)

    return render(request,'mcq.html', {'mcqData': question_data})

def calculate_entropy(mcqs):
    total = len(mcqs)
    difficulty_counts = Counter([d for (_, d) in mcqs])
    entropy = 0
    for count in difficulty_counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def select_balanced_mcqs(mcq_list, num=25, trials=50):
    best_entropy = -1
    best_sample = []

    for _ in range(trials):
        sample = random.sample(mcq_list, num)
        entropy = calculate_entropy(sample)

        if entropy > best_entropy:
            best_entropy = entropy
            best_sample = sample

    return best_sample

@csrf_exempt
@login_required
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

