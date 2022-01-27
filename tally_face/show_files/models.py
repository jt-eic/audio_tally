from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class ShowPage(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add = True)
    show_data = models.TextField()

    def __str__(self):
        stringdate = str(self.date.isoformat())
        return stringdate

