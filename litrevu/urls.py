"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import fonctionnement.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.LoginPageView.as_view(), name="login"),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("ticket/add/", fonctionnement.views.ticket_create, name="ticket-create"),
    path("ticket/<int:id>/", fonctionnement.views.ticket_detail, name="ticket-detail"),
    path(
        "ticket/<int:id>/update/",
        fonctionnement.views.ticket_update,
        name="ticket-update",
    ),
    path(
        "ticket/<int:id>/delete/",
        fonctionnement.views.ticket_delete,
        name="ticket-delete",
    ),
    path("review/add/", fonctionnement.views.review_create, name="review-create"),
    path(
        "review/<int:id>/add/",
        fonctionnement.views.review_response_create,
        name="review-response-create",
    ),
    path("review/<int:id>/", fonctionnement.views.review_detail, name="review-detail"),
    path(
        "review/<int:id>/update/",
        fonctionnement.views.review_update,
        name="review-update",
    ),
    path(
        "review/<int:id>/delete/",
        fonctionnement.views.review_delete,
        name="review-delete",
    ),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)