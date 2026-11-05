from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    Object-level rule for a single book:
      * Anyone may read (GET, HEAD, OPTIONS).
      * Only the book's owner, or a staff user, may change or delete it.
    Books with no owner (created before ownership existed) can only be removed by staff.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff or obj.owner_id == request.user.id)