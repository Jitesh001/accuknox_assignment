from rest_framework import generics, permissions, status, filters
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import FriendRequest, Friendship
from django.middleware.csrf import get_token
from .pagination import CustomPagination

def home(request):
    return render(request, 'api/index.html')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        query = self.request.query_params.get('nameORemail', None)
        if query:
            return User.objects.filter(email__icontains=query) | User.objects.filter(username__icontains=query)
        return User.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    from_user = request.user
    to_user_email = request.data.get('friend_email')

    try:
        to_user = User.objects.get(email=to_user_email)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Rate limit: max 3 requests per minute
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    
    try:
        recent_requests = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
    except Exception as e:
        print(f"Error querying recent requests: {e}")
        return Response({'error': 'Error querying recent requests'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if recent_requests >= 3:
        return Response({'error': 'Too many requests, please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return Response({'status': 'friend request sent'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status': 'friend request already sent'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_friend_request(request):
    request_id = request.data.get('request_id')
    action = request.data.get('action')
    
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept':
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
        return Response({'status': 'friend request accepted'}, status=status.HTTP_200_OK)
    elif action == 'reject':
        friend_request.delete()
        return Response({'status': 'friend request rejected'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    user = request.user
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = []

    for friendship in friendships:
        if friendship.user1 == user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)
    
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    user = request.user
    pending_requests = FriendRequest.objects.filter(to_user=user)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
