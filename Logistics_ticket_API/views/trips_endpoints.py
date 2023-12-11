import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import helpers
from datetime import *
# import asyncio


# TODO automatically create tomorrows trips? - ans -> cron job

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_semester_trip(request) -> HttpResponse:
    """
    Creates a trip for the semester
    :return: Returns an HttpResponse indicating failure or
    success of trip creation
    """

    # check if
    # Get json data
    rawJson = request.body.decode('utf-8')
    trip_data = json.loads(rawJson)

    # Get driver and bus details
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


    # Create and save new semester schedule object
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
        # Decomposed start and end stops
        # for stop in start_end_stops:
        #     sem_sched_stop = SemesterScheduleStop(stop_id = stop.upper(),
        #                                           schedule_id = new_sem_trip.schedule_id,
        #                                           departure_time = departure_time,
        #                                           arrival_time = arrival_time)

        # Save pickup location
        sem_sched_stop = SemesterScheduleStop(stop_id=pickup_location.upper(),
                                              schedule_id=new_sem_trip.schedule_id,
                                              departure_time=departure_time,
                                              arrival_time=departure_time)
        sem_sched_stop.save()
        # Save final destination
        sem_sched_stop = SemesterScheduleStop(stop_id=final_destination.upper(),
                                              schedule_id=new_sem_trip.schedule_id,
                                              departure_time=arrival_time,
                                              arrival_time=arrival_time)
        sem_sched_stop.save()

        print("created decomposition!")
            # sem_sched_stop.save()

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

# TODO optimization would be to make this a "rolling file"
@api_view(['GET'])
def get_todays_trips(request) -> JsonResponse | HttpResponse:
    """
    Gets the available trips for the current date
    :param request: if request contains param:mobible,
    :return:
    """
    client = request.query_params.get('client')
    trips = []
    current_date = str(datetime.now().date())
    # if current_date.weekday() == 5 or current_date.weekday() == 6:
    #     return

    # Query for today's trips
    todays_trips = Trip.objects.filter(trip_date=current_date).order_by('schedule__departure_time')
    # exepcted_no_of_trips = todays_trips.count()

    for trip in todays_trips:
        # Get bus and driver details
        driver_name = f"{str(trip.assigned_driver.employee.f_name)} " \
                      f"{str(trip.assigned_driver.employee.l_name)}"
        license_plate = trip.assigned_vehicle.license_plate
        bus_description = trip.assigned_vehicle.descriptive_name

        # Get stops, cost and times
        starting_location = str(trip.schedule.pickup_location.stop_name)
        final_destination = str(trip.schedule.final_destination.stop_name)
        schedule_id = str(trip.schedule.schedule_id)
        departure_time = trip.schedule.departure_time
        stops = []

        # Stops query
        stop_list = SemesterScheduleStop.objects.filter(schedule__schedule_id=schedule_id).order_by('departure_time')


        for stop in stop_list:
            stops.append({
                "stop_name":stop.stop.stop_name,
                "stop_cost":stop.stop.cost,
                "stop_departure_time":stop.departure_time
            })

        data = {
            "trip_date":trip.trip_date,
            "assigned_driver":driver_name,
            "starting_location":starting_location,
            "departure_time":departure_time,
            "final_destination":final_destination,
            "license_plate":license_plate,
            "bus_description":bus_description,
            "stop":stops
        }
        trips.append(data)


    return JsonResponse({"Trips":trips},status=200)




@api_view(['PUT'])
def create_daily_trips(request) -> HttpResponse:
    """
    Creates a daily trip for all trips listed on semester schedule
    """
    try:
        # Create the trips for today
        current_date = datetime.now().date()
        semester_schedule = SemesterSchedule.objects.all()
        todo = SemesterSchedule.objects.all().count()
        completed = 0

        for trip in semester_schedule:
            new_trip = Trip(
                trip_id = str(current_date) + str(completed),
                schedule= trip,
                trip_date=current_date,
                assigned_driver=trip.assigned_driver,
                assigned_vehicle=trip.assigned_vehicle
            )
            new_trip.save()
            completed +=1
    except Exception as e:
        print(e)
        return HttpResponse(content="Failed to create some trips. Consider "
                                    "resetting the trips databse", status=500)

    return HttpResponse(content=f"{str(completed)} out of "
                                f"{str(todo)} trips created")

def get_trips_in_date_range() -> JsonResponse | HttpResponse:
    return

def edit_trip(request) -> HttpResponse:
    return

def delete_trip() -> HttpResponse:
    return

def book_trip():
    return









