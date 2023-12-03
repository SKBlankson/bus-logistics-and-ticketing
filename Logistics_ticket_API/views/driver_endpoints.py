from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers


# API Endpoints


@api_view(['GET'])
def get_driver(request) -> HttpResponse | JsonResponse :
    """Takes driver id and returns driver details

    :param request: containing driver ID
    :return: Returns a JSONResponse with driver details or
        HTTPResponse with status code
    """
    driver_id = request.query_params.get("employee_id")

    # Check that driver does exists
    if helpers.check_driver_exists(request) == False:
        return HttpResponse(content=f"The driver does not exists", status=404)

    query = Driver.objects.get(employee__employee_id=driver_id)
    data = {
        'employee_id':query.employee.employee_id,
        'driver_fname':query.employee.f_name,
        'driver_lname':query.employee.l_name,
        'license_id':query.drivers_license_number,
        'license_expirey':query.license_expiry_date
    }
    driver_details = data

    return JsonResponse({'Drivers': driver_details}, safe=False, status= 200)


@api_view(['GET'])
def get_all_drivers(request) -> HttpResponse | JsonResponse :
    """Returns details for all registered drivers if employee_id field = 'all'

    :param request: Request object
    :return: HttpResponse or JsonResponse object
    """
    driver_list = []

    if request.query_params.get("employee_id") == 'all':
        try:
            query = Driver.objects.all()
            for driver in query:
                data = {
                    'employee_id': driver.employee.employee_id,
                    'driver_fname': driver.employee.f_name,
                    'driver_lname': driver.employee.l_name,
                    'license_id': driver.drivers_license_number,
                    'license_expirey': driver.license_expiry_date
                }
                driver_list.append(data)
        except:
            return HttpResponse(content='An error occurred on the server', status=500)

    return JsonResponse({'Drivers': driver_list}, status=200)

@api_view(['POST'])
def create_new_driver(request) -> HttpResponse:
    """
    Creates a new driver in employee table and the driver table

    :param request: request object containing details for the driver
    :return: HttpResponse indicating success or failure to create resource
    """

    # Check that driver does not exist
    if helpers.check_driver_exists(request) == True:
        return HttpResponse(content=f"The driver already exists", status=400)

    # Check that request has all required fields and does not contain null values
    validation = helpers.check_driver_fields(request)
    if validation[0] == False:
        return validation[1]

    # Store request data
    employee_id_in = request.query_params.get('employee_id')
    f_name_in = request.query_params.get('f_name')
    l_name_in = request.query_params.get('l_name')
    license_number_in = request.query_params.get('drivers_license_number')
    exp_date_in = request.query_params.get('license_expiry_date')
    momo_number_in = request.query_params.get('momo_number')

    try:
        # Create entry in AshesiEmployee table
        new_employee = AshesiEmployee(employee_id = employee_id_in,
                                      f_name = f_name_in,
                                      l_name = l_name_in,
                                      momo_number = momo_number_in)
        new_employee.save()

        # Create entry in Drivers table
        new_driver = Driver(employee = new_employee,
                            drivers_license_number = license_number_in,
                            license_expiry_date = exp_date_in)
        new_driver.save()
    except Exception as e:
        print(e)
        return HttpResponse(content="An error occured when creating the record", status=500)

    return HttpResponse(content=f"Employee {employee_id_in} created", status=201)


@api_view(['PUT'])
def update_driver_details(request) -> HttpResponse:
    """
    Updates the details for an existing driver

    :param request: Request containing the driver id and driver details to be updated.
    Should still include all driver fields
    :return: HttpResponse indicating success or failure to update resource
    """

    # Check that driver exists
    if helpers.check_driver_exists(request) == False:
        return HttpResponse(content=f"The driver does not exists", status=404)

    # Check that driver request has all required fields and does not contain null values
    validation = helpers.check_driver_fields(request)
    if validation[0] == False:
        return validation[1]

    # Store request data
    employee_id_in = request.query_params.get('employee_id')
    f_name_in = request.query_params.get('f_name')
    l_name_in = request.query_params.get('l_name')
    license_number_in = request.query_params.get('drivers_license_number')
    exp_date_in = request.query_params.get('license_expiry_date')
    momo_number_in = request.query_params.get('momo_number')

    #Get driver refrence and update all fields
    driver = Driver.objects.get(employee__employee_id=employee_id_in)
    driver.employee.f_name = f_name_in
    driver.employee.l_name = l_name_in
    driver.drivers_license_number = license_number_in
    driver.license_expiry_date = exp_date_in
    driver.employee.momo_number = momo_number_in

    # Save
    driver.save()
    driver.employee.save()
    print(driver.employee.l_name)

    return HttpResponse(content='Driver details updated', status=200)


@api_view(['DELETE'])
def delete_driver(request) -> HttpResponse:
    """
    Deletes a specific driver from the database

    :param request: Request containing drivers Id
    :return: HttpResponse indicating success or failure to delete resource
    """

    # Check that driver exists
    if helpers.check_driver_exists(request) == False:
        return HttpResponse(content=f"The driver does not exists", status=404)

    driver_id = request.query_params.get('employee_id')

    # Get and delete driver
    driver = Driver.objects.get(employee__employee_id=driver_id)
    # TODO should the driver be deleted from main employees table
    # driver.employee.delete()
    driver.delete()

    # Check that driver no longer exists
    if helpers.check_driver_exists(request) == False:
        return HttpResponse(content=f"The driver has been deleted", status=200)
    else:
        return HttpResponse(content=f"An error occured when deleting the record",
                            status= 500)




