from django.urls import path
from .views import *

urlpatterns = [
    path("organizations/<int:organization_id>/events",
         FakeEventBriteEventsView.as_view(),
         name="organizations")
    ]
