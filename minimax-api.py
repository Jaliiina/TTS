
import json
import subprocess
import time
from typing import Iterator

import requests
# 配置 API 访问信息
group_id = ""
api_key = ""
file_format = 'mp3'  # 支持 mp3/pcm/flac

url = "https://api.minimax.chat/v1/t2a_v2?GroupId=" + group_id
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}


def build_tts_stream_headers() -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'authorization': "Bearer " + api_key,
    }
    return headers


def build_tts_stream_body(text: str) -> dict:
    body = json.dumps({
        "model": "speech-01-turbo",
        "text": "一提到雨，也就必然的要想到雪：“晚来天欲雪，能饮一杯无？”自然是江南日暮的雪景。“寒沙梅影路，微雪酒香村”，则雪月梅的冬宵三友，会合在一道，在调戏酒姑娘了。“柴门村犬吠，风雪夜归人”，是江南雪夜，更深人静后的景况。“前树深雪里，昨夜一枝开”又到了第二天的早晨，和狗一样喜欢弄雪的村童来报告村景了。诗人的诗句，也许不尽是在江南所写，而做这几句诗的诗人，也许不尽是江南人，但假了这几句诗来描写江南的雪景，岂不直截了当，比我这一枝愚劣的笔所写的散文更美丽得多？    \
            窗外的天气晴朗得像晚秋一样：晴空的高爽，日光的洋溢，引诱得使你在房间里坐不住，空言不如实践，这一种无聊的杂文，我也不再想写下去了，还是拿起手杖，搁下纸笔，上湖上散散步罢！",
        "stream": True,
        "voice_setting": {
            "voice_id": "hongshui001",
            "speed": 0.9,
            "vol": 1.0,
            "pitch": 0
        },
        "pronunciation_dict": {
            "tone": [
                "处理/(chu3)(li3)", "危险/dangerous"
            ]
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        }
    })
    return body


mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
mpv_process = subprocess.Popen(
    mpv_command,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)


def call_tts_stream(text: str) -> Iterator[bytes]:
    tts_url = url
    tts_headers = build_tts_stream_headers()
    tts_body = build_tts_stream_body(text)

    response = requests.request("POST", tts_url, stream=True, headers=tts_headers, data=tts_body)
    for chunk in (response.raw):
        if chunk:
            if chunk[:5] == b'data:':
                data = json.loads(chunk[5:])
                if "data" in data and "extra_info" not in data:
                    if "audio" in data["data"]:
                        audio = data["data"]['audio']
                        yield audio


def audio_play(audio_stream: Iterator[bytes]) -> bytes:
    audio = b""
    for chunk in audio_stream:
        if chunk is not None and chunk != '\n':
            decoded_hex = bytes.fromhex(chunk)
            mpv_process.stdin.write(decoded_hex)  # type: ignore
            mpv_process.stdin.flush()
            audio += decoded_hex

    return audio


audio_chunk_iterator = call_tts_stream('')
audio = audio_play(audio_chunk_iterator)

# 结果保存至文件
timestamp = int(time.time())
file_name = f'output_total_{timestamp}.{file_format}'
with open(file_name, 'wb') as file:
    file.write(audio)
