Career Advisor AI Web Application
A Django-based web application that leverages advanced AI (Groq Llama3-70B model) to analyze resumes, recommend career paths, and generate personalized learning resources. Users can upload their resumes (PDF/TXT), chat with an AI career advisor, and receive tailored job recommendations and educational guidance.

Features
AI-Powered Resume Analysis:
Upload your resume and get 5 personalized job recommendations using the Groq Llama3-70B model.

Learning Path Generator:
Enter your interests and receive a structured, web-formatted learning path and resource recommendations.

Chat History:
All interactions and AI responses are saved for each user.

User Authentication:
Secure registration, login, and logout functionality.

Tech Stack
Backend: Django (Python)

AI Integration: Groq API (Llama3-70B)

PDF Processing: PyPDF2

Frontend: Django Templates (HTML)

Database: Django ORM (SQLite/PostgreSQL)

Setup Instructions
Clone the Repository


bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
Create and Activate a Virtual Environment


bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies


bash
pip install -r requirements.txt
Set Up Environment Variables

Important: For security, set your Groq API key as an environment variable:


bash
export GROQ_API_KEY="your_groq_api_key"
Update the code to read the API key from the environment instead of hardcoding it.

Apply Migrations

bash
python manage.py runserver
Access the Application

Open your browser and go to http://127.0.0.1:8000/

Usage
Register or log in to your account.

Upload your resume (PDF or TXT) and/or type a message in the chat interface.

Receive AI-powered career recommendations.

Ask for learning resources by entering your interests in the "Interests" section.

View your chat and resource history at any time.

File Structure

text
project_root/
│
├── careeradvisor/           # Main Django app
│   ├── models.py            # Chat and Interests models
│   ├── views.py             # Main logic (this file)
│   ├── forms.py             # ChatForm for user input
│   ├── templates/chatbot/   # HTML templates
│   └── ...
├── djangoenv/               # Virtual environment (optional)
├── manage.py
└── requirements.txt
Security Notes
API Keys: Never hardcode API keys in production. Use environment variables.

File Uploads: Only PDF and TXT files are supported. Add validation for file type and size in production.

Error Handling: Basic error handling is implemented for API calls.

Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

License
MIT

Acknowledgements
Groq API

PyPDF2

Django
