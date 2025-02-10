import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

from mock_data import MOCK_PJ1_REPORT

load_dotenv()  # 加载 .env 文件中的环境变量

default_message = "推理结果:\n节点 0: 类别 2\n节点 1: 类别 0\n节点 2: 类别 0\n节点 3: 类别 0\n节点 4: 类别 0\n节点 5: 类别 2\n节点 6: 类别 2\n节点 7: 类别 2\n节点 8: 类别 2\n节点 9: 类别 0\n节点 10: 类别 0\n节点 11: 类别 0\n节点 12: 类别 0\n节点 13: 类别 0\n节点 14: 类别 0\n节点 15: 类别 0\n节点 16: 类别 0\n节点 17: 类别 0\n节点 18: 类别 0\n节点 19: 类别 0\n节点 20: 类别 0\n节点 21: 类别 0\n节点 22: 类别 0\n节点 23: 类别 0\n节点 24: 类别 0\n节点 25: 类别 0\n节点 26: 类别 0\n节点 27: 类别 0\n节点 28: 类别 0\n节点 29: 类别 0\n节点 30: 类别 0\n节点 31: 类别 0\n节点 32: 类别 0\n节点 33: 类别 0\n节点 34: 类别 0\n节点 35: 类别 0\n节点 36: 类别 0\n节点 37: 类别 0\n节点 38: 类别 0\n节点 39: 类别 0\n节点 40: 类别 0\n节点 41: 类别 0\n节点 42: 类别 0\n节点 43: 类别 0\n节点 44: 类别 0\n节点 45: 类别 0\n节点 46: 类别 0\n节点 47: 类别 0\n节点 48: 类别 0\n节点 49: 类别 0\n节点 50: 类别 0\n节点 51: 类别 0\n节点 52: 类别 0\n节点 53: 类别 0\n节点 54: 类别 0\n节点 55: 类别 0\n节点 56: 类别 0\n节点 57: 类别 0\n节点 58: 类别 0\n节点 59: 类别 0\n节点 60: 类别 0\n节点 61: 类别 0\n节点 62: 类别 0\n节点 63: 类别 0\n节点 64: 类别 2\n节点 65: 类别 0\n节点 66: 类别 0\n节点 67: 类别 0\n节点 68: 类别 0\n节点 69: 类别 0\n节点 70: 类别 0\n节点 71: 类别 0\n节点 72: 类别 0\n节点 73: 类别 0\n节点 74: 类别 0\n节点 75: 类别 0\n节点 76: 类别 0\n节点 77: 类别 0\n节点 78: 类别 0\n节点 79: 类别 0\n节点 80: 类别 0\n节点 81: 类别 0\n节点 82: 类别 0\n节点 83: 类别 0\n节点 84: 类别 0\n节点 85: 类别 0\n节点 86: 类别 0\n节点 87: 类别 0\n节点 88: 类别 0\n节点 89: 类别 0\n节点 90: 类别 0\n节点 91: 类别 0\n节点 92: 类别 0\n节点 93: 类别 0\n节点 94: 类别 0\n节点 95: 类别 0\n节点 96: 类别 0\n节点 97: 类别 2\n节点 98: 类别 2\n节点 99: 类别 2\n"

def generate_pj1_report_deepseek(message=None):
    """课题一算法的报告生成。

    参数:
        message (str): 用户输入的消息，预期为课题一算法模型在数据集上的表现。

    返回:
        str: 报告内容。
    """
    if message is None:
        # message = default_message
        return MOCK_PJ1_REPORT
        

    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 构建提示信息
    prompt = f"你是一个专业的报告生成器，下面是跨境贸易支付监测课题一算法模型（基于图神经网络）在数据集上的推理结果，请根据给定的输入生成专业的模型效果报告。你的报告应尽可能详细，不要包含任何称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互：\n{message}\n"

    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n"
            }
        ],
        "stream": False,
        "max_tokens": 6400,
        "stop": ["null"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('SILICONFLOW_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()['choices'][0]['message']['content']

def generate_pj1_report_gpt4(message=None):
    """课题一算法的报告生成。

    参数:
        message (str): 用户输入的消息，预期为课题一算法模型在数据集上的表现。

    返回:
        str: 报告内容。
    """
    if message is None:
        # message = default_message
        return MOCK_PJ1_REPORT
    
    # 调用 OpenAI 的 GPT 模型
    client = OpenAI()
    prompt = f"你是一个专业的报告生成器，下面是跨境贸易支付监测课题一算法模型（基于图神经网络）在数据集上的推理结果，请根据给定的输入生成专业的模型效果报告。你的报告应尽可能详细，不要包含任何称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互：\n{message}\n"
    response = client.chat.completions.create(
        model="gpt-4",  # 选择合适的引擎
        messages=[
            {"role": "system", "content": "你是一个专业的报告生成器。"
             "请撰写报告，总结给定模型的推理结果。你的回答应尽可能详尽，且确保专业"
             "不要包含称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5120,  # 设置生成文本的最大长度
        n=1,
        stop=None,
        temperature=0.7  # 控制生成文本的随机性
    )
    
    # 提取生成的文本
    user_profile_description = response.choices[0].message.content
    
    return user_profile_description

if __name__ == "__main__":
    report = generate_pj1_report_gpt4()
    print(report)
