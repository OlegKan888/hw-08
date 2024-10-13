import pika
import json
import mongoengine as me
from models import Contact

# Підключаємося до MongoDB
me.connect("email_queue_db")  # Замінити на свій MongoDB


# Імітація функції відправки email (заглушка)
def send_email_stub(contact):
    print(f"Імітація відправки email на адресу {contact.email}")
    return True  # Імітація успішної відправки


# Функція для обробки повідомлень з RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get("contact_id")

    # Знаходимо контакт за ID в MongoDB
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.sent:
        if send_email_stub(contact):
            # Оновлюємо поле sent на True
            contact.sent = True
            contact.save()
            print(
                f"Email відправлено для контакту {contact.fullname} ({contact.email})"
            )
        else:
            print(f"Не вдалося відправити email для {contact.fullname}")
    else:
        print(f"Контакт з ID {contact_id} не знайдено або email вже відправлено")


# Налаштовуємо RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Декларуємо чергу
channel.queue_declare(queue="email_queue")

# Налаштовуємо споживання повідомлень
channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print("Очікування повідомлень...")
channel.start_consuming()
