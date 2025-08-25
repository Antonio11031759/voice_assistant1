#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки работы новых плагинов
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vacore import VACore

def test_core_initialization():
    """Тест инициализации ядра"""
    print("🧪 Тестирование инициализации ядра...")
    
    try:
        core = VACore()
        print("✅ Ядро успешно создано")
        return core
    except Exception as e:
        print(f"❌ Ошибка создания ядра: {e}")
        return None

def test_plugin_loading(core):
    """Тест загрузки плагинов"""
    print("\n🧪 Тестирование загрузки плагинов...")
    
    try:
        # Инициализируем плагины
        core.init_with_plugins()
        print("✅ Плагины успешно инициализированы")
        
        # Проверяем загруженные команды
        if core.commands:
            print(f"✅ Загружено команд: {len(core.commands)}")
            for cmd in list(core.commands.keys())[:5]:  # Показываем первые 5
                print(f"   - {cmd}")
        else:
            print("⚠️ Команды не загружены")
            
        return True
    except Exception as e:
        print(f"❌ Ошибка загрузки плагинов: {e}")
        return False

def test_plugin_commands(core):
    """Тест выполнения команд плагинов"""
    print("\n🧪 Тестирование выполнения команд...")
    
    test_commands = [
        "тест",
        "как дела",
        "время"
    ]
    
    for cmd in test_commands:
        try:
            print(f"🔍 Тестирую команду: '{cmd}'")
            if cmd in core.commands:
                print(f"   ✅ Команда найдена")
                # Выполняем команду
                core.execute_next(cmd, None)
            else:
                print(f"   ❌ Команда не найдена")
        except Exception as e:
            print(f"   ❌ Ошибка выполнения: {e}")

def test_spotify_plugin():
    """Тест Spotify плагина"""
    print("\n🧪 Тестирование Spotify плагина...")
    
    try:
        # Импортируем плагин
        from plugins.plugin_spotify import start, SpotifyAPI
        
        # Тестируем создание API
        api = SpotifyAPI("test_id", "test_secret", "http://localhost:5003/callback")
        print("✅ Spotify API класс создан")
        
        # Тестируем manifest
        manifest = start(None)
        print(f"✅ Spotify плагин manifest: {manifest['name']}")
        print(f"   Команды: {len(manifest['commands'])}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка Spotify плагина: {e}")
        return False

def test_homeassistant_plugin():
    """Тест Home Assistant плагина"""
    print("\n🧪 Тестирование Home Assistant плагина...")
    
    try:
        # Импортируем плагин
        from plugins.plugin_homeassistant import start, HomeAssistantAPI
        
        # Тестируем создание API
        api = HomeAssistantAPI("http://localhost:8123", "test_token")
        print("✅ Home Assistant API класс создан")
        
        # Тестируем manifest
        manifest = start(None)
        print(f"✅ Home Assistant плагин manifest: {manifest['name']}")
        print(f"   Команды: {len(manifest['commands'])}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка Home Assistant плагина: {e}")
        return False

def test_config_files():
    """Тест конфигурационных файлов"""
    print("\n🧪 Тестирование конфигурационных файлов...")
    
    config_files = [
        "options/test.json",
        "options/spotify.json", 
        "options/homeassistant.json"
    ]
    
    for config_file in config_files:
        try:
            if os.path.exists(config_file):
                print(f"✅ {config_file} - найден")
                
                # Проверяем, что это валидный JSON
                with open(config_file, 'r', encoding='utf-8') as f:
                    import json
                    config = json.load(f)
                    print(f"   JSON валиден, ключи: {list(config.keys())}")
            else:
                print(f"❌ {config_file} - не найден")
        except Exception as e:
            print(f"❌ Ошибка чтения {config_file}: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования новых плагинов Irene Voice Assistant")
    print("=" * 60)
    
    # Тест 1: Инициализация ядра
    core = test_core_initialization()
    if not core:
        print("❌ Не удалось инициализировать ядро. Тестирование прервано.")
        return
    
    # Тест 2: Загрузка плагинов
    if not test_plugin_loading(core):
        print("❌ Не удалось загрузить плагины. Тестирование прервано.")
        return
    
    # Тест 3: Выполнение команд
    test_plugin_commands(core)
    
    # Тест 4: Spotify плагин
    test_spotify_plugin()
    
    # Тест 5: Home Assistant плагин
    test_homeassistant_plugin()
    
    # Тест 6: Конфигурационные файлы
    test_config_files()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование завершено!")
    print("\n📋 Следующие шаги:")
    print("1. Настройте конфигурационные файлы в папке options/")
    print("2. Получите API ключи для Spotify и Home Assistant")
    print("3. Запустите систему: python runva_webapi.py")
    print("4. Протестируйте команды через веб-интерфейс")

if __name__ == "__main__":
    main()
