
from django.forms import ModelForm, ModelChoiceField
from crowdfunder.models import Project, Comment, Reward, Donation, Profile
from django.forms import CharField, PasswordInput, Form
from datetime import datetime, date
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'end_date', 'description', 'fund_goal']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        today = date.today()
        if start_date < today:
            self.add_error('start_date', 'The date cannot be earlier than today')
        if end_date <= start_date:
            self.add_error('end_date', 'The date cannot be earlier than the start date')



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
        project = model.project 
        fields = ['reward', 'price_in_cents']

    def clean(self):
        cleaned_data = super().clean()
        reward_level = cleaned_data.get('reward')
        price_in_cents = cleaned_data.get('price_in_cents')
        donation = price_in_cents/100
        if reward_level.minimum_donation > donation:
            self.add_error('price_in_cents', 'The donation amount must be at least the reward level')


class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class ProfileForm(ModelForm):
    class Meta: 
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'description']