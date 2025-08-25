# Улучшенный TTS plugin для pyttsx3 engine
# author: Anton (улучшенная версия)

import os

from vacore import VACore
import pyttsx3

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "TTS pyttsx улучшенный",
        "version": "2.0",
        "require_online": False,

        "description": """
Улучшенный TTS через pyttsx с автоматическим выбором лучшего русского женского голоса.
""",

        "default_options": {
            "sysId": 0, # id голоса в системе (резервный)
            "rate": 150, # скорость речи
            "volume": 0.9, # громкость
            "prefer_russian": True, # предпочитать русские голоса
            "prefer_female": True, # предпочитать женские голоса
        },

        "tts": {
            "pyttsx_improved": (init,say,towavfile) # первая функция инициализации, вторая - говорить, третья - в wav file
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def init(core:VACore):
    options = core.plugin_options(modname)

    core.ttsEngine = pyttsx3.init()

    # Получаем список доступных голосов
    voices = core.ttsEngine.getProperty("voices")
    
    print(f"PyTTSx улучшенный: Найдено голосов: {len(voices)}")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.id} - {voice.name} ({voice.languages})")
    
    # Ищем лучший голос согласно предпочтениям
    best_voice_index = options["sysId"]
    
    if options.get("prefer_russian", True):
        # Сначала ищем русские голоса
        for i, voice in enumerate(voices):
            voice_info = str(voice.languages).lower() + " " + str(voice.name).lower()
            if any(lang in voice_info for lang in ["russian", "ru", "русский", "рус"]):
                if options.get("prefer_female", True):
                    # Предпочитаем женские голоса
                    if any(gender in voice_info for gender in ["female", "женский", "жен"]):
                        best_voice_index = i
                        print(f"PyTTSx улучшенный: Найден русский женский голос: {voice.name}")
                        break
                else:
                    best_voice_index = i
                    print(f"PyTTSx улучшенный: Найден русский голос: {voice.name}")
                    break
    
    # Если русский голос не найден, используем первый доступный
    if best_voice_index == options["sysId"]:
        print(f"PyTTSx улучшенный: Русский голос не найден, использую голос по умолчанию")
    
    # Устанавливаем голос и параметры
    core.ttsEngine.setProperty("voice", voices[best_voice_index].id)
    core.ttsEngine.setProperty("rate", options.get("rate", 150))
    core.ttsEngine.setProperty("volume", options.get("volume", 0.9))
    
    print(f"PyTTSx улучшенный: Использую голос: {voices[best_voice_index].name}")
    print(f"PyTTSx улучшенный: Скорость: {options.get('rate', 150)}, Громкость: {options.get('volume', 0.9)}")

def say(core:VACore, text_to_speech:str):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    core.ttsEngine.say(str(text_to_speech))
    core.ttsEngine.runAndWait()

def towavfile(core:VACore, text_to_speech:str,wavfile:str):
    """
    Сохранение речи в WAV файл
    :param text_to_speech: текст, который нужно преобразовать в речь
    :param wavfile: путь к WAV файлу
    """
    core.ttsEngine.save_to_file(str(text_to_speech),wavfile)
    core.ttsEngine.runAndWait()
