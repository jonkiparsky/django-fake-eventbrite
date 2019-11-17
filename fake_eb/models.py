# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import time

from django.conf import settings
from django.db.models import (
    AutoField,
    BigIntegerField,
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    Model,
    TextField,
    TimeField,
)

NOON = time(hour=12)
status_choices = ((x,x) for x in ["draft",
                                  "live",
                                  "started",
                                  "ended",
                                  "completed",
                                  "canceled"])
class FakeEventbriteEvent(Model):
    name_text = TextField(
        default="Fake Eventbrite Event")
    name_html = TextField(
        default="Fake Eventbrite Event")
    description_text = TextField(
        blank=True,
        null=True,
        default="Fake Eventbrite Event Description")
    description_html = TextField(
        blank=True,
        null=True,
        default="Fake Eventbrite Event Description")
    day_specifier = TextField(
        default="today")
    offset_specifier = TextField(
        default="")
    duration_specfier = TextField(default="")
    time = TimeField(default=NOON)
    timezone = CharField(max_length=50, default="America/New_York")
    eventbrite_id = CharField(max_length=20, default="1234567")
    day_specifier = TextField()
    offset_specifier = TextField()
    duration_specifier = TextField() # not used atm
    organization_id = BigIntegerField(default=settings.DEFAULT_ORGANIZATION_ID)
    created = DateTimeField(auto_now_add=True)
    changed = DateTimeField(auto_now=True)
    published = DateTimeField(auto_now_add=True)    
    capacity = IntegerField(default=100)
    capacity_is_custom = BooleanField(default=False)
    status = TextField(choices=status_choices,
                       default="live")
    currency = CharField(max_length=5, default="USD")    
    listed = BooleanField(default=False)
    shareable = BooleanField(default=True)
    invite_only = BooleanField(default=False)
    password = CharField(max_length=64, default="password")
    online_event = BooleanField(default=False) 
    show_remaining = BooleanField(default=True)
    tx_time_limit = IntegerField(default=480)
    hide_start_date = BooleanField(default=False)
    hide_end_date = BooleanField(default=False)    
    locale = CharField(max_length=10, default="en_US")
    is_locked = BooleanField(default=False)
    privacy_setting = CharField(max_length=20, default="unlocked")
    is_series = BooleanField(default=False)
    is_series_parent = BooleanField(default=False)
    inventory_type: CharField(max_length=20, default="limited")
    is_reserved_seating = BooleanField(default=False)
    show_pick_a_seat = BooleanField(default=False)
    show_seatmap_thumbnail = BooleanField(default=False)
    show_colors_in_seatmap_thumbnail = BooleanField(default=False)
    source = CharField(max_length=20, default="create_2.0")
    is_free = BooleanField(default=False)
    version = CharField(max_length=20, default="3.0.0")
    summary = TextField(blank=True, null=True)
    logo_id = CharField(max_length=20, blank=True, null=True)
    organizer_id = CharField(max_length=20, 
                             default=settings.DEFAULT_ORGANIZER_ID)
    venue_id = CharField(max_length=20, default="7882563")
    category_id = CharField(max_length=20, null=True, blank=True)
    subcategory_id = CharField(max_length=20, null=True, blank=True)
    format_id = CharField(max_length=20, null=True, blank=True)
    is_externally_ticketed = BooleanField(default=False)

        
