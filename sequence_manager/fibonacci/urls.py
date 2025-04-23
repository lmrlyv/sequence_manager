from django.urls import path

from sequence_manager.fibonacci.views import (
    BlacklistNumberView,
    FibonacciNumberListView,
    FibonacciNumberView,
)


urlpatterns = [
    path("api/v1/fibonacci/<int:number>/", FibonacciNumberView.as_view(), name="fibonacci-number"),
    path(
        "api/v1/fibonacci/list/<int:number>/",
        FibonacciNumberListView.as_view(),
        name="fibonacci-list",
    ),
    path("api/v1/blacklist/<int:number>/", BlacklistNumberView.as_view(), name="manage-blacklist"),
]
