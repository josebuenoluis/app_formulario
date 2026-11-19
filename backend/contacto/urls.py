from django.urls import path,include
from contacto.views import ClienteLeadView
from rest_framework import routers
from users.views import UsersView
cliente_lead_router = routers.DefaultRouter()

cliente_lead_router.register(r"contacto",ClienteLeadView)
urlpatterns = [
    path('',include(cliente_lead_router.urls)),
    path('api/contacto/<slug:slug>/', UsersView.as_view(), name='detalle-vendedor-slug'),

]