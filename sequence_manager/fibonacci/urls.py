from django.urls import path

from sequence_manager.fibonacci.views import (
    BlacklistNumberView,
    FibonacciListView,
    FibonacciValueView,
)


urlpatterns = [
    path("api/v1/fibonacci/<int:number>/", FibonacciValueView.as_view(), name="fibonacci-value"),
    path("api/v1/fibonacci/", FibonacciListView.as_view(), name="fibonacci-list"),
    path("api/v1/blacklist/<int:number>/", BlacklistNumberView.as_view(), name="manage-blacklist"),
]
