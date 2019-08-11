"""crowdfunder URL Configuration

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
from django.urls import path
import crowdfunder.views as views

urlpatterns = [
    #base STANLEY
    path('admin/', admin.site.urls),
    path('', views.root), 
    path('home/', views.home_page, name="home_page"), 
    # registration SHAHEER
    path('login/', views.login_view, name="login"), 
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"), 
    # projects  ABIGAIL
    path('project/<int:id>', views.project_details, name="project_details"),
    path('project/new', views.new_project, name="new_project"), 
    path('project/create', views.create_project, name="create_project"), 
    path('project/<int:id>/edit', views.edit_project, name="edit_project"),
    # backing ADAM
    path('project/<int:project_id>/donate', views.new_donate, name="new_donate"), # Form
    path('project/<int:project_id>/donatecreate', views.create_donate, name="create_donate"), # Access the database, Validate
    
]
