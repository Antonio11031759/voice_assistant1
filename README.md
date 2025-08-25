# Голосовой ассистент Ирина

Ирина - русский голосовой ассистент для работы оффлайн и онлайн. Требует Python 3.7+ и поддерживает плагины (скиллы).

[Статья на Хабре](https://habr.com/ru/post/595855/) | [Вторая статья на Хабре](https://habr.com/ru/post/660715/) | [Третья статья на Хабре](https://habr.com/ru/articles/725066/) | [Группа в Телеграм](https://t.me/irene_va)

## 🚀 Быстрая установка на домашний сервер

### Требования
- **ОС**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+), Windows Server, macOS
- **Python**: 3.7 - 3.11 (рекомендуется 3.9)
- **RAM**: минимум 2GB, рекомендуется 4GB+
- **Диск**: минимум 1GB свободного места
- **Микрофон**: USB или встроенный (для голосового управления)

### 1. Подготовка системы

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git ffmpeg
sudo apt install -y portaudio19-dev python3-pyaudio  # для аудио
```

#### CentOS/RHEL:
```bash
sudo yum install -y python3 python3-pip git ffmpeg
sudo yum install -y portaudio-devel python3-pyaudio  # для аудио
```

#### Windows Server:
- Установите Python 3.9+ с [python.org](https://python.org)
- Установите Git с [git-scm.com](https://git-scm.com)
- Установите [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### 2. Клонирование и установка

```bash
# Клонируем репозиторий
git clone https://github.com/janvarev/Irene-Voice-Assistant.git
cd Irene-Voice-Assistant

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Устанавливаем зависимости
pip install -r requirements_fixed.txt
```

### 3. Первый запуск

```bash
# Запускаем ассистента
python runva_vosk.py
```

При первом запуске:
- Создастся папка `options` с настройками
- Скачается модель распознавания речи VOSK
- Появится сообщение "Ирина готова к работе"

### 4. Тестирование

Скажите в микрофон: **"Ирина, привет!"**

Должен последовать ответ: "Привет! Чем могу помочь?"

## ⚙️ Настройка для сервера

### Автозапуск (systemd)

Создайте файл `/etc/systemd/system/irene-va.service`:

```ini
[Unit]
Description=Irene Voice Assistant
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Irene-Voice-Assistant
Environment=PATH=/path/to/Irene-Voice-Assistant/venv/bin
ExecStart=/path/to/Irene-Voice-Assistant/venv/bin/python runva_vosk.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable irene-va
sudo systemctl start irene-va
sudo systemctl status irene-va
```

### Удаленное управление

Для управления с других устройств настройте веб-интерфейс:

```bash
# Запуск веб-API
python runva_webapi.py
```

По умолчанию доступен на `http://your_server_ip:8080`

## 🔧 Основные настройки

### Файл `options/core.json`

```json
{
    "voiceAssNames": "ирина|ирины|ирину",
    "ttsEngineId": "pyttsx",
    "playWavEngineId": "audioplayer",
    "isOnline": true,
    "log_console": true,
    "log_file": true,
    "log_file_name": "irene.log"
}
```

### Настройка плагинов

Плагины находятся в папке `plugins/`. Основные:

- **plugin_timer.py** - таймер и будильник
- **plugin_weather_wttr.py** - погода (требует интернет)
- **plugin_spotify.py** - управление Spotify
- **plugin_homeassistant.py** - интеграция с Home Assistant

## 🌐 Веб-интерфейс

### Запуск веб-клиента

```bash
python runva_webapi.py
```

Откройте в браузере: `http://your_server_ip:8080`

### Управление через веб

- Голосовые команды через браузер
- Текстовый ввод команд
- Управление настройками
- Просмотр логов

## 📱 Мобильные клиенты

### Telegram бот
Настройте в `options/core.json`:
```json
{
    "telegram_token": "your_bot_token",
    "telegram_enabled": true
}
```

### Веб-клиент для мобильных
Откройте `http://your_server_ip:8080` в мобильном браузере

## 🔌 Плагины и расширения

### Установка плагинов

```bash
# Запуск менеджера плагинов
python runva_plugin_installer.py
```

### Популярные плагины

- **AI-плагины** - интеграция с ChatGPT, Claude
- **IoT плагины** - управление умным домом
- **Медиа плагины** - управление музыкой и видео
- **Утилиты** - калькулятор, переводчик, заметки

## 🐳 Docker установка

### Быстрый запуск

```bash
# Запуск через Docker Compose
docker-compose up -d
```

### Собственный образ

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements-docker.txt

EXPOSE 8080
CMD ["python", "runva_webapi.py"]
```

## 🔍 Отладка и логи

### Просмотр логов

```bash
# Логи systemd
sudo journalctl -u irene-va -f

# Логи приложения
tail -f options/irene.log
```

### Тестовый режим

```bash
# Запуск без голосового ввода
python runva_cmdline.py
```

## 📊 Мониторинг

### Проверка статуса

```bash
# Статус сервиса
sudo systemctl status irene-va

# Проверка портов
netstat -tlnp | grep :8080

# Использование ресурсов
htop
```

### Автоматические проверки

Создайте скрипт мониторинга `/usr/local/bin/check-irene.sh`:

```bash
#!/bin/bash
if ! systemctl is-active --quiet irene-va; then
    echo "Irene VA is down, restarting..."
    systemctl restart irene-va
    echo "Restart completed at $(date)" >> /var/log/irene-monitor.log
fi
```

Добавьте в crontab:
```bash
*/5 * * * * /usr/local/bin/check-irene.sh
```

## 🔒 Безопасность

### Firewall настройки

```bash
# Ubuntu/Debian
sudo ufw allow 8080/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

### SSL сертификат

```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d your-domain.com
```

## 📚 Дополнительная документация

- [Установка на Linux](docs/INSTALL_LINUX.md)
- [Установка через Docker](docs/INSTALL_DOCKER.md)
- [Настройка плагинов](docs/PLUGINS.md)
- [Разработка плагинов](docs/DEV_PLUGINS.md)
- [Web API интеграция](docs/DEV_WEBAPI_INTEGRATION.md)

## 🆘 Поддержка

- **Issues**: [GitHub Issues](https://github.com/janvarev/Irene-Voice-Assistant/issues)
- **Telegram**: [Группа поддержки](https://t.me/irene_va)
- **Документация**: [docs/](docs/)

## 🤝 Вклад в проект

Если вы хотите помочь проекту:

1. **Создайте плагин** - добавьте новую функциональность
2. **Исправьте баги** - улучшите стабильность
3. **Улучшите документацию** - помогите другим пользователям
4. **Поддержите финансово** - [Boosty](https://boosty.to/irene-voice)

## 📄 Лицензия

Проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE).

---

**Ирина** - ваш персональный голосовой ассистент для домашнего сервера! 🎤✨
