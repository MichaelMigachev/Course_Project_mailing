from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailing.models import Mailing, SendAttempt


class MailingService:
    @staticmethod
    def send_mailing(mailing):
        """
        Отправляет рассылку и создает записи о попытках отправки
        """
        if not hasattr(mailing, 'message'):
            print(f'Рассылка {mailing.id} не имеет сообщения')
            return

        recipients = mailing.recipients.all()
        successful_attempts = 0

        for recipient in recipients:
            try:
                # Отправка письма с использованием правильных полей
                send_mail(
                    subject=mailing.message.topic,  # Поле 'topic' для темы
                    message=mailing.message.letter,  # Поле 'letter' для текста
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False
                )

                # Логируем успешную попытку
                SendAttempt.objects.create(
                    mailing=mailing,
                    status="Успешно",
                    server_response="Сообщение успешно отправлено",
                )
                successful_attempts += 1

                print(f'Сообщение "{mailing.message.topic}" отправлено клиенту {recipient.email}')

            except Exception as e:
                # Логируем неудачную попытку
                SendAttempt.objects.create(
                    mailing=mailing,
                    status="Не успешно",
                    server_response=str(e),
                )
                print(f'Ошибка при отправке клиенту {recipient.email}: {str(e)}')

        # Обновляем статус рассылки
        if successful_attempts > 0:
            mailing.status = "Завершена"
            if not mailing.first_sent_at:
                mailing.first_sent_at = timezone.now()
            mailing.save()


class Command(BaseCommand):
    help = 'Запуск рассылок'

    def handle(self, *args, **options):
        # Получаем активные рассылки
        current_time = timezone.now()
        mailings = Mailing.objects.filter(
            is_activated=True,
            status__in=["Создана", "Запущена"],
            end_at__gte=current_time  # Только рассылки, у которых не истек срок
        ).select_related('message')  # Оптимизация запроса

        for mailing in mailings:
            # Проверяем, что время рассылки наступило
            if mailing.first_sent_at is None or mailing.first_sent_at <= current_time:
                mailing.status = "Запущена"
                mailing.save()
                MailingService.send_mailing(mailing)
