# Тестовый плагин для изучения архитектуры
# author: Anton Aliabev

import os
from vacore import VACore

# Получаем имя модуля
modname = os.path.basename(__file__)[:-3]

def start(core: VACore):
    """Инициализация плагина при запуске"""
    manifest = {
        'name': 'Тестовый плагин',
        'version': '1.0',
        'require_online': False,
        'description': 'Простой тестовый плагин для изучения архитектуры',
        'default_options': {
            'is_active': True,
            'test_message': 'Тестовый плагин работает!'
        },
        'commands': {
            'тест|привет|тестовый плагин': test_function,
            'как дела|как дела у ирины': how_are_you,
            'время|который час': get_time,
        }
    }
    return manifest

def start_with_options(core: VACore, manifest: dict):
    """Инициализация плагина с опциями"""
    options = manifest["options"]
    
    if not options["is_active"]:
        manifest["commands"] = {}
        return manifest
    
    return manifest

def test_function(core: VACore, phrase: str):
    """Простая тестовая функция"""
    options = core.plugin_options(modname)
    message = options.get("test_message", "Тестовый плагин работает!")
    core.play_voice_assistant_speech(message)
    print(f"Тестовая функция вызвана с фразой: {phrase}")

def how_are_you(core: VACore, phrase: str):
    """Функция для проверки состояния системы"""
    core.play_voice_assistant_speech("У меня все отлично! Я готова помогать вам с музыкой и умным домом.")
    print("Пользователь спросил как дела")

def get_time(core: VACore, phrase: str):
    """Функция для получения времени"""
    from datetime import datetime
    current_time = datetime.now().strftime("%H:%M")
    core.play_voice_assistant_speech(f"Сейчас {current_time}")
    print(f"Запрошено время: {current_time}")
