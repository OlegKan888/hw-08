
import mongoengine as me


class Contact(me.Document):
    fullname = me.StringField(required=True)
    email = me.EmailField(required=True)
    sent = me.BooleanField(default=False)  # False - якщо email не надіслано
