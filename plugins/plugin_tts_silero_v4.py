# TTS plugin for silero engine v4
# author: Vladislav Janvarev

# require torch 2.0+

# поддерживает несколько языков
# поменяйте modelurl на нужный вам
# список здесь: https://github.com/snakers4/silero-models#text-to-speech
# или здесь: https://models.silero.ai/models/tts/

modelurl = 'https://models.silero.ai/models/tts/ru/v4_ru.pt'

import os

from vacore import VACore

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "TTS silero V4",
        "version": "2.1",
        "require_online": False,

        "default_options": {
            "speaker": "xenia",
            "threads": 4,
            "sample_rate": 48000,
            "put_accent": True,
            "put_yo": True,
            "speaker_by_assname": {
                "ирина|ирины|ирину": "xenia",
                "альбина|альбине": "baya",
                "николай|николаю": "aidar"
            }
        },

        "tts": {
            "silero_v4": (init,None,towavfile) # первая функция инициализации, вторая - говорить
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def init(core:VACore):
    options = core.plugin_options(modname)

    import os
    import torch

    print("Silero TTS v4: Инициализация...")
    
    device = torch.device('cpu')
    torch.set_num_threads(options["threads"])
    local_file = 'silero_model_v4.pt'

    if not os.path.isfile(local_file):
        print("Silero TTS v4: Скачиваю модель...")
        torch.hub.download_url_to_file(modelurl, local_file)
        print("Silero TTS v4: Модель скачана успешно!")

    print("Silero TTS v4: Загружаю модель...")
    core.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    core.model.to(device)
    
    print(f"Silero TTS v4: Модель загружена на {device}")
    print(f"Silero TTS v4: Доступные голоса: {core.model.speakers}")
    print(f"Silero TTS v4: Текущий голос: {options['speaker']}")
    print(f"Silero TTS v4: Частота дискретизации: {options['sample_rate']}Hz")
    print(f"Silero TTS v4: Количество потоков: {options['threads']}")


def towavfile(core:VACore, text_to_speech:str, wavfile:str):
    # Улучшенная обработка текста для более естественной речи
    text_to_speech = text_to_speech.replace("…","...")
    text_to_speech = text_to_speech.replace("—","-")
    text_to_speech = text_to_speech.replace("–","-")
    
    # Нормализация чисел
    text_to_speech = core.all_num_to_text(text_to_speech)
    
    # Добавляем паузы для более естественной речи
    text_to_speech = text_to_speech.replace(".", " . ")
    text_to_speech = text_to_speech.replace("!", " ! ")
    text_to_speech = text_to_speech.replace("?", " ? ")
    text_to_speech = text_to_speech.replace(",", " , ")
    
    # Убираем лишние пробелы
    text_to_speech = " ".join(text_to_speech.split())
    
    print(f"Silero TTS: Озвучиваю текст: '{text_to_speech}'")

    options = core.plugin_options(modname)
    speaker = options["speaker"]

    # Дополнительный резолвинг по имени обращения
    if core.cur_callname != "":
        for k in options["speaker_by_assname"].keys():
            ar_k = str(k).split("|")
            if core.cur_callname in ar_k:
                speaker = options["speaker_by_assname"][k]
                print(f"Silero TTS: Использую голос '{speaker}' для '{core.cur_callname}'")

    print(f"Silero TTS: Генерация аудио с голосом '{speaker}', частота {options['sample_rate']}Hz")

    # Рендерим wav с улучшенными параметрами
    path = core.model.save_wav(text=text_to_speech,
                               speaker=speaker,
                               put_accent=options["put_accent"],
                               put_yo=options["put_yo"],
                               sample_rate=options["sample_rate"])

    # Перемещаем wav на новое место
    if os.path.exists(wavfile):
        os.unlink(wavfile)
    os.rename(path,wavfile)
    
    print(f"Silero TTS: Аудио сохранено в {wavfile}")