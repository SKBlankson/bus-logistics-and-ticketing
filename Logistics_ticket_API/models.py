# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AshesiEmployee(models.Model):
    employee_id = models.CharField(primary_key=True, max_length=10)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    ashesi_email = models.CharField(max_length=100, blank=True, null=True)
    account_password = models.CharField(max_length=250, blank=True, null=True)
    momo_network = models.JSONField(blank=True, null=True)
    momo_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ashesi_employee'


class Driver(models.Model):
    employee = models.OneToOneField(AshesiEmployee, models.DO_NOTHING, primary_key=True)
    drivers_license_number = models.CharField(max_length=20)
    license_expiry_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'driver'


class EmployeeTrip(models.Model):
    trip = models.OneToOneField('Trip', models.DO_NOTHING, primary_key=True)  # The composite primary key (trip_id, employee_id) found, that is not supported. The first column is selected.
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey(AshesiEmployee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'employee_trip'
        unique_together = (('trip', 'employee'),)


class PrivateTrip(models.Model):
    trip = models.OneToOneField('Trip', models.DO_NOTHING, primary_key=True)
    trip_notes = models.CharField(max_length=600, blank=True, null=True)
    client_list = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'private_trip'


class SemesterSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    day_of_week = models.JSONField()
    pickup_location = models.ForeignKey('Stops', models.DO_NOTHING, db_column='pickup_location')
    final_destination = models.ForeignKey('Stops', models.DO_NOTHING, db_column='final_destination', related_name='semesterschedule_final_destination_set')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'semester_schedule'


class SemesterScheduleStop(models.Model):
    schedule = models.OneToOneField(SemesterSchedule, models.DO_NOTHING, primary_key=True)  # The composite primary key (schedule_id, stop_id) found, that is not supported. The first column is selected.
    stop = models.ForeignKey('Stops', models.DO_NOTHING)
    departure_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'semester_schedule_stop'
        unique_together = (('schedule', 'stop'),)


class Staff(models.Model):
    employee = models.OneToOneField(AshesiEmployee, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'staff'


class StaffShuttleTrip(models.Model):
    trip = models.OneToOneField('Trip', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'staff_shuttle_trip'


class Stops(models.Model):
    stop_id = models.CharField(primary_key=True, max_length=20)
    stop_name = models.CharField(unique=True, max_length=150)
    cost = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stops'


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey('Trip', models.DO_NOTHING)
    employee = models.ForeignKey(AshesiEmployee, models.DO_NOTHING)
    purchase_date = models.DateTimeField()
    ticket_price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ticket'


class Trip(models.Model):
    trip_id = models.CharField(primary_key=True, max_length=10)
    schedule = models.ForeignKey(SemesterSchedule, models.DO_NOTHING)
    trip_date = models.DateTimeField()
    assigned_driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='assigned_driver')
    assigned_vehicle = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='assigned_vehicle')

    class Meta:
        managed = False
        db_table = 'trip'


class Vehicles(models.Model):
    license_plate = models.CharField(primary_key=True, max_length=20)
    vehicle_type = models.CharField(max_length=20)
    capacity = models.IntegerField()
    descriptive_name = models.CharField(max_length=100)
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    permit_issuer = models.CharField(max_length=100, blank=True, null=True)
    permit_issue_date = models.DateField(blank=True, null=True)
    permit_expiry_date = models.DateField(blank=True, null=True)
    assigned_driver = models.ForeignKey(AshesiEmployee, models.DO_NOTHING, db_column='assigned_driver', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicles'
