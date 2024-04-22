from django.urls import path, include
from rest_framework import routers
from .views import AgeGroupDistribution, DeliveryLocationAPI, \
    delivery_location_list, logout_user, save_delivery_location, user_login
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Define schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="delivery-locations",
        default_version='v1',
        description="delivery-locations",
        terms_of_service="#",
        contact=openapi.Contact(email="contact@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

# Define urlpatterns
urlpatterns = [
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Regular views
    path('', user_login, name='login'),
    path('delivery-location-list', delivery_location_list, name='delivery-location-list'),
    path('save-delivery-location/', save_delivery_location, name='save_delivery_location'),
    #####

    # API URLs
    path('api/v1/age-group-distribution/', AgeGroupDistribution.as_view(), name='age_group_distribution'),
    path('api/v1/delivery-locations/', DeliveryLocationAPI.as_view(), name='delivery_locations_api'),
    path('logout/', logout_user, name='logout'),

]