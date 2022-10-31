from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import (CHARFIELD_MAX_LENGTH, EMAIL_MAX_LENGTH,
                                NAME_MAX_LENGTH)

from .validators import validate_username, validate_year


class Roles(Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    @classmethod
    def get_roles(cls):
        return tuple((attribute.name, attribute.value) for attribute in cls)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=(validate_username,),
        max_length=NAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=CHARFIELD_MAX_LENGTH,
        choices=Roles.get_roles(),
        default=Roles.user.value,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=CHARFIELD_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=CHARFIELD_MAX_LENGTH,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == Roles.admin.value

    @property
    def is_moderator(self):
        return self.role == Roles.moderator.value

    def __str__(self) -> str:
        return self.username


class SimpleSlugModel(models.Model):
    '''Abstract model for common ancestor of Genres and Category.'''
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        unique=True, max_length=50, verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(SimpleSlugModel):
    '''Model of Genre'''
    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(SimpleSlugModel):
    '''Model of Category'''
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    '''Model for Titles.'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    year = models.IntegerField(validators=(validate_year,))
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    '''Model for connection of Titles and Genres.'''
    title_id = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f'Произведение номер {self.title_id},'
                f'жанр номер {self.genre_id}')


class BaseReviewCommentModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            '%(class)s'
            + f': автор {self.author}: '
            + f'{self.text}'[:15]
        )


class Review(BaseReviewCommentModel):
    '''Model for reviews of Titles by Users.'''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
        null=True
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                name="reviews_only_one_review_per_title",
                fields=["author", "title"],
            ),
        ]


class Comment(BaseReviewCommentModel):
    '''Model for Comments to Reviews by Users.'''
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
