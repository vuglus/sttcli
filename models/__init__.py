from .gigachat import GigaChatSummarizer
from .local import LocalSummarizer
from .deepseek import DeepSeekSummarizer
from .yandex import YandexGPTSummarizer

# Реестр моделей
_models = {
    "gigachat": GigaChatSummarizer,
    "yandex": YandexGPTSummarizer,
    "local": LocalSummarizer,
    "deepseek": DeepSeekSummarizer
}

def get_model(model: str):
    return _models.get(model)
