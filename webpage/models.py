from django.db import models
from django.utils import timezone

class Reservation(models.Model):
    total_reservation = 0
    reservation_number = models.IntegerField(default = -1)
    customer_name = models.TextField(default = "")
    customer_email = models.TextField(default = "")
    phone_number = models.TextField(default = "")
    number_of_guests = models.IntegerField(default = -1)
    message = models.TextField(default = "")
    reservation_datetime =  models.DateTimeField(default = timezone.now)
    reserved_datetime = models.DateTimeField(default = timezone.now)
    cancelled = models.BooleanField(default = False)

    def __str__(self):
        return str(self.reservation_number)

    def str_reservation_date_and_time(self):
        year = self.reservation_datetime.year
        month = self.reservation_datetime.month
        day = self.reservation_datetime.day
        hour = self.reservation_datetime.hour
        minute = self.reservation_datetime.minute

        all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = all_months[month-1]
        if len(str(minute)) == 1:
            minute = "0"+str(minute)

        return str(month) + " "+str(day)+", "+str(year)+" "+str(hour)+":"+str(minute)

    def str_reserved_datetime (self):
        year = self.reserved_datetime.year
        month = self.reserved_datetime.month
        day = self.reserved_datetime.day
        hour = self.reserved_datetime.hour
        minute = self.reserved_datetime.minute

        all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = all_months[month-1]
        if len(str(minute)) == 1:
            minute = "0"+str(minute)

        return str(month) + " "+str(day)+", "+str(year)+" "+str(hour)+":"+str(minute)
