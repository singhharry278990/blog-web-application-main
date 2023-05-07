from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.core.validators import RegexValidator
from .helpers import *
from django.contrib.sessions.backends.db import SessionStore





class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)


class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)



class MobileModel(models.Model):

    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators=[mobile_regex],max_length=17, blank=False, null=False )
    otp = models.CharField(max_length=6)

class CustomModel(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    
    is_pass_change = models.BooleanField(default=False)

    