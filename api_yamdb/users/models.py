from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import additional_username_validator

MAX_LENGTH = 30


class UserManager(BaseUserManager):
    """Кастомный менеджер объектов модели User."""

    def create_user(
        self, email, username, role=None, password=None, **others
    ):
        if not email:
            raise ValueError("У пользователя должен быть указан email")
        if username == "me":
            raise ValueError("Такое имя пользователя недопустимо.")
        if role is None:
            role = User.USER
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            **others
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **others):
        user = self.model(email=self.normalize_email(email), username=username)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.ADMIN
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователей."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("Юзернейм"),
        max_length=150,
        unique=True,
        help_text=_(
            "Обязательное поле. Не более 150 символов. "
            "Допустимые символы: буквы, цифры и @/./+/-/_."
        ),
        validators=[username_validator, additional_username_validator],
        error_messages={
            "unique": _("Пользователь с таким имененем уже существует."),
        },
    )
    email = models.EmailField(_("Почта"), max_length=254, unique=True)
    first_name = models.CharField(_("Имя"), max_length=150, blank=True)
    last_name = models.CharField(_("Фамилия"), max_length=150, blank=True)
    bio = models.TextField(
        _("Биография"), blank=True, help_text="Опишите биографию пользователя."
    )
    role = models.CharField(
        _("Статус пользователя"),
        max_length=128,
        choices=ROLE_CHOICES,
        default=USER,
        help_text=(
            "Выберите статус пользователя. Дефолт - user. "
            "От выбора зависят его права."
        ),
    )
    is_active = models.BooleanField(
        _("Активный/неактивный."),
        default=True,
        help_text=_("Статус текущего аккаунта - активирован или нет."),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_("Является ли пользователь суперюзером."),
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
    objects = UserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("username",)

    def __str__(self):
        return self.username[:MAX_LENGTH]


class Auth(models.Model):
    """Сохранение кодов подтверждения при регистрации."""

    user = models.OneToOneField(
        User,
        verbose_name=_("Пользователь"),
        help_text=_("Инстанс связанного юзера."),
        on_delete=models.CASCADE,
        unique=True,
        related_name="auth",
    )
    confirmation_code = models.CharField(
        max_length=128,
        verbose_name=_("Код подтверждения"),
        help_text=_("Код подтверждения с почты."),
    )
