import pandas as pd
import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from django.shortcuts import render, redirect
from .models import Chat, Interests
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import ChatForm
from django.http import JsonResponse
import PyPDF2

model = 'groq/llama3-8b-8192'
llm = ChatGroq(
        temperature=0, 
        groq_api_key = os.getenv('GROQ_API_KEY'), 
        model_name=model
    )

def career_analyser_agent(message):
    Career_Analyzer_Agent = Agent(
    role='Career_Analyzer_Agent',
    goal="""Analyze user-submitted resumes and suggest the best career options based on 
        their experience, skills, and qualifications. Provide career pivot suggestions 
        and highlight relevant job roles.""",
    backstory="""You are an expert career analyst, skilled in parsing resumes and identifying 
        the best career paths for users based on their skills, experience, and market demand.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
    task_define_problem = Task(
    description="""Understand and analyse the user's resume, 
    including identifying the skills and specific projects, education, languages known .

    Here is the user's resume in text form:
    {resume}
    """.format(resume=message),
agent=Career_Analyzer_Agent,
expected_output="A clear and concise summary , skills of the given resume and also provide career pivot suggestions and highlight relevant job roles."
)
    crew1 = Crew(
    agents=[Career_Analyzer_Agent], 
    tasks=[task_define_problem], 
    verbose=False
)
    return crew1.kickoff1


def task_generate_resources(message):
    Skill_Builder_Agent = Agent(
    role='Skill_Builder_Agent',
    goal="""Recommend personalized learning resources based on user-inputted interests. 
        Suggest online courses, certifications, and skill-building activities relevant 
        to their career goals.""",
    backstory="""You are a knowledgeable learning advisor, adept at curating the best educational 
        resources to help users upskill and achieve their career aspirations.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


    task_generate_resources = Task(
    description="""Generate personalized learning resources based on the user's specified interests and preferences,
        including relevant online courses, tutorials, documentation, books, and practice projects

        Here are the user's interests:
        {interests}
        """.format(interests=message),
        agent=Skill_Builder_Agent,
        expected_output="Curated list of learning resources including online courses, tutorials, documentation, books, and practice projects, tailored to the user's interests and skill level, plus a brief learning path recommendation."
)


    crew2 = Crew(
        agents=[Skill_Builder_Agent],
        tasks=[task_generate_resources],
        verbose=False
)
    return crew2.kickoff()


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

            chat.message = ''+form.cleaned_data.get('message','').strip() + extracted_text
            response_text = career_analyser_agent(chat.message)
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
        response = task_generate_resources(message)

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


