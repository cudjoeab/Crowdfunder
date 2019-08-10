# Generated by Django 2.2.4 on 2019-08-09 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunder', '0003_auto_20190809_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='donations_project', to='crowdfunder.Project'),
            preserve_default=False,
        ),
    ]
