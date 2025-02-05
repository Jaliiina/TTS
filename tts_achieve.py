
import torch
from transformers import AutoModel, AutoTokenizer  # 确保导入 AutoModel 和 AutoTokenizer
import librosa

# 指定本地模型路径（修改为你的实际路径）
local_model_path = "D:\\MiniCPM-o-2_6"

# 加载 MiniCPM-o-2.6 模型
model = AutoModel.from_pretrained(
    local_model_path,
    trust_remote_code=True,
    attn_implementation='sdpa',  # 可以选择 'sdpa' 或 'flash_attention_2'
    torch_dtype=torch.bfloat16,  # 模型默认使用 bfloat16
)
model = model.eval().cuda()  # 切换为评估模式，并加载到 GPU

# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_model_path, trust_remote_code=True)

# 初始化 TTS 模块
model.init_tts()

# 如果遇到 BFloat16 不支持的问题，切换 TTS 模块为 float32
model.tts.float()

# 加载参考音频（用于克隆声音）
ref_audio, _ = librosa.load('D:\\move11\\TTS\\连淮伟读书.wav', sr=16000, mono=True)

# 生成系统提示，用于指定模型以声音克隆模式工作
sys_prompt = model.get_sys_prompt(ref_audio=ref_audio, mode='voice_cloning', language='zh')

# 定义要合成的文本
text_prompt = "请阅读下列文本"
user_content = ("也许你不知道，在人群中我总会第一时间寻找你的身影。"
                "你的每一个眼神，每一句话语，都如同磁石一般吸引着我。"
                "我喜欢你，是那种藏在心底深处、小心翼翼又炽热无比的喜欢。"
                "我期待着有一天，能与你并肩同行，哪怕只是简单地走在一起，对我来说也是莫大的幸福。")

# 构建消息列表
user_question = {'role': 'user', 'content': [text_prompt, user_content]}
msgs = [sys_prompt, user_question]

# 生成语音
result = model.chat(
    msgs=msgs,
    tokenizer=tokenizer,
    sampling=True,
    max_new_tokens=128,
    use_tts_template=True,
    generate_audio=True,
    temperature=0.3,  # 控制生成的随机性
    output_audio_path='D:\\move11\\cloning.wav',  # 输出音频路径
)