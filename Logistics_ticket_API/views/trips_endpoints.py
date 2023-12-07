from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers


# TODO how do you get the system to automatically create tomorrows trips?

@api_view(['POST'])
def create_semester_trip(request) -> HttpResponse:
    """
    Creates a trip for the semester
    :return: Returns an HttpResponse indicating failure or
    success of trip creation
    """
    # Check that assigned driver exists
    validation = helpers.check_driver_exists(request)
    if validation == False:
        return HttpResponse(content='The assigned driver does not exist', status=400)

    # Check that the vehicle exists
    validation = helpers.check_vehicle_exists(request)
    if validation == False:
        return HttpResponse(content='The assigned vehicle does not exist', status=400)

    # Get request fields
    day_of_week = request.query_params.get('day_of_week')
    pickup_location = request.query_params.get('pickup_location').upper()
    departure_time = request.query_params.get('departure_time')
    final_destination = request.query_params.get('final_destination')
    arrival_time = request.query_params.get('arrival_time')
    assigned_bus = request.query_params.get('assigned_bus')
    assigned_driver = request.query_params.get('assigned_driver')
    stops = request.query_params.get('stops')
    start_end_stops = []


    # Put stops and destinations in the database
    start_end_stops.append(pickup_location)
    start_end_stops.append(final_destination)

    # Put stops in Stops table
    for stop in stops:
        # Check if stop in database
        stop_check = helpers.check_stop_in_db(stop.get('stop_name'))
        if stop_check == False:
            # If not in database, add stop to database
            new_stop = Stops(stop_id = stop.get('stop_name'),
                             stop_name = stop.get('stop_name'))
            new_stop.save()

    # Put start and end locations in Stops tbale
    for stop in start_end_stops:
        # Check if stop in database
        stop_check = helpers.check_stop_in_db(stop)
        if stop_check == False:
            # If not in database, add stop to database
            new_stop = Stops(stop_id=stop,
                             stop_name=stop)
            new_stop.save()

    # Get reference to driver and vehicle objects
    driver_ref = Driver.objects.get(employee_id = assigned_driver)
    bus_ref = Vehicles.objects.get(license_plate = assigned_bus)

    # Create and save new semester  schedule object
    new_sem_trip = SemesterSchedule(
        day_of_week = day_of_week,
        pickup_location = pickup_location,
        departure_time = departure_time,
        final_destination = final_destination,
        arrival_time = arrival_time,
        assigned_driver = driver_ref,
        assigned_bus = bus_ref
    )
    new_sem_trip.save()

    # Create decomposed entries and save
    for stop in stops:
        sem_sched_stop = SemesterScheduleStop(stop_id =stop.get('stop_name'),
                                              departure_time = stop.get('departure_time'),
                                              arrival_time = stop.get('arrival_time'),
                                              schedule_id = new_sem_trip
        )
        sem_sched_stop.save()


    return HttpResponse(content = "Schedule created", status =200)










    return

def edit_semester_trip(request) -> HttpResponse:
    """
    Edits a specific trip on the semester schedule
    :param request:
    :return:
    """
    return

def delete_semester_trip(request) -> HttpResponse:
    return

def get_todays_trips() -> JsonResponse | HttpResponse:
    return

def get_trips_in_date_range() -> JsonResponse | HttpResponse:
    return

def edit_trip(request) -> HttpResponse:
    return

def delete_trip() -> HttpResponse:
    return

def book_trip():
    return







