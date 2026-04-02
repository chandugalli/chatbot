from django.contrib import admin
from .models import ChatSession, Conversation

admin.site.register(ChatSession)
admin.site.register(Conversation)