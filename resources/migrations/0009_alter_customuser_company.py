# Generated by Django 4.1.7 on 2023-03-12 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_alter_customuser_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resources.company', to_field='name'),
        ),
    ]
