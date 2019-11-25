from django.urls import include

urlpatterns = [
    path("", include('fake_eb.urls')),
]
