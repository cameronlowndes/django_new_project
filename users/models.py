from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Creates a one-to-one relationship with the User model
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # Profile image field with a default value

    def __str__(self):
        return f'{self.user.username} Profile'

    # You can add a method to handle image resizing if required in the future
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
