from django_multitenant.utils import set_current_tenant, unset_current_tenant

class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Check if current user is authenticated
        if request.user.is_authenticated:
            # Then, check if user is a tenant and not a developer
            if not request.user.is_staff and not request.user.is_superuser:
                if getattr(request.user, "role") == "tenant":
                    # Assign all related data to the tenant
                    set_current_tenant(tenant=request.user)
        response = self.get_response(request)
        # Ensure tenant context is unset after the request processing
        unset_current_tenant()
        return response