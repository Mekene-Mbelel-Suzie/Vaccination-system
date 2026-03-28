from django.urls import path
from .views import ParentSignupView, ParentLoginView

urlpatterns = [
    # PARENT AUTH
    path("parent/signup/", ParentSignupView.as_view(), name="parent-signup"),
    path("parent/login/", ParentLoginView.as_view(), name="parent-login"),
]