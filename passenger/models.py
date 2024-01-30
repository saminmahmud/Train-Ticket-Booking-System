from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name='account', on_delete=models.CASCADE)
    nid = models.CharField(unique=True, max_length=6, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    def __str__(self):
        return str(self.user.username)
    
class Profile(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null= True, blank= True)

    def __str__(self):
        return f"Profile: {self.account}"
    