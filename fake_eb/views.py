# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings

from fake_eb.models import FakeEventbriteEvent
from fake_eb.utils import fix_fake_response_times

PAGINATION_PAGE_LENGTH = 50

def wrap_response(event_list):
    object_count = len(event_list)
    page_size = (object_count, PAGINATION_PAGE_LENGTH)
    page_count = object_count % (PAGINATION_PAGE_LENGTH + 1)
    return {"pagination": {
        "object_count": object_count,
        "page_number": 1,
        "page_size": page_size,
        "page_count": page_count,
        "continuation": "add continuation later maybe",
        "has_more_items": page_count > 1},
            "events": event_list[:PAGINATION_PAGE_LENGTH]
    }


class FakeEventBriteEventsView(View):
    def get(self, request, *args, **kwargs):
        event_list = FakeEventbriteEvent.objects.values()
        event_list = fix_fake_response_times(event_list)
        data = wrap_response(event_list)
        return JsonResponse(data=data)
    
