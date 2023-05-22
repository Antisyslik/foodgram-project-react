from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


class ActionMixin:
    def action_add(self, request, data, model_class, serializer_class, success_status):
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=success_status)

    def delete_action(self, request, model_class, data):
        instance = get_object_or_404(model_class, **data)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)