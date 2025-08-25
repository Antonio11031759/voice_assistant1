# Плагин для интеграции с Spotify
# author: Anton Aliabev

import os
import requests
import json
from datetime import datetime, timedelta
from vacore import VACore

# Получаем имя модуля
modname = os.path.basename(__file__)[:-3]

class SpotifyAPI:
    """Класс для работы с Spotify API"""
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        
    def get_auth_url(self):
        """Получить URL для авторизации"""
        scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-read-private,user-library-read"
        auth_url = f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={scope}"
        return auth_url
    
    def exchange_code_for_token(self, auth_code):
        """Обмен кода авторизации на токен"""
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.refresh_token = token_data['refresh_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
            return True
        return False
    
    def refresh_access_token(self):
        """Обновление access token"""
        if not self.refresh_token:
            return False
            
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            if 'refresh_token' in token_data:
                self.refresh_token = token_data['refresh_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
            return True
        return False
    
    def get_current_playback(self):
        """Получить текущее состояние воспроизведения"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return None
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def play_pause(self):
        """Воспроизвести/поставить на паузу"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return False
        
        current = self.get_current_playback()
        if not current:
            return False
            
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if current['is_playing']:
            # Поставить на паузу
            response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)
        else:
            # Воспроизвести
            response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers)
            
        return response.status_code == 204
    
    def next_track(self):
        """Следующий трек"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.post('https://api.spotify.com/v1/me/player/next', headers=headers)
        return response.status_code == 204
    
    def previous_track(self):
        """Предыдущий трек"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.post('https://api.spotify.com/v1/me/player/previous', headers=headers)
        return response.status_code == 204
    
    def search_track(self, query):
        """Поиск трека"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return None
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': query, 'type': 'track', 'limit': 5}
        response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['tracks']['items']:
                return data['tracks']['items'][0]
        return None
    
    def play_track(self, track_uri):
        """Воспроизвести конкретный трек"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            if not self.refresh_access_token():
                return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        data = {'uris': [track_uri]}
        response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, json=data)
        return response.status_code == 204

# Глобальная переменная для API
spotify_api = None

def start(core: VACore):
    """Инициализация плагина при запуске"""
    manifest = {
        'name': 'Spotify интеграция',
        'version': '1.0',
        'require_online': True,
        'description': 'Интеграция с Spotify для управления музыкой',
        'default_options': {
            'is_active': False,
            'client_id': '',
            'client_secret': '',
            'redirect_uri': 'http://localhost:5003/spotify_callback',
            'auth_code': ''
        },
        'commands': {
            'включи музыку|поставь музыку': play_music,
            'пауза|поставь на паузу': pause_music,
            'следующий трек|следующий': next_track,
            'предыдущий трек|предыдущий': previous_track,
            'поставь трек|найди трек': search_and_play_track,
            'статус музыки|что играет': get_music_status,
        }
    }
    return manifest

def start_with_options(core: VACore, manifest: dict):
    """Инициализация плагина с опциями"""
    global spotify_api
    
    options = manifest["options"]
    
    if not options["is_active"]:
        manifest["commands"] = {}
        return manifest
    
    # Инициализация Spotify API
    if options["client_id"] and options["client_secret"]:
        spotify_api = SpotifyAPI(
            options["client_id"],
            options["client_secret"],
            options["redirect_uri"]
        )
        
        # Если есть auth_code, обменяем на токен
        if options["auth_code"]:
            if spotify_api.exchange_code_for_token(options["auth_code"]):
                core.play_voice_assistant_speech("Spotify успешно подключен!")
            else:
                core.play_voice_assistant_speech("Ошибка подключения к Spotify")
    
    return manifest

def play_music(core: VACore, phrase: str):
    """Включить музыку"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен. Проверьте настройки плагина.")
        return
    
    if spotify_api.play_pause():
        core.play_voice_assistant_speech("Музыка включена!")
    else:
        core.play_voice_assistant_speech("Не удалось включить музыку")

def pause_music(core: VACore, phrase: str):
    """Поставить музыку на паузу"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен")
        return
    
    if spotify_api.play_pause():
        core.play_voice_assistant_speech("Музыка поставлена на паузу")
    else:
        core.play_voice_assistant_speech("Не удалось поставить на паузу")

def next_track(core: VACore, phrase: str):
    """Следующий трек"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен")
        return
    
    if spotify_api.next_track():
        core.play_voice_assistant_speech("Следующий трек")
    else:
        core.play_voice_assistant_speech("Не удалось переключить трек")

def previous_track(core: VACore, phrase: str):
    """Предыдущий трек"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен")
        return
    
    if spotify_api.previous_track():
        core.play_voice_assistant_speech("Предыдущий трек")
    else:
        core.play_voice_assistant_speech("Не удалось переключить трек")

def search_and_play_track(core: VACore, phrase: str):
    """Поиск и воспроизведение трека"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен")
        return
    
    # Извлекаем название трека из фразы
    track_name = phrase.replace("поставь трек", "").replace("найди трек", "").strip()
    
    if not track_name:
        core.play_voice_assistant_speech("Скажите название трека")
        return
    
    core.play_voice_assistant_speech(f"Ищу трек {track_name}")
    
    track = spotify_api.search_track(track_name)
    if track:
        track_name = track['name']
        artist = track['artists'][0]['name'] if track['artists'] else 'Неизвестный исполнитель'
        
        if spotify_api.play_track(track['uri']):
            core.play_voice_assistant_speech(f"Воспроизвожу {track_name} от {artist}")
        else:
            core.play_voice_assistant_speech("Не удалось воспроизвести трек")
    else:
        core.play_voice_assistant_speech(f"Трек {track_name} не найден")

def get_music_status(core: VACore, phrase: str):
    """Получить статус музыки"""
    global spotify_api
    
    if not spotify_api:
        core.play_voice_assistant_speech("Spotify не настроен")
        return
    
    current = spotify_api.get_current_playback()
    if current and current['is_playing']:
        track = current['item']
        track_name = track['name']
        artist = track['artists'][0]['name'] if track['artists'] else 'Неизвестный исполнитель'
        core.play_voice_assistant_speech(f"Сейчас играет {track_name} от {artist}")
    else:
        core.play_voice_assistant_speech("Музыка не воспроизводится")
