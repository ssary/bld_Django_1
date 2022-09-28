from datetime import datetime, date

from django.db import models

class UserModel(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    email = models.EmailField()
    password = models.CharField(max_length=30)

#    def __str__(self):
#        return 'fname:{} lname:{} birthdate:{} email:{} password:{} '.format(
#            self.first_name, self.last_name, self.birth_date, self.email, self.password
#        )

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def age(self):
        return datetime.now().year - self.birth_date.year

