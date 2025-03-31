from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name = 'home'),
    path('chatbot/',views.chatbot, name = 'chatbot'),
    path('chatbot/interests',views.chatbot_interests, name = 'interests'),
    path('login/',views.login, name = 'login'),
    path('register/',views.register, name = 'register'),
    path('logout/',views.logout, name = 'logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)