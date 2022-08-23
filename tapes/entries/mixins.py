class UserOwnershipMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
