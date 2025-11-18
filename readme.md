# 🎙️ STTCLI — конвертация аудио → текст → саммари

Лёгкий CLI-инструмент для:
- загрузки аудио в Object Storage,
- распознавания речи через Yandex STT v3,
- получения диаризации (спикеры + таймкоды),
- аналитической обработки текста через YandexGPT / DeepSeek / локальные модели,
- выбора инструкции анализа через CLI или интерактивно.

---

## 🚀 Установка

```bash
git clone <repo>
cd sttcli
python3 -m venv sttcli
source sttcli/bin/activate
pip install -r requirements.txt
```
## Шаблон конфига 
config.yml.template

```yaml
yacloud:
  folder_id: "b1gxxx..."              # ID каталога
  oauth_token: "y0_AgAAA..."          # токен доступа
  bucket_name: "speech-uploads"       # бакет для временного хранения
  max_output: 2500                    # максимальный размер саммари

gpt:
  model: "yandexgpt-pro"
  temperature: 0.3

deepseek:
  api_key:

stt:
  language: "ru-RU"
  sample_rate: 48000
deepseek:
  api_key: "sk-..."
stt:
  language: "ru-RU"

instructions:
  default: "Ты помощник..."
  smart: "Сделай глубокий анализ..."
  short: "Дай краткое саммари..."
```

Вариант 1 — указать инструкцию в CLI
python sttcli.py audio.mp3 smart

Вариант 2 — выбор инструкции в интерактиве
python sttcli.py audio.mp3


## Появится меню:

Выберите инструкцию анализа:
1. default
2. smart
3. short
Введите номер инструкции:

## 📦 Структура проекта

```text
sttcli/
├── sttcli.py               # основной CLI
├── stt_recognize.py        # распознавание Yandex STT v3
├── summarize/
│   ├── yandex.py           # YandexGPT
│   ├── deepseek.py         # DeepSeek
│   └── local.py            # локальные модели
├── utils/                  # helpers
├── config.yaml
└── requirements.txt
```

📝 Вывод диаризации (пример)
```
Спикер 2 ∙ 00:00 - 00:02
Вот эти файлы с Мепендом я тебе скину.

Спикер 1 ∙ 00:00 - 00:25
Какая нибудь?

Спикер 2 ∙ 00:02 - 00:08
Вот тебе не интересно, это Си Пи Эс заполняется полностью.
```
📄 Лицензия
- MIT — делай что хочешь, но не вини меня 🙂
