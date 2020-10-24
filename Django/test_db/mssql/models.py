from django.db import models
from datetime import timezone

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Airports(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    created =  models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'<{self.airport}> - {self.city}'

    class Meta:
        managed = False
        db_table = 'airports'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    departure = models.ForeignKey(Airports, models.DO_NOTHING,
                                  related_name='departure', db_column='departure')
    arrival   = models.ForeignKey(Airports, models.DO_NOTHING,
                                  related_name='arrival', db_column='arrival')
    duration  = models.IntegerField()
    
    
    def __str__(self):
        return f' flight {self.flight_id}: {self.departure} to {self.arrival}'

    class Meta:
        managed = False
        db_table = 'flights'


class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey('Flights', models.DO_NOTHING)
    pax = models.IntegerField(db_column='PAX')  # Field name made lowercase.
    flight_date = models.DateTimeField()
    status = models.CharField(max_length=3)
    created = models.DateTimeField()
    author = models.CharField(max_length=20, blank=True, null=True)
    
    def update(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return f'<{self.booking_id}>: flight {self.flight_id}, PAX {self.pax}'

    class Meta:
        managed = False
        db_table = 'bookings'

class Passengers(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flights, through='PassengerFlights', blank=True, related_name="passengers")
    passport = models.CharField(max_length=20, blank=True, null=True)
    birth = models.DateTimeField(blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first} {self.last}'
    
    class Meta:
        managed = False
        db_table = 'passengers'

        
class PassengerFlights(models.Model):
    pf_id       = models.AutoField(primary_key=True)
    passenger_id   = models.ForeignKey(Passengers, models.DO_NOTHING,
                    related_name ='passenger', db_column='passenger_id')
    flight_id     = models.ForeignKey(Flights, models.DO_NOTHING,
                    related_name = 'flight', db_column = 'flight_id')
    flight_date = models.DateTimeField(blank=True, null=True)
    status      = models.IntegerField()
    updated_by  = models.CharField(max_length=20, blank=True, null=True)
#    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_flights'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
