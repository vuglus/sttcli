import os
import shutil
from rich.console import Console
from rich.markdown import Markdown

CONTEXT_FILE = "context.md"
CONTEXT_PREFIX = "\n There is context you can use: \n"

def _get_context_path(base_file: str) -> str:
    """
    Возвращает путь к context.txt рядом с обрабатываемым файлом.
    """
    folder = os.path.dirname(os.path.abspath(base_file))
    return os.path.join(folder, CONTEXT_FILE)


def load_context_for(target_project_file: str) -> str:
    """
    Загружает контекст из context.txt, находящегося рядом с target_project_file.
    """
    source_path = _get_context_path(target_project_file)

    if os.path.exists(source_path):
        with open(source_path, "r", encoding="utf-8") as f:
            return CONTEXT_PREFIX + f.read()

    return ""

def draw_context(context: str):
    console = Console()

    # выводим рамку и заголовок
    console.print("═══════════════════════════════════════════════", style="cyan")
    console.print("              📌  ACTIVE CONTEXT", style="bold cyan")
    console.print("═══════════════════════════════════════════════\n", style="cyan")

    # создаем Markdown объект
    md = Markdown(context)
    # выводим красиво
    console.print(md)

    console.print("\n═══════════════════════════════════════════════", style="cyan")
    