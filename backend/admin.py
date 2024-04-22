from django.contrib import admin
from django.contrib.gis import forms
from leaflet.admin import LeafletGeoAdmin
from backend.models import DeliveryLocation, User

admin.site.register(User)

class DeliveryLocationAdminForm(forms.ModelForm):
    
    class Meta:
        model = DeliveryLocation
        fields = '__all__'

class DeliveryLocationAdmin(LeafletGeoAdmin):  # Extend LeafletGeoAdmin
    form = DeliveryLocationAdminForm

admin.site.register(DeliveryLocation, DeliveryLocationAdmin)
