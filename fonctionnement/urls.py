from django.urls import path
from . import views

urlpatterns = [
    path("flux/", views.flux_detail, name="flux"),
    path("ticket/add/", views.ticket_create, name="ticket-create"),
    path("ticket/<int:id>/", views.ticket_detail, name="ticket-detail"),
    path(
        "ticket/<int:id>/update/",
        views.ticket_update,
        name="ticket-update",
    ),
    path(
        "ticket/<int:id>/delete/",
        views.ticket_delete,
        name="ticket-delete",
    ),
    path("review/add/", views.review_create, name="review-create"),
    path(
        "review/<int:id>/add/",
        views.review_response_create,
        name="review-response-create",
    ),
    path("review/<int:id>/", views.review_detail, name="review-detail"),
    path(
        "review/<int:id>/update/",
        views.review_update,
        name="review-update",
    ),
    path(
        "review/<int:id>/delete/",
        views.review_delete,
        name="review-delete",
    ),
]
