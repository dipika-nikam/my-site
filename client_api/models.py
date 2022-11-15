from django.db import models
from api.models  import User,Beautician,Service
from datetime import date

class BeauticianAvailabilities(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    beautician_id = models.ForeignKey(Beautician,  on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        if self.start_date== date.today() and self.end_date== date.today():
            return self.beautician_id.first_name
        else:
            return self.beautician_id.first_name
class BeauticianServices(models.Model):
    beautician_id = models.OneToOneField(Beautician,  on_delete = models.CASCADE)
    services_id = models.ManyToManyField(Service,blank=True)

    def __str__(self):
        return str(self.beautician_id)

status = (
    ('Approved', 'Approved'),
    ('Panding', 'Panding'),
    ('Rejected', 'Rejected')
)
class AppointmentModel(models.Model):
    appointment_name = models.CharField(max_length=255)
    beautician_id = models.ForeignKey(BeauticianServices, on_delete = models.CASCADE)
    appointment_service= models.ManyToManyField(Service, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=status,default ='Panding',max_length=255)

    def __str__(self):
        return str(self.appointment_name)

rating = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)
class Ratingmodel(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    beautician_id= models.ForeignKey(Beautician,  on_delete = models.CASCADE)
    rating = models.CharField(choices=rating,max_length=255, default=0)
    review = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.beautician_id)


class Blogmodel(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/blog",blank=True, null=True)
    blog= models.TextField()

    def __str__(self):
        return str(self.title)
