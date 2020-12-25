from django.db import models


class Post(models.Model):
    title = models.CharField('Название', max_length=150)
    Anons = models.CharField('Анонс', max_length=250)
    image = models.ImageField('Путь_Фотки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.post


class PlayCity(models.Model):
    user_word = models.CharField('Слово пользователя', max_length=150, null=True)
    bot_word = models.CharField('Слово Бота', max_length=250, null=True)
    error_user_word = models.CharField('Не правильное слово', max_length=250, null=True)
    count_word = models.IntegerField('Количество слов', null=True)
    error_start_word = models.CharField('Начинается не с той буквы', max_length=250, null=True)

    def __str__(self):
        return self.user_word

    class Meta:
        verbose_name = 'Игра в города'
        verbose_name_plural = 'Игра в города'


class Actor(models.Model):
    name = models.CharField('Артист', max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Films(models.Model):
    film = models.CharField('Фильм', max_length=250)

    def __str__(self):
        return self.film

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class ListFilmsActor(models.Model):
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    id_film = models.ForeignKey(Films, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.id_actor, self.id_film)

    class Meta:
        verbose_name = 'Список фильмов и актеров'
        verbose_name_plural = 'Список фильмов и актеров'