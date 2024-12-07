from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Creates a one-to-one relationship with the User model
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # Profile image field with a default value

    def __str__(self):
        return f'{self.user.username} Profile'

    # You can add a method to handle image resizing if required in the future
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
