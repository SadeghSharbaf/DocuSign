from django.db import models
from django.contrib.auth.models import User



class Contract(models.Model):
    creator = models.ForeignKey(User, related_name = "user", on_delete=models.CASCADE)
    recipient_email = models.EmailField(max_length=254)
    recipient_name = models.CharField(max_length=12,default="Unknown")
    envelope_id = models.CharField(max_length=255, blank=True, null= True)
    signing_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"Contract By {self.creator.username} => {self.recipient_email} "
    