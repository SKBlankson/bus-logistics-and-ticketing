from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers

@api_view(['POST'])
def add_new_vehicle(request) -> HttpResponse:
    """
    Adds a new vehicle to the fleet
    :param request: Request containing vehicle type and details
    :return: Returns an HttpResponse indicating success or failure of resource
    creation
    """

    # Check vehicle does not exist


    return

def edit_vehicle_details(request) -> HttpResponse:
    return

def assign_driver_to_vehicle(request) -> HttpResponse:
    return

def get_expiring_vehicle_permits(request) -> JsonResponse | HttpResponse:
    return

def get_expiring_drivers_licenses() -> JsonResponse | HttpResponse:
    return


