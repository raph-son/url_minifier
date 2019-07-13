"""
mini_url URL Configuration
"""

from django.contrib import admin
from django.urls import path
from url_shorter import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("submission/", views.submit_url),
    path("<str:hash>", views.redirect_out),
]
