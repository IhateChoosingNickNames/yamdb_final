from rest_framework import mixins


class CreateDestroyListModelMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    pass
