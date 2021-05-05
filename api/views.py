from django.shortcuts import render
from rest_framework import generics, viewsets
from audits.models import *
from .serializers import *
from django.http import HttpResponse
from django.views import View
# Create your views here.

#Les classes des audits
class AuditList(generics.ListCreateAPIView):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

class AuditDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

#afficher les actions d'un audit
class AuditActionList (generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset = PlanAction.objects.filter(audit=self.kwargs["pk"])
        queryset2= Action.objects.all()
        return queryset2    
    serializer_class = ActionSerializer

#afficher la zone d'un audit
class AuditZoneList (generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        #queryset = Zone.objects.filter(audit=self.kwargs["pk"])
        queryset = Audit.objects.filter(self.kwargs["pk"])
        queryset2 = queryset.zone()
        return queryset2    
    serializer_class = ZoneSerializer

def AuditZoneList_view(request,pk):  
    #audit= Audit.objects.get(pk=id)
    #zone= audit.objects.get(zone)
    return HttpResponse(request)
    #def detail(request, album_id):
    #return render(request, 'music/detail.html', {})
    

class AuditResponsableList (generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset = Zone.objects.filter(audit=self.kwargs["pk"])
        queryset2= queryset.filter(responsable=1)
        return queryset2    
    serializer_class = ResponsableSerializer

#les classes des actions
class ActionList(generics.ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

class ActionDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

#les classes des zones
class ZoneList(generics.ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class ZoneDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

#afficher le responsable d'une zone
class ZoneResponsableList (generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset = Responsable.objects.filter(zone=self.kwargs["pk"])
        return queryset    
    serializer_class = ResponsableSerializer

class StandardAPIView(generics.ListAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer






def first(request):
    return HttpResponse('First message from API')

"""class Another (View):
    audits = Audit.objects.all()
    output = f"We have {len(audits)} audits"
    def get(self,request):
        return HttpResponse(self.output)"""