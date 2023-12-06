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
    :return:
    """

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







