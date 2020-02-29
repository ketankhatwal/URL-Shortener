from django.db import models

class Short(models.Model):
    actual_url = models.CharField(max_length = 1000)
    shortened_url = models.CharField(max_length = 50)

    def __str__(self):
        return self.shortened_url
