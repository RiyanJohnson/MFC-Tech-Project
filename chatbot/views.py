import os
from groq import Groq
from django.shortcuts import render, redirect
from .models import Chat, Interests
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import ChatForm
import PyPDF2

# Initialize Groq client directly
client = Groq(api_key="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")
MODEL_NAME = "llama3-70b-8192"

def career_analyser_agent(message):
    """Analyze resumes using direct Groq API calls"""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert career analyst. Analyze resumes and 
                    suggest career options based on skills and experience."""
                },
                {
                    "role": "user",
                    "content": f"Analyze this resume:\n{message}\n\nProvide 5 job recommendations."
                }
            ],
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"

def task_generate_resources(message):
    """Generate learning resources using direct Groq API"""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a learning advisory exper and an expert in optimizing outputs. Recommend educational 
                    resources based on user interests.
                    Provide relevant and useful answers.
                    Output has to be generated with proper formatting for Django and HTML.
                 
                    
                    """
                },
                {
                    "role": "user",
                    "content": f"Create learning path for: {message} with proper formatting like the output will be displayed in a webpage and the output will be returned to a django file."}
            ],
            model=MODEL_NAME,
            temperature=0.5,
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"

def extract_text_from_pdf(file):
    """Extract text from PDF files"""
    pdf_reader = PyPDF2.PdfReader(file)
    return '\n'.join(page.extract_text() for page in pdf_reader.pages)

def extract_text_from_txt(file):
    """Extract text from TXT files"""
    return file.read().decode('utf-8')

def chatbot(request):
    """Main chatbot view handling file uploads"""
    if request.method == 'POST':
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user
            
            if chat.file:
                if chat.file.name.endswith('.pdf'):
                    extracted_text = extract_text_from_pdf(chat.file)
                elif chat.file.name.endswith('.txt'):
                    extracted_text = extract_text_from_txt(chat.file)
                else:
                    extracted_text = ""
            else:
                extracted_text = ""
            
            chat.message = f"{form.cleaned_data.get('message', '')}\n{extracted_text}".strip()
            chat.response = career_analyser_agent(chat.message)
            chat.save()
            return redirect('chatbot')
    else:
        form = ChatForm()

    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatbot/chatbot.html', {'form': form, 'chats': chats})

def chatbot_interests(request):
    """Handle learning resource requests"""
    chats = Interests.objects.filter(user=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = task_generate_resources(message)
        Interests.objects.create(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now()
        )
        return redirect('interests')
        
    return render(request, 'chatbot/interests.html', {'chats': chats})

# Authentication views remain unchanged
def home(request):
    return render(request, 'chatbot/landingpage.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('home')
        return render(request, 'chatbot/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'chatbot/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                auth.login(request, user)
                return redirect('home')
            except:
                return render(request, 'chatbot/register.html', 
                           {'error_message': 'Account creation failed'})
        return render(request, 'chatbot/register.html', 
                    {'error_message': 'Password mismatch'})
    return render(request, 'chatbot/register.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
