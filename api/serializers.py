from rest_framework import serializers
from audits.models import *

class AuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audit
        fields = ('date','tauxRespect','tauxMin', 'zone')

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ('description', 'photoStandard','date_de_creation','zone','valstandard','categorie')

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('probleme', 'cause','actionAfaire','delai','tauxEfficacite','planAction')

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('nom', 'responsable')

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ('nom','prenom','numeroTel','email', 'photo')

class planActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAction
        fields = ('audit')