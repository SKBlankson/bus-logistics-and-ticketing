from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers


@api_view(['GET'])
def login(request) -> HttpResponse | JsonResponse :
    user_email = request.query_params.get('ashesi_email')