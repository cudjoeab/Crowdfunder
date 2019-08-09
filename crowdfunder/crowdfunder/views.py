from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from crowdfunder.models import *

def root(request):
    return HttpResponseRedirect("/home")

def home_page(request):
    projects = Project.objects.all
    context = {'projects': projects }
    return render(request, 'home.html', context)

def project_details(request, id):
    project = Project.objects.get(pk=id)
    return render(request, "project_details.html", {
    'project': project
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm (request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')

def signup_view (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

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

@login_required
def new_donate(request):  # Renders a form for user donations.
    form = DonateForm()
    return render(request, "donate_form.html", {
        "form": form
    })

@login_required
def create_donate(request, project_id):  # User creating a new donation.
    form = DonateForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect(reverse("show_all"))
    else:  # Else sends user back to existing donation form.
        return render(request, "edit_product_form.html", {
            "product": product, "form": form
        }) 