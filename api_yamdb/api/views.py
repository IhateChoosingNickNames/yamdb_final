from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, response, status, views,
                            viewsets)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import Auth, User

from .filters import CustomSearchFilter
from .mixins import CreateDestroyListModelMixin
from .pagination import CustomPagination
from .permissions import (IsAdmin, IsAdminOrModOrReadOnly, IsAdminOrReadOnly,
                          IsAuthorOrAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RetrieveTokenSerializer,
                          RetrieveUpdateMeSerializer, ReviewSerializer,
                          SingUpSerializer, TitleSerializer, UserSerializer)
from .utils import send_message


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет юзеров."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    lookup_field = "username"
    search_fields = ("username",)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head',
                         'options', 'trace')


class RetrievePatchMeView(generics.RetrieveUpdateAPIView):
    """Получение и обновления данных пользователя."""

    serializer_class = RetrieveUpdateMeSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователя."""

    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создание нового пользователя.
        Если пользователь сам регистрируется - то создается новый пользователь
        и на почту отправляется код подтверждения.
        Если админ создает, то пользователь уже есть в системе и ему просто
        отправится код подтверждения.
        """
        confirmation_code = get_random_string()
        data = request.data.copy()
        serializer = self.get_serializer(data=data)

        # user = User.objects.filter(**request.data)
        user = User.objects.filter(username=request.data.get("username"),
                                   email=request.data.get("email"))
        if not serializer.is_valid() and user:
            user = user[0]
            context = {"confirmed": "Сообщение отправлено"}
        else:

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            if not request.user.is_staff:
                user.is_active = False
                user.save()
            context = serializer.data

        auth, _ = Auth.objects.get_or_create(user=user)
        auth.confirmation_code = confirmation_code
        auth.save()
        send_message(request.data["email"], confirmation_code)
        return response.Response(context, status=status.HTTP_200_OK)


class RetrieveTokenView(views.APIView):
    """Получение токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Получение токена.
        Если пользователь существует и хочет обновить свой токен, то он
        отправит username. Если пользователь неактивен, то он должен ввести
        код подтверждения.
        """

        user = User.objects.filter(
            username=request.data.get("username")
        ).first()

        if (
            not user
            or not user.is_active
            or request.user.username != request.data["username"]
        ):
            serializer = RetrieveTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if not user.is_active:
                user.is_active = True
                user.save()
                auth = Auth.objects.filter(user=user).first()
                if auth:
                    auth.delete()

        refresh = RefreshToken.for_user(user)
        return response.Response(
            {"token": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    # Консоли очень не нравится, что у меня 2 Джанга, поэтому добавил order_by
    queryset = (
        Title.objects.all()
        .annotate(average=Avg("review__score"))
        .order_by("name")
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = CustomSearchFilter


class CategoryViewSet(CreateDestroyListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = CustomPagination
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = CustomPagination
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModOrReadOnly)
    pagination_class = CustomPagination

    def __get_title(self):
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def get_queryset(self):
        return self.__get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.__get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModOrReadOnly)
    pagination_class = CustomPagination

    def __get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def get_queryset(self):
        return self.__get_review().comment.all().select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())
