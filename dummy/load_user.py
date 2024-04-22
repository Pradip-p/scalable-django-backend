import os
import sys
import django
from datetime import date, timedelta
import random
from faker import Faker
from django.db import IntegrityError  # Import IntegrityError

# Adjust the path to the Django project settings file
sys.path.insert(0, os.path.join(sys.path[0], '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from backend.models import User

# Common password for all users
password = 'common_password'

# Faker instance for generating realistic names
fake = Faker()

# Define the range for birth dates (start date and end date)
start_date = date(1970, 1, 1)  # Start date for random generation
end_date = date(2000, 12, 31)   # End date for random generation

# Create 100 users with the same password
for i in range(1, 10000):
    username = f'user{i}'
    email = f'user{i}@example.com'
    
    # Generate random birth date within the specified range
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    
    ph_number = '1234567890'  # Specify the phone number
    
    # Generate random first name and last name
    first_name = fake.first_name()
    last_name = fake.last_name()

    try:
        # Create user object
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            ph_number=ph_number,
            is_staff = True
        )

        # Set password
        user.set_password(password)
        user.save()
        print(f'{first_name} {last_name} is inserted.....')
    except IntegrityError:  # Handle IntegrityError if username already exists
        print(f'Username "{username}" already exists. Generating new username...')
        continue
print("100 users created successfully with the same password and random details!")
