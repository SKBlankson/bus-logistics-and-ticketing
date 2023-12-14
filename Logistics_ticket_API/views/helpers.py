import os

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
# from . import helpers
import requests
import hashlib
from datetime import *
import os


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

def check_email_exists(email):
    """
    Checks if a driver exists
    :param request:
    :return:
    """
    # Check by ID first
    try:
       AshesiEmployee.objects.get(email=email)
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



def custom_hash(input_string):

    hash_object = hashlib.sha256(input_string.encode())


    hex_digest = hash_object.hexdigest()

    # Take the first 10 characters of the hash and convert them to an integer
    short_hash = int(hex_digest[:10], 16)

    return short_hash

def time_plus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()


def pay_for_ticket():
    # import requests
    # load_dotenv()
    url = "https://paybox.com.co/pay"

    payload = {'order_id': '123456',
               'currency': 'GHS',
               'amount': '1.0',
               'mode': 'Test',
               'mobile_network': 'AirtelTigo',
               'voucher_code': '2314',
               'mobile_number': '+233556207957',
               # 'payload': '{"key":"data"}',
               'payerName': 'John Doe',
               'payerPhone': '+233',
               'payerEmail': 'samuel.blankson@ashesi.edu.gh',
               'customer_id': 'c-12345',
               'callback_url': ''}
    files = [

    ]
    headers = {
        'Authorization': os.getenv('payment_token'),
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

# pay_for_ticket()

















