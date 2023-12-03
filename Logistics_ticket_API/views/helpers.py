from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers


def check_driver_fields(request):
    """
    Checks a request to ensure that all the required fields and data are present
    :param request: Request containing the drivers details
    :return: Returns a tuple(bool,HttpResponse)
    """
    # Check that driver request has all required fields and does not contain null
    required_fields = ['employee_id','f_name','l_name',
                      'drivers_license_number','license_expiry_date','momo_number']
    request_fields =  request.query_params.keys()
    for field in required_fields:
        if field not in request_fields:
            return [False, HttpResponse(content=f"The {field} field is not present in your request."
                                                , status=400)]
        if request.query_params.get(field) == '':
            return [False, HttpResponse(content =f"The {field} field contains an empty string."
                                                , status=400)]


    return [True]

def check_driver_exists(request):
    """
    Checks if a dri
    :param request:
    :return:
    """
    driver_id = request.query_params.get("employee_id")
    try:
       Driver.objects.get(employee__employee_id=driver_id)
    except:
        return False

    return True
