# Public YouTube Uploader Telegram Bot

Bot Telegram orqali yuborilgan videolarni YouTube kanaliga `public` holatida upload qiladi. Kanal: https://www.youtube.com/@fazauc_anime


## Eslatma
- Telegram Bot API orqali bot videolarni yuklab olishi uchun fayl hajmi odatda 20 MB gacha cheklangan. Kattaroq videolar uchun Telegram Local Bot API serveri yoki boshqa transfer usuli kerak.
- YouTube OAuth `credentials.json` va yaratiladigan `token.json` fayllarini GitHub'ga yuklamang.
- YouTube API loyihasi audit/verification holatiga qarab, API orqali yuklangan videolar `private` holatda qolishi mumkin; `public` qilib yuborish hamma yangi API loyihalarida avtomatik ruxsat etilmasligi mumkin. Kanal sozlamalari va Google API limit/verification talablarini tekshiring.

## 1) Python
Python 3.11+ o'rnating.

## 2) Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

## 3) Telegram sozlash
`.env.example` dan `.env` nusxa yarating va `TELEGRAM_BOT_TOKEN` hamda `OWNER_TELEGRAM_ID` qiymatlarini to'ldiring.

## 4) YouTube API OAuth
1. Google Cloud Console'da project yarating.
2. YouTube Data API v3 ni yoqing.
3. OAuth consent screen sozlang.
4. OAuth Client ID yarating (Desktop app) va JSON'ni `credentials.json` nomi bilan loyiha papkasiga saqlang.
5. Terminalda `python auth_youtube.py` bajaring va kerakli YouTube kanal akkauntiga login/ruxsat bering.

## 5) Botni ishga tushirish
```bash
python main.py
```
Telegram botga video yuboring. Caption:
- 1-qator: sarlavha
- keyingi qatorlar: description

Caption bo'lmasa, video fayl nomidan sarlavha olinadi.
