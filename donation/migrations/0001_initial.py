# Generated by Django 4.2 on 2025-04-16 21:06

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
                ('is_donor', models.BooleanField(default=False)),
                ('is_ngo', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FoodListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(choices=[('vegetarian', 'Vegetarian'), ('non-vegetarian', 'Non-Vegetarian'), ('vegan', 'Vegan'), ('bakery', 'Bakery'), ('dairy', 'Dairy')], max_length=100)),
                ('quantity', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('expiry_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2025, 4, 16))])),
                ('pickup_location', models.TextField()),
                ('pickup_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_listings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Food Listing',
                'verbose_name_plural': 'Food Listings',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NGOProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(help_text='Official registered name of the NGO', max_length=200, verbose_name='Organization Name')),
                ('registration_number', models.CharField(help_text='Government-issued registration ID', max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Only letters, numbers, and hyphens are allowed', regex='^[A-Za-z0-9-]+$')], verbose_name='Registration Number')),
                ('address', models.TextField(help_text='Street, City, State/Province, Postal Code', verbose_name='Full Address')),
                ('contact_person', models.CharField(help_text='Name of the authorized representative', max_length=100, verbose_name='Primary Contact Person')),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number (8-15 digits, optional +)', regex='^\\+?[0-9]{8,15}$')], verbose_name='Contact Number')),
                ('proof_document', models.FileField(help_text='Upload scanned copy of registration certificate (PDF or image)', upload_to='ngo_documents/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'], message='Only PDF and image files are allowed')], verbose_name='Registration Proof')),
                ('verified', models.BooleanField(default=False, help_text='Designates whether this NGO has been verified by admin', verbose_name='Verification Status')),
                ('date_registered', models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ngo_profile', to=settings.AUTH_USER_MODEL, verbose_name='User Account')),
            ],
            options={
                'verbose_name': 'NGO Profile',
                'verbose_name_plural': 'NGO Profiles',
                'ordering': ['-date_registered'],
            },
        ),
        migrations.CreateModel(
            name='FoodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('contact_info', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('collected', 'Collected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('food_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='donation.foodlisting')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='ngoprofile',
            index=models.Index(fields=['registration_number'], name='donation_ng_registr_409fb8_idx'),
        ),
        migrations.AddIndex(
            model_name='ngoprofile',
            index=models.Index(fields=['organization_name'], name='donation_ng_organiz_59349f_idx'),
        ),
    ]
