# Generated by Django 5.0.8 on 2024-08-07 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subordinates', to='employees.employee')),
                ('subordinate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='employees.employee')),
            ],
            options={
                'unique_together': {('manager', 'subordinate')},
            },
        ),
    ]
