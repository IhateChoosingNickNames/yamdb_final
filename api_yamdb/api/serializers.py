from django.shortcuts import get_object_or_404
from rest_framework import exceptions, relations, serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import Auth, User


class RetrieveUpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели юзеров."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class SingUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        """Дополнительная валидация юзернейма на уровне сериализатора."""
        if value == "me":
            raise serializers.ValidationError("Недопустимое имя пользователя.")
        return value


class RetrieveTokenSerializer(serializers.Serializer):
    """Проверка кода подтверждения и выдача токена."""

    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        auth = get_object_or_404(
            Auth, user__username=self.initial_data.get("username")
        )
        if auth.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("Некорретный код подтверждения.")
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CustomSlugRelatedField(relations.SlugRelatedField):
    """Переопределения ответа."""

    def to_representation(self, obj):
        return {
            obj._meta.fields[1].name: obj.name,
            obj._meta.fields[2].name: obj.slug,
        }


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели произведений."""

    category = CustomSlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )

    genre = CustomSlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        required=False,
        many=True,
    )
    rating = serializers.IntegerField(source="average", read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "genre",
            "description",
            "category",
            "rating",
        )
        read_only_fields = ("rating",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "score", "author", "pub_date")

    def validate(self, attrs):
        user = self.context["request"].user
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        method = self.context["request"].method
        if (
            method == "POST"
            and Review.objects.filter(author=user, title__id=title_id).exists()
        ):
            raise exceptions.ValidationError("Вы уже оставили свой отзыв.")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
