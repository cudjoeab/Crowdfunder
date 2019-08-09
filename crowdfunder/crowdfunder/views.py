from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from crowdfunder.models import *

def root(request):
    return HttpResponseRedirect("/home")

def home_page(request):
    pass

def project_details(request, id):
    project = Project.objects.get(pk=id)
    return render(request, "project_details.html", {
    'project': project
    })

def login_view(request):
    pass

def logout_view(request):
    pass

def signup_view (request):
    pass

def new_project(request):
    form = ProjectForm()
    context = {"form": form}
    return render(request, "project_form.html", context)

def create_project(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("homepage"))
    else:  
        context = {"form": form}
        return render(request, "project_form.html", context)

    
def new_donate(request):  # Generates a form for user donations.
    pass

def create_donate(request):  # Validates user donation and saves to database.
    pass
