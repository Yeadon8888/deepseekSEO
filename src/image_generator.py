import requests
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from utils.config import Config
import logging

class ImageGenerator:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        try:
            self.api_key = self.config.get('flux_api_key')
            if not self.api_key:
                raise ValueError("FLUX API密钥未配置")
            
            self.output_dir = os.path.join('output', 'images')
            os.makedirs(self.output_dir, exist_ok=True)
            self.logger.info("图片生成器初始化成功")
            
        except Exception as e:
            error_msg = f"图片生成器初始化失败：{str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
    def generate(self, article_content, image_style="", watermark_text=""):
        """
        生成并处理图片
        :param article_content: 文章内容
        :param image_style: 图片风格
        :param watermark_text: 水印文字
        :return: 生成的图片路径列表
        """
        image_prompts = self._extract_image_prompts(article_content)
        image_paths = []
        
        for prompt in image_prompts:
            try:
                # 生成图片
                image_data = self._generate_image(prompt)
                if image_data:
                    # 添加水印（如果有）
                    if watermark_text:
                        image = Image.open(BytesIO(image_data))
                        image = self._add_watermark(image, watermark_text, 'bottom-right')
                        # 保存带水印的图片
                        image_path = self._save_image(prompt, image)
                    else:
                        # 直接保存原图
                        image_path = self._save_image(prompt, image_data)
                    
                    image_paths.append(image_path)
                    
            except Exception as e:
                print(f"生成图片时出错: {str(e)}")
                continue
                
        return image_paths
    
    def _extract_image_prompts(self, article_content):
        """
        从文章内容中提取需要生成图片的关键段落
        """
        paragraphs = article_content.split('\n\n')
        prompts = []
        for i, para in enumerate(paragraphs):
            if i % 2 == 0 and len(para.strip()) > 100:  # 每隔一个段落，且段落长度大于100
                prompts.append(para[:200])  # 取前200个字作为提示词
        return prompts[:3]  # 最多生成3张图
    
    def _generate_image(self, prompt):
        """
        调用FLUX API生成图片
        """
        url = "https://api.siliconflow.cn/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "black-forest-labs/FLUX.1-dev",
            "prompt": prompt,
            "image_size": "1024x1024",
            "num_inference_steps": 10
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url')
                if image_url:
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    return image_response.content
                    
            raise Exception("未能获取到图片URL")
            
        except Exception as e:
            raise Exception(f"生成图片失败: {str(e)}")
    
    def _save_image(self, prompt, image_data):
        """
        保存图片到本地
        :param prompt: 生成图片的提示词
        :param image_data: 图片数据（bytes或PIL Image对象）
        :return: 保存的图片路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_short = prompt[:30].replace(" ", "_")  # 使用提示词的前30个字符
        filename = f"{timestamp}_{prompt_short}.png"
        file_path = os.path.join(self.output_dir, filename)
        
        if isinstance(image_data, bytes):
            with open(file_path, 'wb') as f:
                f.write(image_data)
        else:  # PIL Image对象
            image_data.save(file_path, 'PNG')
            
        return file_path
    
    def _add_watermark(self, image, text, position='bottom-right'):
        """
        添加水印到图片
        """
        if not isinstance(image, Image.Image):
            image = Image.open(BytesIO(image))
            
        # 确保图片是RGBA模式
        image = image.convert('RGBA')
        width, height = image.size
        
        # 创建水印层
        watermark = Image.new('RGBA', image.size, (0,0,0,0))
        draw = ImageDraw.Draw(watermark)
        
        # 设置字体和大小
        font_size = int(min(width, height) * 0.05)
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        # 获取文本大小
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 计算水印位置
        padding = 20
        if position == 'bottom-right':
            x = width - text_width - padding
            y = height - text_height - padding
        elif position == 'bottom-left':
            x = padding
            y = height - text_height - padding
        elif position == 'top-right':
            x = width - text_width - padding
            y = padding
        else:  # top-left
            x = padding
            y = padding
        
        # 绘制水印文本
        draw.text((x, y), text, font=font, fill=(255,255,255,128))
        
        # 合并原图和水印
        return Image.alpha_composite(image, watermark)