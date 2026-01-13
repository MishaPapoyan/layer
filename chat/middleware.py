from django.utils import timezone
from .models import AdminOnlineStatus


class AdminOnlineStatusMiddleware:
    """Update admin online status"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Update admin online status if user is staff
        if request.user.is_authenticated and request.user.is_staff:
            admin_status, created = AdminOnlineStatus.objects.get_or_create(admin=request.user)
            admin_status.is_online = True
            admin_status.last_seen = timezone.now()
            admin_status.save()
        
        response = self.get_response(request)
        return response

