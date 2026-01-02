import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Bilgilerin
TRLINK_API_KEY = "510ed1f00db22c48ddbf17cd2b7d3fa293f24d9c"
BOT_TOKEN = "8569206431:AAGp49qmrVpjmEBdIr_1osDlHjnHvtNUxQ8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🚀 Akbaba Bot Aktif! Linkini gönder kanka.
    insta ffurk4an ismi eylül olanlar eklesin ")

@dp.message(F.text.startswith("http"))
async def link_handler(message: types.Message):
    uzun_link = message.text
    # API URL'sini alternatif bir formatta deniyoruz
    api_url = f"https://tr.link/api?api={TRLINK_API_KEY}&url={uzun_link}"
    
    try:
        # Kendimizi gerçek bir kullanıcı gibi gösteriyoruz
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # requests.get yerine requests.post veya farklı bir yöntem deniyoruz
        response = requests.get(api_url, headers=headers, timeout=20)
        
        # Eğer site JSON değil de hata sayfası dönerse bunu anlamamızı sağlar
        try:
            data = response.json()
            if data.get("status") == "success":
                await message.answer(f"✅ **Linkin:** {data['shortenedUrl']}")
            else:
                await message.answer(f"❌ TR.Link: {data.get('message', 'API Hatası')}")
        except:
            # Burası o meşhur hatayı yakaladığımız yer
            await message.answer("⚠️ TR.Link şu an bu sunucuyu (Render) engelledi. Birkaç dakika sonra tekrar dene kanka.")
            
    except Exception as e:
        await message.answer(f"⚠️ Bağlantı hatası: {str(e)[:30]}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
