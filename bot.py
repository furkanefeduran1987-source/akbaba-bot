import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Bilgileri Render ayarlarından veya direkt buradan alıyoruz
BOT_TOKEN = os.getenv("BOT_TOKEN", "8569206431:AAGp49qmrVpjmEBdIr_1osDlHjnHvtNUxQ8")
TRLINK_API_KEY = "510ed1f00db22c48ddbf17cd2b7d3fa293f24d9c"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🚀 Akbaba Bot Render'da canlandı! Link gönder kanka, hemen kısaltayım.")

@dp.message(F.text.startswith("http"))
async def link_handler(message: types.Message):
    uzun_link = message.text
    api_url = f"https://tr.link/api?api={TRLINK_API_KEY}&url={uzun_link}"
    try:
        response = requests.get(api_url, timeout=30)
        data = response.json()
        if data.get("status") == "success":
            await message.answer(f"✅ **Linkin Hazır:**\n{data['shortenedUrl']}")
        else:
            await message.answer("❌ TR.Link bir hata verdi, API anahtarını kontrol etmelisin.")
    except:
        await message.answer("⚠️ Bağlantı hatası oluştu.")

async def main():
    # Eski bağlantıları temizle ve botu başlat
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
