from django.db import models
from django.contrib.auth.models import User

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
)


class Profile(models.Model):
    # username = models.CharField(max_length=300)
    first_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300, blank=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE )

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'


class Project(models.Model):
    title = models.CharField(max_length=300)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'project')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )

    def __str__(self):
        return f'{self.title} by {self.creator}'


class Comment(models.Model):
    message = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments_profile')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments_project')

    def __str__(self):
        return f'"{self.message}" - by {self.profile} on{self.project}'

    
class Reward(models.Model):
    description = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    level = models.IntegerField(
        validators=[MinValueValidator(0)], null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name = 'rewards_project')

    def __str__(self):
        return f"{self.description} - Level: {self.level} - Project: {self.project}"


class Donation(models.Model):
    price_in_cents = models.IntegerField(
        validators=[MinValueValidator(100)], null=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='donations_profile')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='donations_reward')

    def __str__(self):
        return f"{self.price_in_cents} pennies - Donator: {self.profile} - Reward: {self.reward}"

    def price_in_dollars(self):  # Converts cents to dollars.
        return self.price_in_cents / 100

    