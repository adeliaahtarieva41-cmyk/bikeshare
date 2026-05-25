import requests
import json
from django.conf import settings


def ask_gpt(prompt):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_GPT_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{settings.YANDEX_GPT_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 500
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    # Отладка: выводим JSON перед отправкой
    print(f"Отправляемый JSON: {json.dumps(data, ensure_ascii=False)}")

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Статус ответа: {response.status_code}")
        print(f"Ответ: {response.text}")

        if response.status_code == 200:
            result = response.json()
            return result['result']['alternatives'][0]['message']['text']
        else:
            return f"Ошибка API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Ошибка: {str(e)}"