from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from checks.models import Item
from .serializers import ItemSerializer
import pdfkit


class CashMachineView(APIView):
    def post(self, request):
        pass
