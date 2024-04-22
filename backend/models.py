from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    ph_number = models.CharField(max_length=15,null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['username', 'email']),
        ]
        
    def __str__(self):
        return f'{self.username}'
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
        
class DeliveryLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_delivery_locations")
    address = models.CharField(max_length=200)
    point = gis_models.PointField( blank=True,
                                spatial_index=False,
                                default=Point(0, 0))
    
    class Meta: #Spatial Index
        indexes = [
            models.Index(fields=['point']),
            models.Index(fields=['user']),
        ]
    def __str__(self):
        return self.address