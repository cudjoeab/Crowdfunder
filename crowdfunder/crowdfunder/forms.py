<<<<<<< HEAD
from django.forms import ModelForm
from crowdfunder.models import Profile, Project, Comment, Reward, Donation
from django.forms import CharField, PasswordInput, Form

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'first_name', 'last_name']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'end_date', 'description']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ['description', 'level']


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['price_in_cents']


class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())
