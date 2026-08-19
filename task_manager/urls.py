from django.contrib import admin
from django.urls import include, path

from task_manager.views import IndexView
from users.views import (
    UserLoginView,
    UserLogoutView,
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "users/",
        include("users.urls"),
    ),
    path(
        "statuses/",
        include("statuses.urls"),
    ),
    path(
        "labels/",
        include("labels.urls"),
    ),
    path(
        "tasks/",
        include("tasks.urls"),
    ),
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "sentry-debug/",
        trigger_error
    ),
]