from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers
from datetime import date, timedelta
from django.db.models import Q

@api_view(['POST'])
def add_new_vehicle(request) -> HttpResponse:
    """
    Adds a new vehicle to the fleet
    :param request: Request containing vehicle type and details
    :return: Returns an HttpResponse indicating success or failure of resource
    creation
    """

    # Check vehicle does not exist
    if helpers.check_vehicle_exists(request) == True:
        return HttpResponse(content="Vehicle already exists", status=400)

    # Check that necessary fields are present with no null values
    validation = helpers.check_vehicle_fields(request)
    if validation[0] == False:
        return validation[1]

    # Check that assigned driver exists
    validation = helpers.check_driver_exists(request)
    if validation == False:
        return HttpResponse(content='Driver does not exist',status=400)

    # Get vehicle details
    license_plate_in = request.query_params.get('license_plate')
    vehicle_type_in = request.query_params.get('vehicle_type')
    capacity_in = request.query_params.get('capacity')
    descriptive_name_in = request.query_params.get('descriptive_name')
    make_in = request.query_params.get('make')
    model_in = request.query_params.get('model')
    permit_issuer_in = request.query_params.get('permit_issuer')
    permit_issue_date_in = request.query_params.get('permit_issue_date')
    permit_expiry_date_in = request.query_params.get('permit_expiry_date')
    assigned_driver_in = request.query_params.get('employee_id')
    driver_ref = AshesiEmployee.objects.get(employee_id=assigned_driver_in)
    last_maintained = request.query_params.get('last_maintenance_date')
    next_maintenance = request.query_params.get('next_maintenance_date')


    # Create new vehicle
    new_vehicle = Vehicles(license_plate = license_plate_in,
                           vehicle_type = vehicle_type_in,
                           capacity = capacity_in,
                           descriptive_name = descriptive_name_in,
                           make = make_in,
                           model = model_in,
                           permit_issuer = permit_issuer_in,
                           permit_issue_date = permit_issue_date_in,
                           permit_expiry_date = permit_expiry_date_in,
                           assigned_driver = driver_ref,
                           last_maintenance_date = last_maintained,
                           next_maintenance_date = next_maintenance
                           )
    new_vehicle.save()

    # Check if vehicle exists
    if helpers.check_vehicle_exists(request) == True:
        return HttpResponse(content='The vehicle has been created', status = 200)
    else:
        return HttpResponse(content='An error occured when creating the entry',
                            status = 500)

@api_view(['PATCH'])
def edit_vehicle_details(request) -> HttpResponse:
    """
    Edits details of an existing vehicle
    :param request: Request containing vehicle details
    :return: Returns an HttpResponse indicating success or failure to edit the details
    """

    # Check vehicle exists
    if helpers.check_vehicle_exists(request) == False:
        return HttpResponse(content="Vehicle does not exists", status=404)

    # Check that necessary fields are present with no null values
    validation = helpers.check_vehicle_fields(request)
    if validation[0] == False:
        return validation[1]

    # Check that assigned driver exists
    validation = helpers.check_driver_exists(request)
    if validation == False:
        return HttpResponse(content='Driver does not exist', status=400)

    # TODO implement to allow license plate changes
    # Get vehicle details
    license_plate_in = request.query_params.get('license_plate')
    vehicle_type_in = request.query_params.get('vehicle_type')
    capacity_in = request.query_params.get('capacity')
    descriptive_name_in = request.query_params.get('descriptive_name')
    make_in = request.query_params.get('make')
    model_in = request.query_params.get('model')
    permit_issuer_in = request.query_params.get('permit_issuer')
    permit_issue_date_in = request.query_params.get('permit_issue_date')
    permit_expiry_date_in = request.query_params.get('permit_expiry_date')
    assigned_driver_in = request.query_params.get('employee_id')
    driver_ref = AshesiEmployee.objects.get(employee_id=assigned_driver_in)

    # Get vehicle reference and update values
    vehicle_ref = Vehicles.objects.get(license_plate = license_plate_in)
    vehicle_ref.license_plate = license_plate_in
    vehicle_ref.vehicle_type = vehicle_type_in
    vehicle_ref.capacity = capacity_in
    vehicle_ref.descriptive_name = descriptive_name_in
    vehicle_ref.make = make_in
    vehicle_ref.model = model_in
    vehicle_ref.permit_issuer = permit_issuer_in
    vehicle_ref.permit_issue_date = permit_issue_date_in
    vehicle_ref.permit_expiry_date = permit_expiry_date_in
    vehicle_ref.assigned_driver = driver_ref
    vehicle_ref.save()


    return HttpResponse(content="Changes sucessfully made", status=200)

@api_view(['GET'])
def get_all_busses(request) -> JsonResponse | HttpResponse:
    """
    returns all busses in the db
    :param request: Request to get all buss
    :return: Returns Json object with all busses or HttpResponse indicating some issue
    """
    # get list of all buses
    try:
        query = Vehicles.objects.filter(vehicle_type='Bus')
        bus_details_list = []
        for bus in query:
            serialized_obj = VehiclesSerializer(bus)
            bus_details_list.append(serialized_obj.data)
    except:
        HttpResponse(content='An error occured when fetching the list.'
                             'There might be no busses in the database', status=500)

    print(bus_details_list)
    return JsonResponse({'bus_list':bus_details_list},status=200)


