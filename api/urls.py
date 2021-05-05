from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *
from . import views

urlpatterns =[
path('audits/', AuditList.as_view()),
path('audits/<int:pk>', AuditDetails.as_view()),
path('audits/<int:pk>/actions/', AuditActionList.as_view()),
path('audits/<int:pk>/zone/',AuditZoneList.as_view()),
path('audits/<int:pk>/zone/responsable', AuditResponsableList.as_view()),

path('actions/',ActionList.as_view()),
path('actions/<int:pk>', ActionDetails.as_view()),

path('zones/',ZoneList.as_view()),
path('zones/<int:pk>',ZoneDetails.as_view()),
path('zones/<int:pk>/responsable/', ZoneResponsableList.as_view()),

path('standards/', StandardAPIView.as_view()),
#path("audits/<int:pk>/actions/", ActionList.as_view(), name="action_list"),




#path('1',views.first),
#path('',Another.as_view()),
]