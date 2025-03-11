import json
import requests


group_id = "1895527701121340150"
api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJuYW4iLCJVc2VyTmFtZSI6Im5hbiIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODk1NTI3NzAxMTI5NzI4NzU4IiwiUGhvbmUiOiIxMzExMTYyMjY3NSIsIkdyb3VwSUQiOiIxODk1NTI3NzAxMTIxMzQwMTUwIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDMtMDMgMTc6MDQ6MjIiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.hI0wKswiOVK-iAKXdjjf1uKd8LRrKqcx4JX_X972F40PVlQpt4hkd6P5Thc515F3WT6YBToStqzPwrMjXzMVgyPNVh62zs4-PdlokkE3KSughCrimizyfmwXhnGtnXL_7G6vf4YHgvP9ROt9NfpVkJwH9HLo4mFNpNdG7yrmG9RB9luDiqP1EsiE50Kl-3S24mGQhwUWnVEA2UPSQVHzufc9J85zwMb1xppV6OfmQ4Pyk4RdEX34tVDFW-aDEPLCOh2RVrpeIk_-KI52i5T1dkqqmqgdlgxQNOx8hrHl6O1r-_vnb_JT1uehfBbBdFk9HNZiou4wP33e2z9FNKYWlQ"


url = 'https://api.minimax.chat/v1/files/upload?GroupId={}'.format(group_id)
headers1 = {
    'Authorization': 'Bearer {}'.format(api_key)
}

data = {
    'purpose': 'voice_clone'  
}

# 替换为音频文件路径
files = {
    'file': open('D:\桌面\TTS\哄睡004.mp3', 'rb')  
}

# 上传文件并获取file_id
response = requests.post(url, headers=headers1, data=data, files=files)
file_id = response.json().get("file").get("file_id")
print("File ID:", file_id)


url = 'https://api.minimax.chat/v1/files/upload?GroupId={}'.format(group_id)
data = {
    'purpose': 'prompt_audio'  
}

 # 替换为示例音频文件路径
files = {
    'file': open('D:\桌面\TTS\prompt.mp3', 'rb') 
}

# 上传示例音频并获取file_id
response = requests.post(url, headers=headers1, data=data, files=files)
prompt_file_id = response.json().get("file").get("file_id")
print("Prompt File ID:", prompt_file_id)

# 音频复刻请求
url = "https://api.minimax.chat/v1/voice_clone?GroupId={}".format(group_id)
payload2 = json.dumps({
  "file_id": file_id,  
  "voice_id": "hongshui004",  # 替换为自定义的voice_id
  "text_validation": "开始了。刘十三出生在云边镇，是王莺莺的外孙，属于小卖部继承人。班上女同学流行写日记，王莺莺专门批发两箱花花绿绿的日记本，刚开学就卖光了。那些女同学把日记本贴身带着，好像里面真的充满了秘密似的。刘十三对此不屑，谁有他的本子秘密的！具体来说不能算是个本子，他用东信电子厂的内部稿纸拼起来的。打开第一页，是妈妈曾经留给他的话，他一笔一划抄的仔细。", # 音频与文本对比的验证
  "accuracy": 0.8, 
  "clone_prompt": {
        "prompt_audio": prompt_file_id,  
        "prompt_text": "如果能在一分钟内赶到法国，那就能看见日落，可惜法国太远了。"  # 提供prompt voice对应的文本
    }
})

headers2 = {
  'Authorization': 'Bearer {}'.format(api_key),
  'Content-Type': 'application/json'
}

# 发起音频复刻请求
response = requests.post(url, headers=headers2, data=payload2)
print("Response:", response.text)