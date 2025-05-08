from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator  # Add this import
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Donor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Changed from auth.User
        on_delete=models.CASCADE,
        primary_key=True
    )
    # Keep all your existing fields exactly as they are
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    verified = models.BooleanField(default=False)

class Receiver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Changed from auth.User
        on_delete=models.CASCADE,
        primary_key=True
    )
    # Keep all your existing fields
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    verified = models.BooleanField(default=False)

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

class FoodListing(models.Model):
    FOOD_CATEGORIES = [
        ('vegetarian', 'Vegetarian'),
        ('non-vegetarian', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('bakery', 'Bakery'),
        ('dairy', 'Dairy'),
    ]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_listings')
    food_type = models.CharField(max_length=100, choices=FOOD_CATEGORIES)
    quantity = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    expiry_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    pickup_location = models.TextField()
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    
    # ✅ New image field to store food images
    image = models.ImageField(upload_to='media/food_images', blank=True, null=True)  

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Food Listing"
        verbose_name_plural = "Food Listings"

    def __str__(self):
        return f"{self.get_food_type_display()} ({self.quantity})"


class FoodRequest(models.Model):
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    food_listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.receiver.user.username} for {self.food_listing.food_type}"
    

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_ngo = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'auth_user' 

from django.core.validators import FileExtensionValidator

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

class NGOProfile(models.Model):
    """
    Represents an NGO profile with comprehensive validation and documentation.
    All fields are required and validated before saving.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ngo_profile',
        verbose_name=_('User Account')
    )
    
    organization_name = models.CharField(
        max_length=200,
        verbose_name=_('Organization Name'),
        help_text=_('Official registered name of the NGO')
    )
    
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Registration Number'),
        help_text=_('Government-issued registration ID'),
        validators=[
            RegexValidator(
                regex='^[A-Za-z0-9-]+$',
                message=_('Only letters, numbers, and hyphens are allowed')
            )
        ]
    )
    
    address = models.TextField(
        verbose_name=_('Full Address'),
        help_text=_('Street, City, State/Province, Postal Code')
    )
    
    contact_person = models.CharField(
        max_length=100,
        verbose_name=_('Primary Contact Person'),
        help_text=_('Name of the authorized representative')
    )
    
    phone_number = models.CharField(
        max_length=15,
        verbose_name=_('Contact Number'),
        validators=[
            RegexValidator(
                regex='^\+?[0-9]{8,15}$',
                message=_('Enter a valid phone number (8-15 digits, optional +)')
            )
        ]
    )
    
    proof_document = models.FileField(
        upload_to='ngo_documents/%Y/%m/%d/',
        verbose_name=_('Registration Proof'),
        help_text=_('Upload scanned copy of registration certificate (PDF or image)'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'],
                message=_('Only PDF and image files are allowed')
            )
        ]
    )
    
    verified = models.BooleanField(
        default=False,
        verbose_name=_('Verification Status'),
        help_text=_('Designates whether this NGO has been verified by admin')
    )
    
    date_registered = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Registration Date')
    )

    class Meta:
        verbose_name = _('NGO Profile')
        verbose_name_plural = _('NGO Profiles')
        ordering = ['-date_registered']
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['organization_name']),
        ]

    def __str__(self):
        return f"{self.organization_name} ({self.registration_number})"

    def clean(self):
        """Additional model-wide validation"""
        super().clean()
        if not self.proof_document:
            raise ValidationError(_('Proof document is required'))
        if len(self.phone_number) < 8:
            raise ValidationError(_('Phone number too short'))
        




        from django.db import models
from django.conf import settings
from django.utils import timezone

class FoodRequest(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('collected', 'Collected')
    ]
    
    food_listing = models.ForeignKey('FoodListing', on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Request for {self.food_listing} by {self.requester.username}"

