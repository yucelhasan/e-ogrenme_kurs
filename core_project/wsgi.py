import os
from django.core.wsgi import get_wsgi_application

# Proje adının 'core_project' olduğundan emin ol
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')

application = get_wsgi_application()