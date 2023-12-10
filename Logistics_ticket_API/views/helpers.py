from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers
from datetime import *


def check_driver_fields(request):
    """
    Checks a request to ensure that all the required fields and data are present
    :param request: Request containing the drivers details
    :return: Returns a tuple(bool,HttpResponse)
    """
    # Check that driver request has all required fields and does not contain null
    required_fields = ['f_name','l_name',
                      'drivers_license_number','license_expiry_date','momo_number','address']
    request_fields =  request.data.keys()
    for field in required_fields:
        if field not in request_fields:
            return [False, HttpResponse(content=f"The {field} field is not present in your request."
                                                , status=400)]
        if request.query_params.get(field) == '':
            return [False, HttpResponse(content =f"The {field} field contains an empty string."
                                                , status=400)]


    return [True]



def check_driver_exists(request, driverId = None):
    """
    Checks if a driver exists
    :param request:
    :return:
    """
    # Check by ID first
    if driverId != None:
        try:
            Driver.objects.get(employee__employee_id=driverId)
        except:
            return False

        return True

    # Check via request objt cdrgh
    driver_id = request.query_params.get("employee_id")
    try:
       Driver.objects.get(employee__employee_id=driver_id)
    except:
        return False

    return True

def check_vehicle_exists(request, licenseplate = None):
    """
    Checks if a vehicle exists in the database
    :param request:
    :return:
    """
    # Check by licnese plate first
    if licenseplate != None:
        try:
            Vehicles.objects.get(license_plate=licenseplate)
        except:
            return False

        return True

    vehicle_id = request.query_params.get("license_plate")

    try:
        Vehicles.objects.get(license_plate=vehicle_id)
    except:
        return False

    return True

def check_vehicle_fields(request):
    """
    Checks a request to ensure that all the required fields and data are present
    :param request: Request containing the drivers details
    :return: Returns a tuple(bool,HttpResponse)
    """
    # Check that driver request has all required fields and does not contain null
    required_fields = ['vehicle_type','capacity','descriptive_name',
                      'make','model','permit_issuer','permit_issue_date','permit_expiry_date',
                       'employee_id']
    request_fields = request.data.keys()

    for field in required_fields:
        if field not in request_fields:
            return [False, HttpResponse(content=f"The {field} field is not present in your request."
                                                , status=400)]
        if request.data.get(field) is None:
            return [False, HttpResponse(content =f"The {field} field contains an empty string."
                                                , status=400)]



    return [True]

def check_stop_in_db(stop_name : str):
    """
    Checks if a stop is in the database
    :param request:
    :return:
    """

    try:
        query = Stops.objects.filter(stop_name=stop_name)

        if query.exists():
            return True
        else:
            return False

    except:
        return False

def create_daily_trips():
    """
    Creates the daily trips for the semester excluding weekends
    :return:
    """
    # Create the trips for today
    current_date = datetime.now().date()
    semester_schedule = SemesterSchedule.objects.all()
    count=0

    for trip in semester_schedule:
        new_trip = Trip(
            trip_id = str(trip.start_date) + str(count),
            schedule= trip,
            trip_date=current_date,
            assigned_driver=trip.assigned_driver,
            assigned_vehicle=trip.assigned_vehicle
        )
        new_trip.save()

    return















