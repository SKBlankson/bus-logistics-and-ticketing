import datetime
import json
from math import fabs
# import auth_endpoints
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import helpers
from datetime import *
from django.utils import timezone
# import asyncio


# TODO automatically create tomorrows trips? - ans -> cron job

@api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
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
    upcoming_trips = []
    future_trips = []
    all_trips = []
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    time_window = 0

    # Query for today's trips
    if client == 'admin':
        todays_trips = Trip.objects.filter(trip_date=current_date).order_by('schedule__departure_time')
    if client == 'mobile':
        todays_trips = Trip.objects.filter(trip_date=current_date, schedule__departure_time__gt=current_time).order_by('schedule__departure_time')

    if not todays_trips.exists():
        return JsonResponse({"message": "No more trips today."})

    count = 0
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
        print(type(departure_time))
        stops = []

        if count == 0 and client == "mobile":
            time_window = departure_time

        # Stops query
        stop_list = SemesterScheduleStop.objects.filter(schedule__schedule_id=schedule_id).order_by('departure_time')

        for stop in stop_list:
            stops.append({
                "stop_name":stop.stop.stop_name,
                "stop_cost":stop.stop.cost,
                "stop_departure_time":stop.departure_time
            })

        # Build trip object
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

        if client == 'mobile':
            # Check if the departure time is within 10 minutes of the time window
            # time_difference = (departure_time - time_window).total_seconds() / 60  # in minutes
            # time_limit = (time_window + timedelta(minutes=10)).time()
            # time_limit =

            print(time_window, departure_time)
            time_window_seconds = time_window.hour * 3600 + time_window.minute * 60 + time_window.second
            departure_time_seconds = departure_time.hour * 3600 + departure_time.minute * 60 + departure_time.second

            # Check if the departure time is within 10 minutes (600 seconds) of the time window
            if departure_time_seconds < (time_window_seconds + 600):
                upcoming_trips.append(data)
            else:
                future_trips.append(data)

        if client == 'admin':
            all_trips.append(data)

        count+=1

    # 'upcoming_trips' contains trips within 10 minutes of the time window,
    # and 'future_trips' contains trips beyond that time window
    if client == 'mobile':
        return JsonResponse({"upcoming_trips": upcoming_trips, "future_trips": future_trips}, status=200)
    elif client == 'admin':
        return JsonResponse({"all_trips": all_trips}, status=200)

@api_view(['GET'])
def get_trips(request) -> HttpResponse | JsonResponse:
    """
    Returns the upcoming trips. (Trips that are nearest in time)
    :param requst:
    :return:
    """
    # client = request.query_params.get('client')
    upcoming_trips = []
    future_trips = []
    all_trips = []
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    time_window = 0
    time_period = request.query_params.get('time_period')

    # Query for today's trips
    todays_trips = Trip.objects.filter(trip_date=current_date, schedule__departure_time__gt=current_time).order_by(
            'schedule__departure_time')

    if not todays_trips.exists():
        return JsonResponse({"message": "No more trips today."})

    count = 0
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
        print(type(departure_time))
        stops = []

        if count == 0:
            time_window = departure_time

        # Stops query
        stop_list = SemesterScheduleStop.objects.filter(schedule__schedule_id=schedule_id).order_by('departure_time')

        for stop in stop_list:
            stops.append({
                "stop_name": stop.stop.stop_name,
                "stop_cost": stop.stop.cost,
                "stop_departure_time": stop.departure_time
            })

        # Get capacity for trip
        tickets_booked = trip.booked_tickets
        bus_capacity = trip.assigned_vehicle.capacity
        capacity = str(tickets_booked)+"/"+str(bus_capacity)

        # Build trip object
        data = {
            "trip_id": trip.trip_id,
            "trip_date": trip.trip_date,
            "assigned_driver": driver_name,
            "starting_location": starting_location,
            "departure_time": departure_time,
            "final_destination": final_destination,
            "license_plate": license_plate,
            "bus_description": bus_description,
            "booked_seats": capacity,
            "stop": stops,
        }

        # if client == 'mobile':
            # Check if the departure time is within 10 minutes of the time window
            # time_difference = (departure_time - time_window).total_seconds() / 60  # in minutes
            # time_limit = (time_window + timedelta(minutes=10)).time()
            # time_limit =

        print(time_window, departure_time)
        time_window_seconds = time_window.hour * 3600 + time_window.minute * 60 + time_window.second
        departure_time_seconds = departure_time.hour * 3600 + departure_time.minute * 60 + departure_time.second

        # Check if the departure time is within 10 minutes (600 seconds) of the time window
        if departure_time_seconds < (time_window_seconds + 600):
            upcoming_trips.append(data)
        else:
            future_trips.append(data)

        # if client == 'admin':
        #     all_trips.append(data)

        count += 1

    # 'upcoming_trips' contains trips within 10 minutes of the time window,
    # and 'future_trips' contains trips beyond that time window
    if time_period == 'upcoming':
        return JsonResponse({"upcoming_trips": upcoming_trips, "future_trips": future_trips}, status=200)
    elif time_period == 'future':
        return JsonResponse({"future_trips": future_trips}, status=200)



@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
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

@api_view(['POST'])
def book_trip(request) -> HttpResponse:
    """
    Books a trip for the user
    :param request: Request contains, stop id for trip
    :return:
    """

    # Get user details
    token_key = request.headers.get('Authorization').split(' ')[1]

    # Fetch the token object from the database
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        # Handle the case where the token is not valid
        return HttpResponse(content="Invalid User!", status=401)

    # Retrieve the user and requsted stop
    user = token.user
    user_stopid = request.data.get('stop_id')
    user_tripid = request.data.get('trip_id') #check if trip exists
    trip = Trip.objects.get(trip_id=user_tripid)
    ticket_price = Stops.objects.get(stop_id=user_stopid).cost
    vehicle_capacity = trip.assigned_vehicle.capacity
    no_of_booked_tickets = trip.booked_tickets

    # Check available seats
    if no_of_booked_tickets == vehicle_capacity:
        return HttpResponse(content="The bus is full, no available seats",
                            status=400)



    # payment

    # Create ticket
    new_ticket = Ticket(trip_id=user_tripid,
                        employee_id=user.employee_id,
                        purchase_date=datetime.now(),
                        ticket_price=ticket_price
    )
    new_ticket.save()

    trip.booked_tickets += 1
    trip.save()

    confirmation = {
        "license_plate": trip.assigned_vehicle.license_plate,
        "ticket_rice": ticket_price,
        "ticket_number": new_ticket.ticket_id
    }

    return JsonResponse(confirmation,status= 200)

    # Book ticket for staff


    # new_ticket = Ticket(
    #     trip_id=user_tripid,
    #     employee_id=user.empl
    # )



    # # Get requested trip
    # # requested_trip = Trip.objects.get(schedule__semesterschedulestop__stop=user_stop,
    # #                                   trip_date =  datetime.now().date())
    #
    # # requested_trip = Trip.objects.filter(
    # #     schedule__semester_schedule_stop__stop__stop_id=user_stop,
    # #     trip_date=datetime.now().date()
    # # ).first()
    #
    # requested_trip = Trip.objects.filter(schedule__schedule_id__semester_schedule_stop = user_stop)
    # # requested_trip = Trip.objects.filter(schedule__schedule_id=
    #
    # # )
    #
    #
    # print(requested_trip.trip_id,requested_trip.schedule_id)


    # return HttpResponse()











