import os
import discord
from discord.ext import commands


import openai
import discord
from discord.ext import commands

# OpenAI API anahtarı ve Discord bot token'ı
openai.api_key = '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'

# Discord bot token'ı
# Discord Intents ayarı
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='kodland!', intents=intents)

# Sohbet oturumu için bir dictionary yapısı.
chat_sessions = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='chat')
async def chat(ctx, *, message):
    user_id = str(ctx.author.id)

    # Kullanıcının mevcut oturum ID'sini al.
    session_id = chat_sessions.get(user_id)

    # Kullanıcının mesajı ile bir mesaj listesi oluştur.
    messages = [
        {"role": "system", "content": "senin adın Kodland Canlı Destek ve yardım sever bir asistansın, birisi sana adını sorduğunda adım Kodland Canlı Destek Demelisin"},
        {"role": "user", "content": message}
    ]

    # ChatCompletion çağrısı yaparken session_id varsa ekleyin.
    chat_params = {
        "model": "gpt-4",
        "messages": messages
    }

    if session_id:
        chat_params["session_id"] = session_id

    # ChatCompletion çağrısı.
    response = openai.ChatCompletion.create(**chat_params)

    # Cevabı ve yeni oturum ID'sini kaydet.
    # 'choices' içerisinden 'data' ve oradan da 'session_id' anahtarına ulaşılır.
    if 'data' in response['choices'][0]:
        chat_sessions[user_id] = response['choices'][0]['data']['session_id']
    else:
        # İlk yanıtta session_id yoksa, bu bir başlangıç yanıtıdır ve oturum ID'si henüz oluşturulmamış olabilir.
        # Bu durumda, bu kullanıcı için henüz bir session_id yok demektir.
        pass

    answer = response['choices'][0]['message']['content']

    # Gelen yanıtı Discord'da gönder.
    await ctx.send(answer)

# Botu çalıştır.
bot.run("MTE3MDcyMjQwOTI0Mjk1MTgxMg.GS7Gp8.LlSvYCtKB8cp1tK05Yne9LOD9YDfB0F_jiSBsQ")

