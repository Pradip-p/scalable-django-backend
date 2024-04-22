import os
from dotenv import load_dotenv
load_dotenv()
from .base import *
# Now you can access the MYPROJECT_ENV variable using the os module:
MYPROJECT_ENV = os.getenv("MYPROJECT_ENV")
if os.getenv("MYPROJECT_ENV"):
   from .dev import *
else:
   from .prod import *