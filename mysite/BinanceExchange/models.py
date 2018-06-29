from django.db import models

# Create your models here.
# class BinanceExchangeInformation(models.Model):
#     symbol = models.CharField(max_length=20)
#     baseAsset = models.CharField(max_length=20)
#     quoteAsset = models.CharField(max_length=20)
#     minPrice = models.CharField(max_length=20)
#     maxPrice = models.CharField(max_length=20)
#     tickSize = models.CharField(max_length=20)
#     minQty = models.CharField(max_length=20)
#     maxQty = models.CharField(max_length=20)
#     stepSize = models.CharField(max_length=20)

#     def __str__(self):
#         return self.symbol,self.minQty,self.maxQty,self.stepSize
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Binanceexchangeinformation(models.Model):
    symbol = models.CharField(max_length=15)
    baseasset = models.CharField(db_column='baseAsset', max_length=10)  # Field name made lowercase.
    quoteasset = models.CharField(db_column='quoteAsset', max_length=10)  # Field name made lowercase.
    minprice = models.CharField(db_column='minPrice', max_length=15)  # Field name made lowercase.
    maxprice = models.CharField(db_column='maxPrice', max_length=15)  # Field name made lowercase.
    ticksize = models.CharField(db_column='tickSize', max_length=15)  # Field name made lowercase.
    minqty = models.CharField(db_column='minQty', max_length=15)  # Field name made lowercase.
    maxqty = models.CharField(db_column='maxQty', max_length=15)  # Field name made lowercase.
    stepsize = models.CharField(db_column='stepSize', max_length=15)  # Field name made lowercase.

    def show(self):
        return str(self.symbol)

    class Meta:
        #managed = False
        db_table = 'BinanceExchangeInformation'


class Coinlist(models.Model):
    coin_id = models.CharField(max_length=10)
    name = models.CharField(db_column='Name', max_length=10)  # Field name made lowercase.
    coinname = models.CharField(db_column='CoinName', max_length=15)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=150)  # Field name made lowercase.
    algorithm = models.CharField(db_column='Algorithm', max_length=15)  # Field name made lowercase.
    prooftype = models.CharField(db_column='ProofType', max_length=15)  # Field name made lowercase.
    sortorder = models.CharField(db_column='SortOrder', max_length=15)  # Field name made lowercase.


    def fetchData(self):
        return (self.name,self.coinname)
    class Meta:
        #managed = False
        db_table = 'CoinList'


class Facebook(models.Model):
    coin_id = models.CharField(max_length=10)
    likes = models.CharField(max_length=15)
    is_closed = models.CharField(max_length=10)
    talking_about = models.CharField(max_length=10)
    link = models.CharField(max_length=150)
    points = models.CharField(db_column='Points', max_length=15)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'Facebook'


class Reddit(models.Model):
    coin_id = models.CharField(max_length=10)
    subscribers = models.CharField(max_length=15)
    active_users = models.CharField(max_length=10)
    community_creation = models.CharField(max_length=15)
    posts_per_hour = models.CharField(max_length=10)
    posts_per_day = models.CharField(max_length=10)
    comments_per_hour = models.CharField(max_length=10)
    comments_per_day = models.CharField(max_length=10)
    link = models.CharField(max_length=150)
    points = models.CharField(db_column='Points', max_length=15)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Reddit'


class Twitter(models.Model):
    coin_id = models.CharField(max_length=10)
    followers = models.CharField(max_length=10)
    following = models.CharField(max_length=10)
    lists = models.CharField(max_length=10)
    favourites = models.CharField(max_length=10)
    statuses = models.CharField(max_length=10)
    account_creation = models.CharField(max_length=10)
    link = models.CharField(max_length=150)
    points = models.CharField(db_column='Points', max_length=15)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'Twitter'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=80)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'

class payload:
    panda_data = {'ETC':0.2,'BTC':0.2,'ADA':0.3,'LTC':0.3,'ETH':0.2}
    panda_rebalance = {}
    key = ''
    secret=''
    main_curreny=''
    quantity = 0.0
