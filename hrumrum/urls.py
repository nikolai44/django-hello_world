"""hrumrum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from question_site import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="home"),

    path('hot', views.hot, name="hot"),

    path('new', views.home, name="new"),

    path('add/question', views.new_question, name="new_question"),

    path('question/<int:question_id>', views.question, name="question"),

    path('question/<int:question_id>/vote', views.vote, name="vote"),

    path('question', views.question, name="question"),

    path('tag/<str:tag>', views.question_by_tag, name="question_by_tag"),

    path('settings/<str:user_id>', views.settings, name="settings"),

    path('accounts/registration', views.registration, name="registration"),

    path('accounts/login', auth_views.LoginView.as_view(template_name='registration/login.html',
        extra_context=views.sidebar(), redirect_authenticated_user=True), name="login"),          # redirect_authenticated_user - if logged in redirect to homepage

    path('accounts/logout', auth_views.LogoutView.as_view(), name="logout"),

    path('accounts/add/avatar', views.add_avatar, name="add_avatar"),

    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
