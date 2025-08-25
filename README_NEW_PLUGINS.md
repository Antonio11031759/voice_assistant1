# 🎯 Новые плагины для Irene Voice Assistant

## 🚀 Что добавлено

В проект Irene Voice Assistant добавлены три новых плагина для расширения функциональности:

### 1. 🧪 **Тестовый плагин** (`plugin_test.py`)
- Простой плагин для изучения архитектуры
- Базовые команды для тестирования системы
- Пример структуры плагина

### 2. 🎵 **Spotify интеграция** (`plugin_spotify.py`)
- Управление музыкой через Spotify API
- Воспроизведение, пауза, переключение треков
- Поиск и воспроизведение музыки по голосу

### 3. 🏠 **Home Assistant интеграция** (`plugin_homeassistant.py`)
- Управление умным домом
- Контроль освещения, температуры, влажности
- Готовые сценарии (подготовка ко сну, уход из дома)

## 📁 Структура файлов

```
Irene-Voice-Assistant-master/
├── plugins/
│   ├── plugin_test.py           # Тестовый плагин
│   ├── plugin_spotify.py        # Spotify интеграция
│   └── plugin_homeassistant.py  # Home Assistant интеграция
├── options/
│   ├── test.json                # Конфигурация тестового плагина
│   ├── spotify.json             # Конфигурация Spotify
│   └── homeassistant.json       # Конфигурация Home Assistant
├── docs/
│   └── PLUGINS_SETUP.md         # Подробная документация
├── test_plugins.py              # Скрипт тестирования
└── README_NEW_PLUGINS.md        # Этот файл
```

## ⚡ Быстрый старт

### 1. Проверка готовности
```bash
python test_plugins.py
```

### 2. Настройка Spotify
1. Создайте приложение на [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Получите `Client ID` и `Client Secret`
3. Отредактируйте `options/spotify.json`
4. Получите `auth_code` через браузер

### 3. Настройка Home Assistant
1. Создайте Long-Lived Access Token в Home Assistant
2. Отредактируйте `options/homeassistant.json`
3. Укажите URL вашего Home Assistant сервера

### 4. Запуск системы
```bash
python runva_webapi.py
```

## 🎮 Доступные команды

### Тестовый плагин
- `тест` - простая тестовая команда
- `как дела` - проверка состояния системы  
- `время` - получение текущего времени

### Spotify
- `включи музыку` - включить/поставить на паузу
- `следующий трек` - следующий трек
- `предыдущий трек` - предыдущий трек
- `поставь трек [название]` - поиск и воспроизведение
- `статус музыки` - что сейчас играет

### Home Assistant
- `включи свет` - включить основное освещение
- `выключи свет` - выключить все источники света
- `включи свет в [комнате]` - включить свет в комнате
- `температура дома` - получить температуру
- `влажность дома` - получить влажность
- `готовлюсь ко сну` - сценарий подготовки ко сну
- `ухожу из дома` - сценарий ухода из дома

## 🔧 Настройка

### Spotify
```json
{
    "is_active": true,
    "client_id": "ваш_client_id",
    "client_secret": "ваш_client_secret",
    "redirect_uri": "http://localhost:5003/spotify_callback",
    "auth_code": "полученный_auth_code"
}
```

### Home Assistant
```json
{
    "is_active": true,
    "base_url": "http://localhost:8123",
    "access_token": "ваш_access_token",
    "default_room": "гостиная"
}
```

## 🧪 Тестирование

### Запуск тестов
```bash
python test_plugins.py
```

### Проверка через веб-интерфейс
1. Откройте `http://localhost:5003`
2. Используйте веб-клиент для тестирования команд
3. Проверьте логи на наличие ошибок

## 📚 Документация

- **Подробная настройка**: `docs/PLUGINS_SETUP.md`
- **Архитектура плагинов**: изучите существующие плагины в папке `plugins/`
- **API документация**: 
  - [Spotify Web API](https://developer.spotify.com/documentation/web-api)
  - [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

## 🐛 Устранение неполадок

### Spotify не работает
- Проверьте правильность `client_id` и `client_secret`
- Убедитесь, что `auth_code` получен и вставлен
- Проверьте `redirect_uri` в настройках Spotify

### Home Assistant не подключается
- Проверьте доступность Home Assistant по указанному URL
- Убедитесь в правильности `access_token`
- Проверьте права доступа токена

### Общие проблемы
- Запустите `test_plugins.py` для диагностики
- Проверьте логи системы
- Убедитесь, что все зависимости установлены

## 🚀 Разработка

### Создание нового плагина
1. Изучите структуру существующих плагинов
2. Создайте файл `plugin_имя.py`
3. Реализуйте функции `start()` и `start_with_options()`
4. Создайте конфигурационный файл в `options/`
5. Протестируйте через `test_plugins.py`

### Структура плагина
```python
def start(core: VACore):
    manifest = {
        'name': 'Название плагина',
        'version': '1.0',
        'require_online': True,
        'commands': {
            'команда|альтернатива': функция_обработчик,
        }
    }
    return manifest

def функция_обработчик(core: VACore, phrase: str):
    core.play_voice_assistant_speech("Ответ пользователю")
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи системы
2. Запустите `test_plugins.py`
3. Изучите документацию в `docs/PLUGINS_SETUP.md`
4. Проверьте настройки конфигурационных файлов

## 🎉 Результат

После настройки у вас будет:
- ✅ Работающий голосовой помощник с русским языком
- ✅ Управление музыкой через Spotify
- ✅ Контроль умного дома через Home Assistant
- ✅ Расширяемая система плагинов
- ✅ Веб-интерфейс для управления

**Готово к использованию! 🚀**
