# from django.http import JsonResponse, HttpRequest, HttpResponse
# from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
# from Logistics_ticket_API.models import  *
from Logistics_ticket_API.serializers import *
from rest_framework.response import Response
# from django.db import connection
from rest_framework.decorators import api_view
from . import helpers
# from rest_framework import status
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def login(request) -> HttpResponse | JsonResponse :
    """
    logs in the user
    :param request:
    :return:
    """

    ashesi_email = request.data.get('ashesi_email')
    password = request.data.get('password')

    #check email exists
    try:
        user_ref = AshesiEmployee.objects.get(ashesi_email=ashesi_email)
    except AshesiEmployee.DoesNotExist:
        return HttpResponse(content="User does not exist", status=404)

    if user_ref.check_password(password):
        token, created = Token.objects.get_or_create(user=user_ref)
        print(token.key)
        return JsonResponse({'token': str(token.key)}, status=200)
    else:
        return HttpResponse(content="Passwords do not match", status=400)


@api_view(['POST'])
def signup(request) -> HttpResponse:
    """
    Signs up a user on the platform
    :param request:
    :return:
    """
    # Check request is valid
    serializer = AshesiEmployeeSerializer(data=request.data)
    # try:
    #     if not serializer.is_valid():
    #         # return HttpResponse(content="One of the required sign up fields is missing",
    #         #                     status = 400)
    #         return HttpResponse(content=serializer.errors, status=500)
    # except Exception as e:
    #     print(e)

    # Check email is not taken
    if helpers.check_email_exists(request.data.get('ashesi_email')):
        return HttpResponse(content="Account with email already exists", status=400)

    # Create new user
    new_user = AshesiEmployee(
        employee_id = request.data.get('employee_id'),
        f_name = request.data.get('f_name'),
        l_name = request.data.get('l_name'),
        ashesi_email = request.data.get('ashesi_email'),
        # account_password = request.data.get('password'),
        momo_network = request.data.get('momo_network'),
        momo_number = request.data.get('momo_number')
    )
    new_user.set_password(request.data.get('password'))
    new_user.save()

    return HttpResponse(content='User Created', status=201)









def test_token():
    return