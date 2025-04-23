from celery import shared_task
from notifications.models import Notification
from connections.models import Connection

@shared_task
def send_connection_notification(connection_id):
    try:
        connection = Connection.objects.get(id=connection_id)
        if connection.status == 'accepted':
            message = f"{connection.to_user.username} accepted your connection request."
        elif connection.status == 'rejected':
            message = f"{connection.to_user.username} rejected your connection request."
        else:
            return  # no notification for pending

        # Send notification to the user who SENT the request
        Notification.objects.create(
            user=connection.from_user,
            message=message
        )
    except Connection.DoesNotExist:
        pass
