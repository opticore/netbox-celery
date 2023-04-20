"""URLs for the example_plugin plugin."""
from django.urls import path

from example_plugin.views import ExampleAddView


urlpatterns = [
    path("add/", ExampleAddView.as_view(), name="example_add"),
]
