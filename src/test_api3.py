import requests
import yaml
import json
import os
from datetime import datetime

# 读取配置文件
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 确保输出目录存在
output_dir = "output/images"
os.makedirs(output_dir, exist_ok=True)

url = "https://api.siliconflow.cn/v1/images/generations"

payload = {
    "model": "black-forest-labs/FLUX.1-dev",
    "prompt": "一只小兔子",
    "image_size": "1024x1024",
    "num_inference_steps": 10
}
headers = {
    "Authorization": f"Bearer {config['flux_api_key']}",
    "Content-Type": "application/json"
}

try:
    # 发送生成图片请求
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # 检查响应状态
    
    # 解析响应数据
    result = response.json()
    
    if 'data' in result and len(result['data']) > 0:
        # 获取图片URL
        image_url = result['data'][0].get('url')
        
        if image_url:
            # 下载图片
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # 生成文件名（使用时间戳和提示词）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt_short = payload['prompt'][:30].replace(" ", "_")  # 使用提示词的前30个字符
            filename = f"{timestamp}_{prompt_short}.png"
            file_path = os.path.join(output_dir, filename)
            
            # 保存图片
            with open(file_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"图片已成功保存到: {file_path}")
        else:
            print("未在响应中找到图片URL")
    else:
        print("API响应格式不正确")
        print("完整响应:", json.dumps(result, ensure_ascii=False, indent=2))

except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")