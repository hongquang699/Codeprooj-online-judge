from rest_framework import permissions

def user_has_org_permission(user, organization, permission_name):
    """
    Check if a user has a specific permission in an organization.
    Superusers and organization owners have all permissions.
    """
    if not user or not user.is_authenticated or not user.is_active:
        return False
    if user.is_superuser or user.is_staff:
        return True
    
    # Check if user is owner of organization
    if hasattr(organization, 'owner_id') and organization.owner_id == getattr(user, 'id', None):
        return True

    from .models import OrganizationMember, OrganizationPermission
    membership = OrganizationMember.objects.filter(
        organization=organization,
        user=user,
        status='active'
    ).select_related('role').first()

    if not membership:
        return False

    role = membership.role
    if role.name.lower() == 'owner':
        return True

    # Check role permissions
    perms = list(OrganizationPermission.objects.filter(role=role).values_list('permission', flat=True))
    if '*' in perms:
        return True
    
    # Check wildcard like 'member.*'
    parts = permission_name.split('.')
    if len(parts) == 2 and f"{parts[0]}.*" in perms:
        return True

    return permission_name in perms


def get_user_org_role(user, organization):
    """Return user's role name in organization or None."""
    if not user or not user.is_authenticated or not user.is_active:
        return None
    if hasattr(organization, 'owner_id') and organization.owner_id == getattr(user, 'id', None):
        return 'Owner'
    from .models import OrganizationMember
    m = OrganizationMember.objects.filter(organization=organization, user=user, status='active').select_related('role').first()
    return m.role.name if m else None
