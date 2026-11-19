# app_formulario

Modo de desarrollo:

    1- Ejecutar en desarrollo Django
        python manage.py runserver
    2- Ejecutar celery para un solo proceso en Windows:
        celery -A app_seguros worker -E -l info --pool=solo
    3- Ejecutar flower:
        celery -A app_seguros.celery_app flower --basic_auth=admin:12345678
    4- Ejecutar Beat:
        celery -A app_seguros beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    5- Ejecutar frontend:
        pnpm dev