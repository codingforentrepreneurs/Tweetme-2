import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many users can many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    
    # def __str__(self):
    #     return self.content
    
    class Meta:
        ordering = ['-id']
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }