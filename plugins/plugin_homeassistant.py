# Плагин для интеграции с Home Assistant
# author: Anton Aliabev

import os
import requests
import json
from datetime import datetime
from vacore import VACore

# Получаем имя модуля
modname = os.path.basename(__file__)[:-3]

class HomeAssistantAPI:
    """Класс для работы с Home Assistant API"""
    
    def __init__(self, base_url, access_token):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_states(self):
        """Получить все состояния устройств"""
        try:
            response = requests.get(f'{self.base_url}/api/states', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Ошибка получения состояний: {e}")
            return None
    
    def get_state(self, entity_id):
        """Получить состояние конкретного устройства"""
        try:
            response = requests.get(f'{self.base_url}/api/states/{entity_id}', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Ошибка получения состояния {entity_id}: {e}")
            return None
    
    def call_service(self, domain, service, data=None):
        """Вызвать сервис Home Assistant"""
        if data is None:
            data = {}
            
        try:
            response = requests.post(
                f'{self.base_url}/api/services/{domain}/{service}',
                headers=self.headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Ошибка вызова сервиса {domain}.{service}: {e}")
            return False
    
    def turn_on_light(self, entity_id):
        """Включить свет"""
        return self.call_service('light', 'turn_on', {'entity_id': entity_id})
    
    def turn_off_light(self, entity_id):
        """Выключить свет"""
        return self.call_service('light', 'turn_off', {'entity_id': entity_id})
    
    def toggle_light(self, entity_id):
        """Переключить свет"""
        return self.call_service('light', 'toggle', {'entity_id': entity_id})
    
    def set_light_brightness(self, entity_id, brightness):
        """Установить яркость света (0-255)"""
        return self.call_service('light', 'turn_on', {
            'entity_id': entity_id,
            'brightness': brightness
        })
    
    def get_temperature(self, entity_id):
        """Получить температуру"""
        state = self.get_state(entity_id)
        if state and 'state' in state:
            try:
                return float(state['state'])
            except ValueError:
                return None
        return None
    
    def get_humidity(self, entity_id):
        """Получить влажность"""
        state = self.get_state(entity_id)
        if state and 'state' in state:
            try:
                return float(state['state'])
            except ValueError:
                return None
        return None
    
    def get_light_status(self, entity_id):
        """Получить статус света"""
        state = self.get_state(entity_id)
        if state:
            return state['state'] == 'on'
        return None
    
    def get_all_lights(self):
        """Получить все устройства освещения"""
        states = self.get_states()
        if states:
            lights = []
            for state in states:
                if state['entity_id'].startswith('light.'):
                    lights.append({
                        'entity_id': state['entity_id'],
                        'name': state['attributes'].get('friendly_name', state['entity_id']),
                        'state': state['state']
                    })
            return lights
        return []
    
    def get_all_sensors(self):
        """Получить все датчики"""
        states = self.get_states()
        if states:
            sensors = []
            for state in states:
                if state['entity_id'].startswith('sensor.'):
                    sensors.append({
                        'entity_id': state['entity_id'],
                        'name': state['attributes'].get('friendly_name', state['entity_id']),
                        'state': state['state'],
                        'unit': state['attributes'].get('unit_of_measurement', '')
                    })
            return sensors
        return []

# Глобальная переменная для API
ha_api = None

def start(core: VACore):
    """Инициализация плагина при запуске"""
    manifest = {
        'name': 'Home Assistant интеграция',
        'version': '1.0',
        'require_online': True,
        'description': 'Интеграция с Home Assistant для управления умным домом',
        'default_options': {
            'is_active': False,
            'base_url': 'http://localhost:8123',
            'access_token': '',
            'default_room': 'гостиная'
        },
        'commands': {
            'включи свет|включи освещение': turn_on_lights,
            'выключи свет|выключи освещение': turn_off_lights,
            'переключи свет|переключи освещение': toggle_lights,
            'включи свет в|освещение в': turn_on_lights_in_room,
            'выключи свет в|освещение в': turn_off_lights_in_room,
            'температура дома|температура в доме': get_home_temperature,
            'влажность дома|влажность в доме': get_home_humidity,
            'статус устройств|статус света': get_devices_status,
            'готовлюсь ко сну|иду спать': bedtime_scenario,
            'ухожу из дома|уезжаю': leaving_home_scenario,
        }
    }
    return manifest

def start_with_options(core: VACore, manifest: dict):
    """Инициализация плагина с опциями"""
    global ha_api
    
    options = manifest["options"]
    
    if not options["is_active"]:
        manifest["commands"] = {}
        return manifest
    
    # Инициализация Home Assistant API
    if options["base_url"] and options["access_token"]:
        ha_api = HomeAssistantAPI(options["base_url"], options["access_token"])
        core.play_voice_assistant_speech("Home Assistant успешно подключен!")
    else:
        core.play_voice_assistant_speech("Home Assistant не настроен. Проверьте настройки плагина.")
    
    return manifest

def turn_on_lights(core: VACore, phrase: str):
    """Включить все основные источники света"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    # Получаем все устройства освещения
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Включаем основные источники света
    main_lights = [light for light in lights if 'main' in light['name'].lower() or 'основной' in light['name'].lower()]
    
    if main_lights:
        for light in main_lights:
            ha_api.turn_on_light(light['entity_id'])
        core.play_voice_assistant_speech("Основное освещение включено")
    else:
        # Если нет основных источников, включаем первые несколько
        for light in lights[:3]:
            ha_api.turn_on_light(light['entity_id'])
        core.play_voice_assistant_speech("Освещение включено")

def turn_off_lights(core: VACore, phrase: str):
    """Выключить все источники света"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Выключаем все источники света
    for light in lights:
        ha_api.turn_off_light(light['entity_id'])
    
    core.play_voice_assistant_speech("Все источники света выключены")

def toggle_lights(core: VACore, phrase: str):
    """Переключить состояние основного освещения"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Переключаем основные источники света
    main_lights = [light for light in lights if 'main' in light['name'].lower() or 'основной' in light['name'].lower()]
    
    if main_lights:
        for light in main_lights:
            ha_api.toggle_light(light['entity_id'])
        core.play_voice_assistant_speech("Состояние освещения переключено")
    else:
        core.play_voice_assistant_speech("Основные источники света не найдены")

def turn_on_lights_in_room(core: VACore, phrase: str):
    """Включить свет в конкретной комнате"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    # Извлекаем название комнаты из фразы
    room_name = phrase.replace("включи свет в", "").replace("освещение в", "").strip()
    
    if not room_name:
        options = core.plugin_options(modname)
        room_name = options.get("default_room", "гостиная")
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Ищем светильники в указанной комнате
    room_lights = [light for light in lights if room_name.lower() in light['name'].lower()]
    
    if room_lights:
        for light in room_lights:
            ha_api.turn_on_light(light['entity_id'])
        core.play_voice_assistant_speech(f"Свет в {room_name} включен")
    else:
        core.play_voice_assistant_speech(f"Светильники в {room_name} не найдены")

def turn_off_lights_in_room(core: VACore, phrase: str):
    """Выключить свет в конкретной комнате"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    # Извлекаем название комнаты из фразы
    room_name = phrase.replace("выключи свет в", "").replace("освещение в", "").strip()
    
    if not room_name:
        options = core.plugin_options(modname)
        room_name = options.get("default_room", "гостиная")
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Ищем светильники в указанной комнате
    room_lights = [light for light in lights if room_name.lower() in light['name'].lower()]
    
    if room_lights:
        for light in room_lights:
            ha_api.turn_off_light(light['entity_id'])
        core.play_voice_assistant_speech(f"Свет в {room_name} выключен")
    else:
        core.play_voice_assistant_speech(f"Светильники в {room_name} не найдены")

def get_home_temperature(core: VACore, phrase: str):
    """Получить температуру в доме"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    sensors = ha_api.get_all_sensors()
    if not sensors:
        core.play_voice_assistant_speech("Датчики температуры не найдены")
        return
    
    # Ищем датчики температуры
    temp_sensors = [sensor for sensor in sensors if 'temperature' in sensor['entity_id'].lower() or 'temp' in sensor['entity_id'].lower()]
    
    if temp_sensors:
        # Берем первый найденный датчик температуры
        temp = ha_api.get_temperature(temp_sensors[0]['entity_id'])
        if temp is not None:
            core.play_voice_assistant_speech(f"Температура в доме {temp} градусов")
        else:
            core.play_voice_assistant_speech("Не удалось получить показания температуры")
    else:
        core.play_voice_assistant_speech("Датчики температуры не найдены")

def get_home_humidity(core: VACore, phrase: str):
    """Получить влажность в доме"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    sensors = ha_api.get_all_sensors()
    if not sensors:
        core.play_voice_assistant_speech("Датчики влажности не найдены")
        return
    
    # Ищем датчики влажности
    humidity_sensors = [sensor for sensor in sensors if 'humidity' in sensor['entity_id'].lower() or 'влажность' in sensor['name'].lower()]
    
    if humidity_sensors:
        # Берем первый найденный датчик влажности
        humidity = ha_api.get_humidity(humidity_sensors[0]['entity_id'])
        if humidity is not None:
            core.play_voice_assistant_speech(f"Влажность в доме {humidity} процентов")
        else:
            core.play_voice_assistant_speech("Не удалось получить показания влажности")
    else:
        core.play_voice_assistant_speech("Датчики влажности не найдены")

def get_devices_status(core: VACore, phrase: str):
    """Получить статус основных устройств"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства не найдены")
        return
    
    # Подсчитываем включенные и выключенные устройства
    on_count = sum(1 for light in lights if light['state'] == 'on')
    total_count = len(lights)
    
    if on_count == 0:
        core.play_voice_assistant_speech("Все источники света выключены")
    elif on_count == total_count:
        core.play_voice_assistant_speech("Все источники света включены")
    else:
        core.play_voice_assistant_speech(f"Включено {on_count} из {total_count} источников света")

def bedtime_scenario(core: VACore, phrase: str):
    """Сценарий подготовки ко сну"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Выключаем основное освещение
    main_lights = [light for light in lights if 'main' in light['name'].lower() or 'основной' in light['name'].lower()]
    for light in main_lights:
        ha_api.turn_off_light(light['entity_id'])
    
    # Включаем ночник (если есть)
    night_lights = [light for light in lights if 'ночник' in light['name'].lower() or 'night' in light['name'].lower()]
    for light in night_lights:
        ha_api.turn_on_light(light['entity_id'])
        ha_api.set_light_brightness(light['entity_id'], 50)  # Уменьшаем яркость
    
    core.play_voice_assistant_speech("Сценарий подготовки ко сну активирован. Основное освещение выключено, ночник включен.")

def leaving_home_scenario(core: VACore, phrase: str):
    """Сценарий ухода из дома"""
    global ha_api
    
    if not ha_api:
        core.play_voice_assistant_speech("Home Assistant не настроен")
        return
    
    lights = ha_api.get_all_lights()
    if not lights:
        core.play_voice_assistant_speech("Устройства освещения не найдены")
        return
    
    # Выключаем все источники света
    for light in lights:
        ha_api.turn_off_light(light['entity_id'])
    
    core.play_voice_assistant_speech("Сценарий ухода из дома активирован. Все источники света выключены.")
