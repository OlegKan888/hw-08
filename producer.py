import pika
import json
import mongoengine as me
from models import Contact
from faker import Faker

# Підключаємося до MongoDB
me.connect("email_queue_db")  # Замінити на свій MongoDB

# Налаштовуємо RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)  # RabbitMQ сервер
channel = connection.channel()
channel.queue_declare(queue="email_queue")

# Генеруємо фейкові контакти
fake = Faker()
num_contacts = 10  # Кількість контактів, які треба згенерувати

for _ in range(num_contacts):
    # Створюємо контакт
    contact = Contact(fullname=fake.name(), email=fake.email())
    contact.save()

    # Надсилаємо ObjectID контакту в чергу RabbitMQ
    message = json.dumps({"contact_id": str(contact.id)})
    channel.basic_publish(exchange="", routing_key="email_queue", body=message)
    print(f"Відправлено контакт {contact.fullname} з ID {contact.id}")

# Закриваємо з'єднання
connection.close()
