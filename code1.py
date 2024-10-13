import json
from mongoengine import Document, StringField, ReferenceField, ListField, connect
from mongoengine.errors import DoesNotExist

# Підключення до бази даних MongoDB Atlas
connect(host="your_mongo_atlas_connection_string")


# Модель для авторів
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


# Модель для цитат
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule="CASCADE")
    quote = StringField(required=True)


# Завантаження авторів із файлу authors.json
def load_authors():
    with open("authors.json", "r", encoding="utf-8") as f:
        authors_data = json.load(f)

    for author_data in authors_data:
        author = Author(
            fullname=author_data["fullname"],
            born_date=author_data.get("born_date"),
            born_location=author_data.get("born_location"),
            description=author_data.get("description"),
        )
        author.save()


# Завантаження цитат із файлу qoutes.json
def load_quotes():
    with open("qoutes.json", "r", encoding="utf-8") as f:
        quotes_data = json.load(f)

    for quote_data in quotes_data:
        try:
            author = Author.objects.get(fullname=quote_data["author"])
            quote = Quote(
                tags=quote_data["tags"], author=author, quote=quote_data["quote"]
            )
            quote.save()
        except DoesNotExist:
            print(f"Author {quote_data['author']} not found.")


# Пошук цитат
def search_quotes():
    while True:
        command = input("Введіть команду (name, tag, tags або exit): ").strip()

        if command.startswith("name:"):
            name = command.split("name:")[1].strip()
            author = Author.objects(fullname=name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Автор не знайдений.")

        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.quote)

        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)

        elif command == "exit":
            break

        else:
            print("Невідома команда.")


# Основна функція для запуску
if __name__ == "__main__":
    # Завантажуємо авторів і цитати у базу даних (викликайте ці функції лише один раз)
    # load_authors()  # Використовуйте цей рядок, щоб один раз завантажити авторів
    # load_quotes()   # Використовуйте цей рядок, щоб один раз завантажити цитати

    # Запускаємо пошук цитат
    search_quotes()
