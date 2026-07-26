# STTCLI Project Guide

## What it does
CLI-инструмент для Windows: MP3 → Yandex STT v3 (распознавание с диаризацией спикеров) → LLM-нормализация (YandexGPT) → WSL-диаризация → diamix-слияние → опционально LLM-анализ (суммаризация, ADR, cost-estimate и т.д.)

## Key files

| File | Role |
|---|---|
| `sttcli.ps1` | Главный оркестратор: вызов STT → backup → normalize → wait WSL diarization → diamix |
| `sttcli.py` | STT-пайплайн: загрузка в S3 → Yandex STT v3 async → парсинг JSONL → сохранение .txt |
| `pipcli.py` | LLM-пайплайн: читает текст → chunk_summarize → join (если >1 chunk и не normalize) |
| `recognize/yandex.py` | Yandex STT v3: `recognizeFileAsync` → polling каждые 10с → `getRecognition` |
| `models/base.py` | Базовый суммаризатор: `chunk_text()` (60K символов) → `chunk_summarize()` → join |
| `models/yandex.py` | YandexGPT через OpenAI SDK (model из config: `yandexgpt-pro`) |
| `formats/format_asr.py` | Парсинг JSONL из STT → форматированный диалог с таймстемпами |
| `files/upload.py` | S3 upload в Yandex Object Storage |
| `instruction/choose.py` | Меню выбора инструкции (normalize, summarize, cost_estimate, bp_analize...) |

## Flow (MP3)

1. `sttcli.ps1` → проверка/конвертация в моно (ffmpeg) → активация .venv
2. Запуск WSL-диаризации в фоне (Start-Job)
3. `sttcli.py` → upload → recognize → parse → save .txt (с сырым STT)
4. `pipcli.py normalize` → LLM-нормализация, перезаписывает output.txt
5. **backup** `output.txt` → `output.txt.bak` (нормализованный текст перед diamix)
6. Wait WSL job → `run_diamix.ps1` (слияние диаризации в нормализованный текст)

## Fixed issues

1. **Backup после normalize**: backup перемещён ПОСЛЕ normalize (сохраняет нормализованный текст перед diamix-слиянием) в `sttcli.ps1:122-125`.
2. **Chunking 60K**: `chunk_text()` увеличен с 30K до 60K символов — с учётом 16K лимита `max_output_tokens`. YandexGPT Pro держит 32K токенов (60K входа + ~60K выхода укладываются в контекст).
3. **Модель из config**: `models/yandex.py` больше не хардкодит `yandexgpt/rc`, а читает `yandex.model` из `config.yml`.

## Config
- `config.yml` — модель, API-ключи, инструкции
- `model_name: yandex` — какая модель используется для LLM
- `yandex.model` — `yandexgpt-pro`
- `instructions.normalize` — промпт для нормализации (строгое требование: кол-во строк = вход)

## LLM Models
- `yandex` — YandexGPT (OpenAI-compatible SDK)
- `gigachat` — GigaChat (официальный SDK)
- `deepseek` — DeepSeek (REST API)