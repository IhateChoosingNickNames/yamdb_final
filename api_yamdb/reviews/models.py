from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import year_validator

User = get_user_model()

LIMIT = 30
SCORE_MIN = 1
SCORE_MAX = 10


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(_("Имя категории"), max_length=256, db_index=True)
    slug = models.SlugField(_("Слаг для URL"), max_length=50, unique=True)

    def __str__(self):
        return self.name[:LIMIT]

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ("name",)


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(_("Название жанра"), max_length=256, db_index=True)
    slug = models.SlugField(_("Слаг для URL"), max_length=50, unique=True)

    def __str__(self):
        return self.name[:LIMIT]

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        ordering = ("name",)


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        _("Название произведения"),
        max_length=256,
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        _("Год публикации"),
        blank=False,
        validators=[year_validator],
    )
    description = models.TextField(_("Описание"), blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, verbose_name=_("Жанр"), related_name="title"
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="title",
    )

    def __str__(self):
        return self.name[:LIMIT]

    class Meta:
        verbose_name = _("Произведение")
        verbose_name_plural = _("Произведения")
        ordering = ("name",)


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User, verbose_name=_("Автор отзыва"), on_delete=models.CASCADE
    )
    text = models.TextField(_("Текст отзыва"), max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        _("Оценка"),
        validators=[
            MinValueValidator(SCORE_MIN, _("Допустимы значения от 1 до 10")),
            MaxValueValidator(SCORE_MAX, _("Допустимы значения от 1 до 10")),
        ],
    )
    title = models.ForeignKey(
        Title,
        verbose_name=_("Произведение"),
        on_delete=models.CASCADE,
        related_name="review",
    )

    def __str__(self):
        return f"{self.author[:LIMIT]} - {self.text[:LIMIT]}"

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ("-pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_review"
            ),
        )


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User, verbose_name=_("Автор комментария"), on_delete=models.CASCADE
    )
    text = models.CharField(_("Текст комментария"), max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review,
        verbose_name=_("Отзыв"),
        on_delete=models.CASCADE,
        related_name="comment",
    )

    def __str__(self):
        return f"{self.author[:LIMIT]} - {self.text[:LIMIT]}"

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ("-pub_date",)
