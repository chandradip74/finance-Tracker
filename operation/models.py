from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class Transaction(models.Model):
    userid = models.ForeignKey(User, verbose_name=_("userid"), on_delete=models.CASCADE)
    tran_id = models.AutoField(primary_key=True)
    tran_type = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.userid.username} - {self.title}"
