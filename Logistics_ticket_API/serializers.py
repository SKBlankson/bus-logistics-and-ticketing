from rest_framework import serializers
from .models import AshesiEmployee, Driver, EmployeeTrip, PrivateTrip, SemesterSchedule,SemesterScheduleStop
from .models import Staff, StaffShuttleTrip, Stops, Ticket, Trip, Vehicles

class AshesiEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AshesiEmployee
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    # employee_details = AshesiEmployeeSerializer()
    class Meta:
        model = Driver
        fields = '__all__'


class EmployeeTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTrip

class PrivateTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateTrip

class SemesterScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterSchedule

class SemesterScheduleStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterScheduleStop

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff

class StaffShuttleTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffShuttleTrip

class StopsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Stops

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip

class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'