from django.db import models


class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name
