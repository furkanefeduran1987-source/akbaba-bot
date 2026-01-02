import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Bilgilerin (Bunları kontrol et kanka)
TRLINK_API_KEY = "510ed1f00db22c48ddbf17cd2b7d3fa293f24d9c"
BOT_TOKEN = "8569206431:AAGp49qmrVpjmEBdIr_1osDlHjnHvtNUxQ8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🚀 Bot Hazır! Linkini bekliyorum kanka.")

@dp.message(F.text.startswith("http"))
async def link_handler(message: types.Message):
    uzun_link = message.text
    api_url = f"https://tr.link/api?api={TRLINK_API_KEY}&url={uzun_link}"
    
    try:
        # User-agent ekleyerek kendimizi tarayıcı gibi tanıtıyoruz
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(api_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                await message.answer(f"✅ **Linkin:** {data['shortenedUrl']}")
            else:
                await message.answer(f"❌ TR.Link Hatası: {data.get('message', 'Bilinmiyor')}")
        else:
            await message.answer(f"⚠️ TR.Link Sunucusu Cevap Vermiyor (Kod: {response.status_code})")
            
    except Exception as e:
        await message.answer(f"⚠️ Bağlantı hatası detayı: {str(e)[:50]}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

