from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from crowdfunder.models import *
from crowdfunder.forms import *
import pdb

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
    return render(request, "new_project_form.html", context)

@login_required
def create_project(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        new_project = form.save(commit=False)
        new_project.creator = request.user
        new_project.save()
        return redirect(reverse("home_page"))
    else:  
        context = {"form": form}
        return render(request, "new_project_form.html", context)

@login_required
def new_donate(request, project_id):  # Renders a form for user donations.
    form = DonationForm()
    return render(request, "donate_form.html", {
        "form": form,
        "project_id": project_id
    })

@login_required
def create_donate(request, project_id):  # User creating a new donation.
    form = DonationForm(request.POST)

    if form.is_valid():
        new_donation = form.save(commit=False)
        new_donation.user = request.user
        # new_donation.reward = .... reward instance
        new_donation.save()
        return redirect(reverse("project_details", kwargs={'id': project_id}))
    else:  # Else sends user back to existing donation form.
        return render(request, "donate_form.html", {
            "project_id": project_id, "form": form
        })

@login_required
def create_comment(request, project_id):
    project = Project.objects.get(pk=product_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.project = project
        comment.save()
        return redirect(reverse("project_details", args=(project_id)))
    return render(request, "project_details.html", {
    "project": project, "form": form
    } )

@login_required
def edit_comment(request, project_id, comment_id):
    project = Project.objects.get(pk=project_id)
    comment = Comment.objects.get(pk=comment_id)
    comment.product_id = comment_id
    form = CommentForm(instance=comment)
    return render(request, "edit_comment_form.html", {
    "comment": comment,
    "form": form,
    "project": project})

def update_comment(request, project_id, comment_id):
    project = Project.objects.get(pk=project_id)
    comment = Comment.objects.get(pk=comment_id)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return redirect(reverse("project_details"))
    else:
        context = {"comment": comment, "form": form, "project": project}
        return render(request, "edit_comment_form.html", context)

    def delete_comment(request, project_id, comment_id): 
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return redirect(reverse("project_details", kwargs={"id":project_id}))
            
    
    