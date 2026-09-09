#!/usr/bin/env bash
# Render Build Command: bash build.sh
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput || true
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
U = get_user_model()
U.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).update(role='admin')
" || true
