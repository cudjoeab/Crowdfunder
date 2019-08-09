from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from crowdfunder.models import *

def root(request):
    return HttpResponseRedirect("/home")

def home_page(request):
    pass

def project_details(request):
    pass

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
    form = ProjecttForm(request.POST)
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
