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
    path('already_donated/', views.already_donated, name='already_donated'),
    # search ABIGAIL
    path('search', views.search_project, name='search_project'),
    # registration SHAHEER
    path('login/', views.login_view, name="login"), 
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"), 
    # projects  ABIGAIL
    path('project/<int:project_id>', views.project_details, name="project_details"),
    path('project/<int:project_id>/edit', views.edit_project, name="edit_project"),
    path('project/<int:project_id>/new_reward', views.new_reward, name='new_reward'),
    path('project/<int:project_id>/create_reward', views.create_reward, name = 'create_reward'),
    path('project/new', views.new_project, name="new_project"), 
    path('project/create', views.create_project, name="create_project"), 
    path('project/<int:project_id>/delete', views.delete_project, name="delete_project"),
    # backing ADAM
    path('project/<int:project_id>/donate', views.new_donate, name="new_donate"), # Form
    path('project/<int:project_id>/donatecreate', views.create_donate, name="create_donate"), # Access the database, Validate

    # comments ABIGAIL 
    path('project/<int:project_id>/comments/create', views.create_comment, name="create_comment"),  
    # path('project/<int:project_id>/comments/<int:comment_id>/update', views.update_comment, name="update_comment"),
    path('project/<int:project_id>/comments/<int:comment_id>/edit', views.edit_comment, name="edit_comment"), 
    path('project/<int:project_id>/comments/<int:comment_id>/delete',views.delete_comment, name="delete_comment"), 

    # Updates for Projects
    path('project/<int:project_id>/updates/create', views.create_update, name="create_update"),  

    path('users', views.all_users, name="all_users"), # A list of all users.
    path('user/<int:user_id>', views.user_profile, name="user_profile"), # User profile page

    path('profile/<int:user_id>/new', views.new_profile, name='new_profile'),
    path('profile/create', views.create_profile, name='create_profile'),
    path('user/<int:user_id>/edit', views.edit_profile, name="edit_profile"),
    path('user/<int:user_id>/delete', views.delete_profile, name="delete_profile"),
]
