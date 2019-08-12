from django.forms import ModelForm
from crowdfunder.models import Project, Comment, Reward, Donation, Profile
from django.forms import CharField, PasswordInput, Form

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'end_date', 'description', 'fund_goal']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'minimum_donation']


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['price_in_cents']


class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class ProfileForm(Form):
    class Meta: 
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'description']