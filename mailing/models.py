from django.db import models


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.', help_text='Введите получателя')
    email = models.EmailField(max_length=100, verbose_name='Email ', help_text='Введите Email', unique=True)
    comment = models.TextField(max_length=250, verbose_name='комментарий', help_text='Введите комментарий')


    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['full_name']

class Message(models.Model):
    topic = models.TextField(max_length=100, verbose_name='тема', help_text='Введите тему') # тема письма
    letter = models.TextField(verbose_name='сообщение', help_text='Введите сообщение')      # тело письма

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        ordering = ['topic']


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена')
    ]

    first_sent_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана')
    # Статус строка: 'Завершена','Создана','Запущена'
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client)

    def __str__(self):
        return f"{self.message.topic} - {self.status}"

    class Meta:
        verbose_name = 'Расссылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['status']


class SendAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно')
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    # Статус строка: 'Завершена','Создана','Запущена'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # Ответ почтового сервера (текст)
    server_response = models.TextField(blank=True)
    # Рассылка (внешний ключ на модель «Рассылка»)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='send_attempts')


    def __str__(self):
        return f"Attempt: {self.attempt_time} - {self.status}"

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
        ordering = ['status']