@api_view(['GET'])
def  get_all_private_cars(request) -> JsonResponse | HttpResponse:
    """
    Gets and returns all busses in the db
    :param request: Request to get all buss
    :return: Returns Json object with all busses or HttpResponse indicating some issue
    """
    # get list of all buses
    try:
        query = Vehicles.objects.filter(vehicle_type='Private Vehicle')
        private_vehicle_list = []
        for bus in query:
            serialized_obj = VehiclesSerializer(bus)
            private_vehicle_list.append(serialized_obj.data)
    except:
        HttpResponse(content='An error occured when fetching the list.'
                             'There might be no buses in the database', status=500)

    return JsonResponse({'private_list':private_vehicle_list},status=200)

@api_view(['GET'])
def get_vehicle(request) -> JsonResponse | HttpResponse:
    """
    Gets details for a specifc vehicle
    :param request: Request containing license_plate of desired vehicle
    :return: Returns a Json object containing details for a specific
    """
    vehicle_id = request.query_params.get("license_plate")

    # Check that the vehicle exists
    validation = helpers.check_vehicle_exists(request)
    if validation == False:
        return HttpResponse(content='Vehicle does not exist', status=400)

    # Get vehicle details
    vehicle_details = Vehicles.objects.get(license_plate=vehicle_id)
    serialized_data = VehiclesSerializer(vehicle_details).data

    return JsonResponse({'Vehicle_data':serialized_data}, status=200)

@api_view(['DELETE'])
def delete_vehicle(request) -> HttpResponse:
    """
    Deletes a specified vehicle from the db
    :param request: Request containing license plate
    :return: Returns HttpResponse indicating failure or success of deletion
    """
    print(request)
    vehicle_id = request.query_params.get('license_plate')

    # Check vehicle exists
    validation = helpers.check_vehicle_exists(request)
    if validation == False:
        return HttpResponse(content='Vehicle does not exist. Try again with'
                                    'valid details', status=400)

    # Delete vehicle
    vehicle_obj = Vehicles.objects.get(license_plate=vehicle_id)
    vehicle_obj.delete()

    # Check vehicle no longer exists
    validation = helpers.check_vehicle_exists(request)
    if validation == False:
        return HttpResponse(content='Vehicle succesfully deleted.', status=200)
    else:
        return HttpResponse(content='An error occurred when deleting the record',
                            status=500)

@api_view(['GET'])
def get_expiring_vehicle_permits(request) -> JsonResponse | HttpResponse:
    """
    Returns a list of vehicles whos permits will expire within 15 days
    :param request:
    :return: Returns an JsonResponse with vehicle details or an HttpResponse
    indicating some error/notice
    """
    present_day = date.today()
    expiration_limit = present_day + timedelta(days=15)
    serialized_data = {}


    # Query to get vehicles with permits expiring 15 days from the present day
    try:
        vehicles_query = Vehicles.objects.filter(
            Q(permit_expiry_date__isnull=False) &
            Q(permit_expiry_date__gte=present_day) &  # Permit expiry date is on or after today
            Q(permit_expiry_date__lte=expiration_limit)  # Permit expiry date is 15 days from today or earlier
        )
    except:
        HttpResponse(content='An error occured when querying the database', status=500)

    # List of vehicles with permits expiring 15 days from the present day
    expiring_permits = list(vehicles_query)
    if len(expiring_permits) == 0:
        return  HttpResponse(content='No vehicle permits expire in the next 15 days', status=200)
        # TODO look into a different status code


    for vehicle in expiring_permits:
        expiry_date = vehicle.permit_expiry_date
        license_plate = vehicle.license_plate
        delta = expiry_date - present_day
        vehicle_type = vehicle.vehicle_type
        formatted_message = f"The {vehicle_type} with license plate {license_plate} expires " \
                            f"on {expiry_date} - {delta.days} Day(s)"
        serialized_data[license_plate] = formatted_message

    return JsonResponse({'Expiring_permits':serialized_data}, status=200)


@api_view(['GET'])
def get_expiring_drivers_licenses(request) -> JsonResponse | HttpResponse:
    """
     Returns a list of drivers whos license will expire within 15 days
     :param request:
     :return: Returns an JsonResponse with driver details or an HttpResponse
     indicating some error/notice
     """
    present_day = date.today()
    expiration_limit = present_day + timedelta(days=15)
    serialized_data = {}

    # Query to get vehicles with permits expiring 15 days from the present day
    try:
        driver_query = Driver.objects.filter(
            Q(license_expiry_date__isnull=False) &
            Q(license_expiry_date__gte=present_day) &  # license expiry date is on or after today
            Q(license_expiry_date__lte=expiration_limit)  # Permit expiry date is 15 days from today or earlier
        )
    except:
        HttpResponse(content='An error occured when querying the database', status=500)

    # List of drivers with licenses expiring 15 days from the present day
    expiring_license = list(driver_query)
    if len(expiring_license) == 0:
        return HttpResponse(content='No drivers license expire in the next 15 days', status=200)
        # TODO look into a different status code

    for driver in expiring_license:
        expiry_date = driver.license_expiry_date
        license_number = driver.drivers_license_number
        f_name = driver.employee.f_name
        l_name = driver.employee.l_name
        delta = expiry_date - present_day

        formatted_message = f"{f_name} {l_name}'s drivers license expires " \
                            f"on {expiry_date} - {delta.days} Day(s). " \
                            f"license number - {license_number}"
        serialized_data[license_number] = formatted_message

    return JsonResponse({'Expiring_license': serialized_data}, status=200)



