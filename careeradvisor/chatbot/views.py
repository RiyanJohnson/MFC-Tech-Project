from django.shortcuts import render, redirect
from .models import Chat, Interests
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import ChatForm
from django.http import JsonResponse
import PyPDF2

def home(request):
    return render(request, 'chatbot/landingpage.html')

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

def chatbot(request):
    if request.method == 'POST':
        form = ChatForm(request.POST,request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user 

            extracted_text = "" 

            if chat.file:
                if chat.file.name.endswith('.pdf'):
                    extracted_text = extract_text_from_pdf(chat.file)
                elif chat.file.name.endswith('.txt'):
                    extracted_text = extract_text_from_txt(chat.file)

            chat.message = form.cleaned_data.get('message','').strip() + extracted_text

            response_text = "Hi"

            chat.response = response_text
            chat.save()
            return redirect('chatbot') 

    else:
        form = ChatForm()

    chats = Chat.objects.filter(user=request.user).order_by('-created_at')  
    return render(request, 'chatbot/chatbot.html', {'form': form, 'chats': chats})

def chatbot_interests(request):
    chats = Interests.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = "Hi"

        chat = Interests(user=request.user, message=message, response=response, created_at=timezone.now)
        chat.save()
        return redirect('interests')
    return render(request, 'chatbot/interests.html', {'chats': chats})

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'chatbot/login.html', {'error_message': error_message})
        
    else:
        return render(request, 'chatbot/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
            except:
                error_message = 'Error creating account'
            return render(request, 'chatbot/register.html', {'error_message': error_message})
        else:
            error_message = "Password don't match" 
            return render(request, 'chatbot/register.html', {'error_message': error_message})
    return render(request, 'chatbot/register.html')

def logout(request):
    auth.logout(request)
    return redirect('home')