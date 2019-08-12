from django.contrib import admin
from crowdfunder.models import Project, Comment, Reward, Donation, Update

admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Reward)
admin.site.register(Donation)
admin.site.register(Update)
