from django.db import models


class Courses(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return "name: {} , description: {}".format(self.name, self.description)