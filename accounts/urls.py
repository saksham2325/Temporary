from django.db import router
from django.urls import include, path, re_path
from rest_framework import routers

from accounts import views as accounts_views


router = routers.DefaultRouter()
router.register(r'users', accounts_views.UserViewSet, basename="user")
router.register(r'groups', accounts_views.GroupViewSet, basename="group")
router.register(r'user-jiraToken',
                accounts_views.UserJiraTokenViewset, basename="userJiraToken")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', accounts_views.UserLoginView.as_view()),
    path('logout/', accounts_views.UserLogoutView.as_view()),
    path('user-groups/', accounts_views.UserGroups.as_view(), name='user-groups'),
    path('user-groups/<int:pk>/', accounts_views.UserGroups.as_view()),
    path('update-password/<int:pk>/', accounts_views.UpdatePassword.as_view()),
    path('verify-token/', accounts_views.VerifyToken.as_view(), name='verify-email'),
    path('send-token/', accounts_views.SendToken.as_view(), name='send-token'),
    path('send-invitation/',accounts_views.SendInvitation.as_view(), name='send-invitation'),
]
