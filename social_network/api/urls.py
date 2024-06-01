from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (UserCreateView, UserLoginView, UserSearchView, send_friend_request, respond_to_friend_request,
list_friends, list_pending_requests, get_csrf_token)

urlpatterns = [
    path('csrf-token/', get_csrf_token, name='csrf-token'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('friend-request/send/', send_friend_request, name='send_friend_request'),
    path('friend-request/respond/', respond_to_friend_request, name='respond_friend_request'),
    path('friends/', list_friends, name='list_friends'),
    path('friend-requests/', list_pending_requests, name='list_pending_requests'),

]
