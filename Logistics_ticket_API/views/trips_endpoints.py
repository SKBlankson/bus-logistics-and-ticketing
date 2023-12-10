import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers
from datetime import *
# import asyncio


# TODO how do you get the system to automatically create tomorrows trips?

@api_view(['POST'])
def create_semester_trip(request) -> HttpResponse:
    """
    Creates a trip for the semester
    :return: Returns an HttpResponse indicating failure or
    success of trip creation
    """
    # Get json data
    rawJson = request.body.decode('utf-8')
    trip_data = json.loads(rawJson)

    # Get drive and bus details
    assigned_bus = trip_data.get('assigned_bus')
    assigned_driver = trip_data.get('assigned_driver')
    print(assigned_bus, assigned_driver)

    # Check that assigned driver exists
    validation = helpers.check_driver_exists(request, assigned_driver)
    if validation == False:
        return HttpResponse(content='The assigned driver does not exist', status=400)

    # Check that the vehicle exists
    validation = helpers.check_vehicle_exists(request, assigned_bus)
    if validation == False:
        return HttpResponse(content='The assigned vehicle does not exist', status=400)

    # Get request fields
    title = trip_data.get('title')
    pickup_location = trip_data.get('pickup_location').upper()
    departure_time = trip_data.get('departure_time')
    final_destination = trip_data.get('final_destination').upper()
    arrival_time = trip_data.get('arrival_time')
    assigned_bus = trip_data.get('assigned_bus')
    assigned_driver = trip_data.get('assigned_driver')
    stops = trip_data.get('stops')
    time_period = trip_data.get('time_period').upper()
    full_cost = trip_data.get('full_trip_cost')
    start_date = trip_data.get('start_date')
    end_date = trip_data.get('end_date')

    #### Put stops and destinations in the database ####
    start_end_stops = []
    start_end_stops.append(pickup_location)
    start_end_stops.append(final_destination)

    # Put stops in Stops table
    for stop in stops:
        # Check if stop in database
        stop_check = helpers.check_stop_in_db(stop.get('stop_name'))
        if stop_check == False:
            # If not in database, add stop to database
            new_stop = Stops(stop_id = stop.get('stop_name').upper(),
                             stop_name = stop.get('stop_name').upper(),
                             cost = stop.get('cost'))
            new_stop.save()
            print("Stop created!")

    # Put pick up and drop off locations in Stops table
    for stop in start_end_stops:
        # Check if stop in database
        stop_check = helpers.check_stop_in_db(stop)
        if stop_check == False:
            # If not in database, add stop to database
            new_stop = Stops(stop_id=stop,
                             stop_name=stop,
                             cost = full_cost)
            new_stop.save()
            print("Stop created!")


    # Get reference to needed objects
    driver_ref = Driver.objects.get(employee_id = assigned_driver)
    bus_ref = Vehicles.objects.get(license_plate = assigned_bus)
    pickup_ref = Stops.objects.get(stop_id = pickup_location)
    final_dest_ref = Stops.objects.get(stop_id = final_destination)


    # Create and save new semester  schedule object
    new_sem_trip = SemesterSchedule(
        title = title,
        pickup_location = pickup_ref,
        departure_time = departure_time,
        final_destination = final_dest_ref,
        arrival_time = arrival_time,
        assigned_driver = driver_ref,
        assigned_vehicle = bus_ref,
        time_period = time_period,
        start_date = start_date,
        end_date = end_date
    )
    new_sem_trip.save()

    # Create decomposed entries and save
    try:
        print(len(stops))
        # Decomposed middle stops
        for stop in stops:
            sem_sched_stop = SemesterScheduleStop(stop_id =stop.get('stop_name').upper(),
                                                  schedule_id=new_sem_trip.schedule_id,
                                                  departure_time = stop.get('departure_time'),
                                                  arrival_time = stop.get('arrival_time'))
            print("created decomposition!")
            sem_sched_stop.save()
         # Decomposed startand end stops
        for stop in start_end_stops:
            sem_sched_stop = SemesterScheduleStop(stop_id = stop.upper(),
                                                  schedule_id = new_sem_trip.schedule_id,
                                                  departure_time = departure_time,
                                                  arrival_time = arrival_time)
            print("created decomposition!")
            sem_sched_stop.save()

    except Exception as e:
        print(e)

    # TODO remember to create a trigger event for this
    # helpers.create_daily_trips()

    return HttpResponse(content = "Schedule created", status =200)



def edit_semester_trip(request) -> HttpResponse:
    """
    Edits a specific trip on the semester schedule
    :param request:
    :return:
    """
    return

def delete_semester_trip(request) -> HttpResponse:
    return

@api_view(['GET'])
def get_todays_trips(request) -> JsonResponse | HttpResponse:
    """
    Gets the available trips for the current date
    :param request:
    :return:
    """
    trips = []
    current_date = str(datetime.now().date())
    # if current_date.weekday() == 5 or current_date.weekday() == 6:
    #     return

    # Query for today's trips
    todays_trips = Trip.objects.filter(trip_date=current_date)
    for trip in todays_trips:
        # Get bus and driver details
        driver_name = f"{str(trip.assigned_driver.employee.f_name)} " \
                      f"{str(trip.assigned_driver.employee.l_name)}"
        license_plate = trip.assigned_vehicle.license_plate
        bus_description = trip.assigned_vehicle.descriptive_name

        # Get stops and cost
        starting_location = str(trip.schedule.pickup_location.stop_name)
        final_destination = str(trip.schedule.final_destination.stop_name)
        schedule_id = str(trip.schedule.schedule_id)
        print(schedule_id + "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        stops = []

        # Stops query
        try:
            stop_list = SemesterScheduleStop.objects.filter(schedule__schedule_id=schedule_id)
        except Exception as e:
            print(e)
            return

        for stop in stop_list:
            stops.append({
                "stop_name":stop.stop.stop_name,
                "stop_cost":stop.stop.cost
            })

        data = {
            "trip_date":trip.trip_date,
            "assigned_driver":driver_name,
            "starting_location":starting_location,
            "final_destination":final_destination,
            "license_plate":license_plate,
            "bus_description":bus_description,
            "stop":stops
        }
        trips.append(data)

        return JsonResponse({"Trips":trips},status=200)



    return

def get_trips_in_date_range() -> JsonResponse | HttpResponse:
    return

def edit_trip(request) -> HttpResponse:
    return

def delete_trip() -> HttpResponse:
    return

def book_trip():
    return







