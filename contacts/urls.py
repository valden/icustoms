from django.urls import path
from contacts.views import ContactFormView


urlpatterns = [
    path("", ContactFormView.as_view(), name="contacts"),
]
