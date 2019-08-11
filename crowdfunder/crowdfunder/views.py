
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from crowdfunder.models import *
from crowdfunder.forms import *
import pdb

def root(request):
    return HttpResponseRedirect("/home")

def home_page(request):
    projects = Project.objects.all
    context = {'projects': projects }
    return render(request, 'home.html', context)

def search_project(request): 
    query = request.GET['query']
    search_results = Project.objects.filter(title=query, creator=query) # -- option 1-- 
    # search_results = Project.objects.filter(title=query).filter(creator=query) -- option 2 -- 
    return render(request,'search_results.html', {
        'projects': search_results,
        'query': query,
    })

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
def new_reward(request, project_id):
    form = RewardForm()
    context = {"form": form, "project_id": project_id}
    return render(request, "new_reward.html", context)

# @login_required
def create_reward(request, project_id):
    form = RewardForm(request.POST)
    if form.is_valid():
        new_reward = form.save(commit = False)
        new_reward.project = Project.objects.get(pk = project_id)
        new_reward.save()
        return redirect(reverse('project_details', kwargs={'id': project_id}))
    else:
        return render(request, 'new_reward.html', context)



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
        new_donation.project = Project.objects.get(pk = project_id)
        new_donation.reward = new_donation.determine_reward(project_id)
        new_donation.save()
        project = Project.objects.get(pk = project_id)
        project.current_funds = new_donation.total_donations(project_id)
        project.save()
        return redirect(reverse("project_details", kwargs={'id': project_id}))
    else:  # Else sends user back to existing donation form.
        return render(request, "donate_form.html", {
            "project_id": project_id, "form": form
        })

@login_required
def create_comment(request, project_id):
    project = Project.objets.get(pk=project_id)
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
    project = get_object_or_404(Project, pk=id, user=request.user.pk)
    comment = Comment.objects.get(pk=comment_id)
    comment.product_id = comment_id
    form = CommentForm(instance=comment)
    return render(request, "edit_comment_form.html", {
    "comment": comment,
    "form": form,
    "project": project})

@login_required
def update_comment(request, project_id, comment_id):
    project =  get_object_or_404(Project, pk=id, user=request.user.pk)
    comment = Comment.objects.get(pk=comment_id)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return redirect(reverse("project_details"))
    else:
        context = {"comment": comment, "form": form, "project": project}
        return render(request, "edit_comment_form.html", context)

@login_required
def delete_comment(request, project_id, comment_id): 
    comment = get_object_or_404(Comment, pk=id, user=request.user.pk)
    comment.delete()
    return redirect(reverse("project_details", kwargs={"id":project_id}))
            
    
    