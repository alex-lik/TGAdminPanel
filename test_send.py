import requests

# --- НАСТРОЙКИ ---
# Замените на ваш токен бота
BOT_TOKEN = "7723270954:AAFooFxb46jA6EqUXkllrRYeoUaPMG-txJE"
# Замените на ID вашего канала. Для числовых ID кавычки не нужны.
# Пример для публичного канала: CHANNEL_ID = "@your_channel_name"
# Пример для частного канала: CHANNEL_ID = -1001234567890
CHANNEL_ID = -397262379

# --- СООБЩЕНИЕ ---
html_message = """<b>Робота з пакетами: requirements.txt lock 🧾</b>

<i>Фіксація версій залежностей критична для відтворюваності проекту. Requirements.txt — базовий спосіб "заморозити" стан пакетів.</i>

<b>Створення requirements.txt</b>
• Вручну: перелічуємо пакети та версії
• Автоматично: pip freeze &gt; requirements.txt
• З хешами: pip hash -r requirements.txt
• Рекомендований формат:
<pre><code>requests==2.31.0
python-dotenv&gt;=0.19.0,&lt;1.0.0
pytest~=7.4.0  # сумісні мінорні</code></pre>

<b>Типи фіксації версій</b>
• == точна версія (найнадійніший)
• &gt;= мінімальна версія (ризиковано)
• ~= сумісні мінорні (компроміс)
• != виключити версію
• [extras] додаткові фічі

<b>Поради щодо роботи</b>
• Розділяйте основні та dev-залежності
• Використовуйте constraints.txt для конфліктів
• Перевіряйте сумісність перед фіксацією
• Регулярно оновлюйте з урахуванням безпеки
• Тримайте в git разом з кодом

💡 Вправа:
Створіть віртуальне оточення, встановіть flask та requests різних версій, згенеруйте requirements.txt та спробуйте відтворити оточення в новій папці:

<pre><code>python -m venv env
source env/bin/activate  # або .envScriptsactivate
pip install flask==2.0.0 requests==2.31.0
pip freeze &gt; requirements.txt
deactivate
# Створіть нове оточення та встановіть
python -m venv env2
source env2/bin/activate
pip install -r requirements.txt</code></pre>"""

def send_telegram_message():
    """
    Отправляет сообщение в Telegram канал через прямое обращение к API с использованием requests.
    """
    if "YOUR_BOT_TOKEN" in BOT_TOKEN:
        print("Пожалуйста, укажите ваш BOT_TOKEN в файле test_send.py")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': CHANNEL_ID,
        'text': html_message,
        'parse_mode': 'HTML'
    }

    print(f"Отправка сообщения в канал {CHANNEL_ID}...")
    try:
        response = requests.post(url, json=params)
        # Печатаем ответ от сервера для диагностики
        print(f"Ответ от Telegram API: {response.text}")
        response.raise_for_status()  # Вызовет исключение для статусов 4xx/5xx

        result = response.json()
        if result.get("ok"):
            message_id = result["result"]["message_id"]
            print(f"Сообщение успешно отправлено! Message ID: {message_id}")
        else:
            print(f"Telegram API вернул ошибку: {result.get('description')}")
    except requests.exceptions.HTTPError as e:
        print(f"Произошла ошибка HTTP: {e}")
        print(f"Тело ответа: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при отправке запроса: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    send_telegram_message()