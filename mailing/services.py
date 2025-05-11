from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, SendAttempt


def start_mailing(mailing_id):
    """ Запускает рассылку по её ID """
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        message_obj = mailing.message

        # Получаем данные из связанной модели Message
        topic = message_obj.topic
        plain_message = message_obj.letter  # Используем поле 'letter' вместо общего 'message'

        # Обновляем статус рассылки ДО отправки
        mailing.status = 'Запущена'
        mailing.save()

        # Отправка писем всем получателям
        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    subject=topic,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],  # Используем email конкретного получателя
                    fail_silently=False
                )
                # Логируем успешную попытку
                SendAttempt.objects.create(
                    status='Успешно',
                    mailing=mailing,
                    server_response="OK"
                )
            except Exception as e:
                # Логируем ошибку
                SendAttempt.objects.create(
                    status='Не успешно',
                    mailing=mailing,
                    server_response=str(e)
                )

        return True, "Рассылка успешно запущена"

    except Mailing.DoesNotExist:
        return False, "Рассылка не найдена"

    except Exception as e:
        # Общая ошибка (например, проблемы с SMTP)
        return False, f"Критическая ошибка: {str(e)}"