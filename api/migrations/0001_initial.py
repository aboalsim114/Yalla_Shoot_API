# Generated by Django 5.0.3 on 2024-03-28 23:15

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='Date and Time')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('sport', models.CharField(max_length=255, verbose_name='Sport')),
                ('required_skill_level', models.CharField(max_length=255, verbose_name='Required Skill Level')),
                ('players_needed', models.PositiveIntegerField(verbose_name='Players Needed')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('player', 'Player'), ('organisator', 'Organisator')], default='player', max_length=11, verbose_name='User Type')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Location')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Sent At')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(verbose_name='Age')),
                ('gender', models.CharField(max_length=10, verbose_name='Gender')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Weight')),
                ('favorite_sports', models.CharField(max_length=255, verbose_name='Favorite Sports')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Skill Level')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='MatchRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=255, verbose_name='Status')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='api.match', verbose_name='Match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='api.playerprofile', verbose_name='Player')),
            ],
        ),
        migrations.CreateModel(
            name='SportActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.CharField(max_length=255, verbose_name='Sport')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration in Minutes')),
                ('calories_burned', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Calories Burned')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.playerprofile', verbose_name='Player')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255, verbose_name='Team Name')),
                ('sport', models.CharField(max_length=255, verbose_name='Sport')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Skill Level')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='api.team', verbose_name='Team'),
        ),
    ]
