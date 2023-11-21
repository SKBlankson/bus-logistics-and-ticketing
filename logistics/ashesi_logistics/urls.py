from django.urls import path
from . import views


#url configuaration model. Maps urls to view functions.
# view functions return a HTTP response
urlpatterns = [
    path('home/', views.home)
]