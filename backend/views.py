# Django imports
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db.models import F, Prefetch
from django.db.models.functions import ExtractYear
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page

# Third-party imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from matplotlib import pyplot as plt
import io
import base64
from django.contrib.gis.geos import GEOSException
import logging

# Local imports
from .serializers import DeliveryLocationSerializer, AgeGroupSerializer
from .models import User, DeliveryLocation



logger = logging.getLogger(__name__)

# Lazy import for matplotlib
def lazy_import_matplotlib():
    import matplotlib
    matplotlib.use('agg')
    
class AgeGroupDistribution(APIView):
    def get(self, request):
        try:
            lazy_import_matplotlib()
            # Define age group categories
            age_groups = {
                '1-20': (1, 20),
                '21-40': (21, 40),
                '41-60': (41, 60),
                '61+': (61, 200),
            }

            # Retrieve ages of customers (non-staff users) from the database
            customer_ages = User.objects.filter(is_staff=True).annotate(
                birth_year=ExtractYear('birth_date')
            ).annotate(
                age=2024 - F('birth_year')
            ).values_list('age', flat=True)

            # Calculate distribution of customers across different age groups
            age_group_distribution = {group: 0 for group in age_groups.keys()}
            for age in customer_ages:
                for group, (start, end) in age_groups.items():
                    if start and end and start <= age <= end:
                        age_group_distribution[group] += 1

            # Create Matplotlib bar chart
            labels = list(age_groups.keys())  # Use age group keys as labels
            counts = list(age_group_distribution.values())

            fig, ax = plt.subplots()
            ax.bar(labels, counts, color='skyblue')
            ax.set_xlabel('Age Group')
            ax.set_ylabel('Count')
            ax.set_title('Age Group Distribution')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()

            # Save figure as PNG image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()

            # Serialize data
            serializer = AgeGroupSerializer(
                [{'age_group': group, 'count': count} 
                 for group, count in age_group_distribution.items()],
                many=True
            )
            return Response({'data': serializer.data, 'image': image_base64})

        except User.DoesNotExist:
            return Response({"error": "No user found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response({"error": "An error occurred while processing the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def user_login(request):
    if request.user.is_authenticated:
        return redirect('delivery-location-list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username is None or password is None:
            messages.error(request, 'Username and password are required.')
            return redirect('/')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other page
            return redirect('delivery-location-list')
        else:
            print("Invalid")
            # Invalid login, display an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('/')
    
    return render(request, 'backend/login.html')


@login_required
@require_POST
def save_delivery_location(request):
    try:
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Create DeliveryLocation object
        delivery_location = DeliveryLocation.objects.create(
            user=User.objects.get(id=request.user.id),
            address=address,
            point=f'POINT({longitude} {latitude})'  # Assuming you're using a PointField for 'point'
        )
        return JsonResponse({'message': 'Delivery location saved successfully'})
    
    except GEOSException as e:
        error_message = 'An error occurred while saving the delivery location.'
        logger.error(f'{error_message} Error: {e}')
        return JsonResponse({'error': error_message}, status=500)  # Internal Server Error
    except User.DoesNotExist:
        error_message = 'User does not exist.'
        logger.error(error_message)
        return JsonResponse({'error': error_message}, status=404)  # Not Found
    except Exception as e:
        error_message = 'An unexpected error occurred.'
        logger.error(f'{error_message} Error: {e}')
        return JsonResponse({'error': error_message}, status=500)  # Internal Server Error

#@cache_page(60 * 15)  # Cache the page for 15 minutes
@login_required
def delivery_location_list(request):
    try:
        user = User.objects.prefetch_related(Prefetch('user_delivery_locations')).get(id=request.user.id)
        delivery_locations = user.user_delivery_locations.all()
        delivery_locations_json = serialize('geojson', delivery_locations)    
        context = {
            'delivery_locations_json': delivery_locations_json,
            'user': user
        }
        return render(request, 'backend/delivery_location_map.html', context)
    except User.DoesNotExist:
        error_message = 'User does not exist.'
        return JsonResponse({'error': error_message}, status=404)  # Not Found
    except Exception as e:
        error_message = 'An unexpected error occurred.'
        return HttpResponseServerError(error_message)


class DeliveryLocationAPI(APIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10  # Set the number of items per page
    
    # @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    def get(self, request):
        try:
            delivery_locations = DeliveryLocation.objects.all().order_by('-id')
            # Pagination
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(delivery_locations, request)
            
            # Serializing to GeoJSON
            geojson_data = serialize('geojson', result_page)
            # serializer = DeliveryLocationSerializer(result_page, many=True)
            
            response_data = {
                "data": geojson_data,
                "total_pages": paginator.page.paginator.num_pages,  # Total number of pages
                "total_items": paginator.page.paginator.count,     # Total count of items
                "message": "Delivery locations retrieved successfully.",
                "next": paginator.get_next_link()  # Next page URL
            }
            return Response(response_data)
        
        except DeliveryLocation.DoesNotExist:
            return Response({"error": "No delivery locations found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": "An error occurred while retrieving delivery locations."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required
def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')  # Redirect to the home page after logout