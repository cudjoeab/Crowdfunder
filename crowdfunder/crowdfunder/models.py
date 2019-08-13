from django.db import models
from django.contrib.auth.models import User

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    first_name = models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    description = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(500)])
    total_donations = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    title = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'project')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    fund_goal = models.FloatField(
        validators = [MinValueValidator(100)]
    )
    current_funds = models.CharField(max_length = 100, blank = True, null = True)
 
    

    def __str__(self):
        return f'{self.title} by {self.creator}'


class Comment(models.Model):
    message = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_profile')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments_project')

    def __str__(self):
        return f'"{self.message}" - by {self.user} on{self.project}'

    
class Reward(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    minimum_donation = models.FloatField(
        validators=[MinValueValidator(0)], null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name = 'rewards_project')


    def __str__(self):
        return f"{self.minimum_donation} - {self.name}"


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_profile')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations_project')
    price_in_cents = models.IntegerField(
        validators=[MinValueValidator(100)], null=True
    )
    reward = models.ForeignKey(Reward, blank = True, null = True, on_delete=models.CASCADE, related_name='donations_reward')

    def __str__(self):
        # Changed so it displays the dollar price instead of cents
        return f"{self.price_in_cents/100} dollars - Donator: {self.user} - Reward: {self.reward}"

    def price_in_dollars(self):  # Converts cents to dollars.
        return self.price_in_cents / 100
    
    @classmethod
    def total_donations(cls, project_id):
        return Donation.objects.filter(project = project_id).aggregate(models.Sum('price_in_cents'))['price_in_cents__sum']/100
    
    @classmethod
    def total_donations_user(cls, user_id):
        user_donations = Donation.objects.filter(user = user_id).aggregate(models.Sum('price_in_cents'))
        # return user_donations
        if user_donations['price_in_cents__sum'] != None:
            return f'${user_donations["price_in_cents__sum"]/100}'
        else:
            return None

    def determine_reward(self, project_id):
        rewards_list = Reward.objects.filter(project = project_id).order_by('minimum_donation')
        temp_reward = None
        for i in range(len(rewards_list)):
            if self.price_in_cents/100 >= rewards_list[i].minimum_donation:
                temp_reward = rewards_list[i]
        return temp_reward

    @classmethod
    def check_donation(cls, project_id, user_id):
        donations = Donation.objects.filter(project = project_id)
        donation = None
        for d in donations:
            if d.user == user_id:
                donation = d
        if donation:
            return True
        else: 
            return False

class Update(models.Model):
    message = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updates_profile')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates_project')

    def __str__(self):
        return f'"{self.message}" - by {self.user} on {self.project}'
