from django.urls import path,include
from contacto.views import ClienteLeadView
from rest_framework import routers

cliente_lead_router = routers.DefaultRouter()

cliente_lead_router.register(r"contacto",ClienteLeadView)
urlpatterns = [
    path('',include(cliente_lead_router.urls)),

]