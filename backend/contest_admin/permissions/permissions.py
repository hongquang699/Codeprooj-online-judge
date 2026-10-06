from backend.judge.models import Contest
from django.contrib.auth.models import User

# Role capability mapping
ROLE_PERMISSIONS = {
    'owner': ['*'],
    'contest_manager': [
        'contest.view', 'contest.edit', 'participant.manage', 'announcement.manage',
        'clarification.manage', 'ranking.manage', 'reports.view', 'problem.view',
        'submission.view', 'audit.view'
    ],
    'problem_setter': [
        'contest.view', 'problem.view', 'problem.create', 'problem.edit',
        'testcase.manage', 'checker.manage', 'validator.manage', 'solution.manage',
        'submission.view'
    ],
    'jury_manager': [
        'contest.view', 'submission.view', 'submission.rejudge', 'judge.view',
        'ranking.manage', 'reports.view', 'audit.view'
    ],
    'moderator': [
        'contest.view', 'participant.manage', 'clarification.manage', 'announcement.manage',
        'submission.view'
    ],
    'observer': [
        'contest.view', 'ranking.manage', 'reports.view', 'submission.view'
    ]
}

def resolve_admin_user(request):
    """Helper to extract user from session, token, X-Username header or query."""
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    username = request.headers.get('X-Username') or request.GET.get('user') or request.GET.get('username')
    if username:
        return User.objects.filter(username=username).first()
    return None

def has_contest_permission(user, contest, permission_name):
    """
    Check if user has specific permission in this contest.
    Superusers, staff, admin username, and contest authors/owners have full rights.
    """
    if not user:
        return False
    if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False) or getattr(user, 'username', '') == 'admin':
        return True

    # Check if contest was created by user or linked through organization owned by user
    from backend.organizations.models import OrganizationContest
    oc = OrganizationContest.objects.filter(contest=contest).select_related('organization').first()
    if oc and oc.organization.owner_id == getattr(user, 'id', None):
        return True

    from ..models.models import ContestAdminRole
    role_obj = ContestAdminRole.objects.filter(contest=contest, user=user).first()
    if not role_obj:
        # Check if user has teacher role
        profile = getattr(user, 'profile', None)
        if profile and profile.role in ['teacher', 'setter']:
            return True
        return False

    role = role_obj.role
    perms = ROLE_PERMISSIONS.get(role, [])
    if '*' in perms or permission_name in perms:
        return True
    
    prefix = permission_name.split('.')[0] + '.*'
    if prefix in perms:
        return True

    return False

def get_user_contest_role(user, contest):
    """Return user's assigned role name or 'Admin' for superusers."""
    if not user:
        return None
    if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False) or getattr(user, 'username', '') == 'admin':
        return 'Contest Administrator'
    
    from backend.organizations.models import OrganizationContest
    oc = OrganizationContest.objects.filter(contest=contest).select_related('organization').first()
    if oc and oc.organization.owner_id == getattr(user, 'id', None):
        return 'Contest Owner'

    from ..models.models import ContestAdminRole
    role_obj = ContestAdminRole.objects.filter(contest=contest, user=user).first()
    if role_obj:
        return role_obj.get_role_display()
    
    profile = getattr(user, 'profile', None)
    if profile and profile.role == 'teacher':
        return 'Teacher / Manager'
    if profile and profile.role == 'setter':
        return 'Problem Setter'

    return None
