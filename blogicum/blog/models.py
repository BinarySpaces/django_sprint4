from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class PublishedModel(models.Model):
    """Базовая модель."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Location(PublishedModel):
    """Местоположение."""

    name = models.CharField(
        'Название места',
        max_length=256,
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return str(self.name[:20])


class Category(PublishedModel):
    """Категория."""

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.title[:20])


class Post(PublishedModel):
    """Публикация."""

    title = models.CharField('Заголовок', max_length=256,)
    text = models.TextField('Текст',)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.',
    )
    image = models.ImageField(
        'Фото к постам',
        upload_to='posts_images',
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return str(self.title[:20])


class Comment(models.Model):
    """Комментарий."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.text)
