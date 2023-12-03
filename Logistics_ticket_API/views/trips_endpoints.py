from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from django.db import connection
from rest_framework.decorators import api_view
from . import helpers


def get_todays_trips():
    return

def get_trips_in_date_range():
    return

def edit_trip():
    return

def delete_trip():
    return

def book_trip():
    return







