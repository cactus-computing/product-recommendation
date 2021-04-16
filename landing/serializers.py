from rest_framework import serializers
from landing.models import Contact
import re
from rest_framework.response import Response
#from store.models import Store


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "company_url")