from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from connections.models import Connection
from connections.serializers import UserSearchSerializer, ConnectionSerializer
from rest_framework import status
from notifications.tasks import send_connection_notification
from django.db.models import Q

class SearchUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        users = CustomUser.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(company_name__icontains=query)
        ).exclude(id=request.user.id)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)


class SendConnectionRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
            connection, created = Connection.objects.get_or_create(
                from_user=request.user, to_user=to_user
            )
            if not created:
                return Response({"message": "Request already exists."}, status=400)
            return Response({"message": "Connection request sent."}, status=201)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=404)


class RespondConnectionRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        action = request.data.get('action')
        try:
            connection = Connection.objects.get(id=pk, to_user=request.user)
            if action == 'accept':
                connection.status = 'accepted'
            elif action == 'reject':
                connection.status = 'rejected'
            else:
                return Response({"message": "Invalid action."}, status=400)

            connection.save()

            # Trigger Celery task for sending notification
            send_connection_notification.delay(connection.id)

            return Response({"message": f"Connection request {action}ed."})
        except Connection.DoesNotExist:
            return Response({"message": "Connection not found."}, status=404)

class UserConnectionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all connections where user is involved and status is 'accepted'
        connections = Connection.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user)
            # ,status='accepted'
        )
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data)