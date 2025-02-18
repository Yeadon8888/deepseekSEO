from openai import OpenAI
from utils.config import Config
import time
from requests.exceptions import RequestException, Timeout, ConnectionError
import logging

class ArticleGenerator:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        try:
            api_key = self.config.get('deepseek_api_key')
            if not api_key:
                raise ValueError("API密钥未配置")
                
            self.client = OpenAI(
                base_url="https://api.ppinfra.com/v3/openai",
                api_key=api_key
            )
            self.logger.info("API客户端初始化成功")
            
        except Exception as e:
            error_msg = f"API客户端初始化失败：{str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
    def generate(self, requirements, word_count, max_retries=5, retry_delay=3):
        """
        生成文章内容，包含重试机制
        :param requirements: 文章要求
        :param word_count: 字数要求
        :param max_retries: 最大重试次数
        :param retry_delay: 重试间隔（秒）
        :return: 生成的文章内容
        """
        prompt = self._create_prompt(requirements, word_count)
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"尝试生成文章，第{attempt + 1}次尝试")
                response = self.client.chat.completions.create(
                    model="deepseek/deepseek-r1/community",
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一个专业的SEO文章写手，擅长创作优质的SEO文章。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    stream=False,
                    max_tokens=10240,
                    temperature=1,
                    top_p=1,
                    presence_penalty=0,
                    frequency_penalty=0,
                    response_format={"type": "text"},
                    extra_body={
                        "top_k": 50,
                        "repetition_penalty": 1,
                        "min_p": 0
                    }
                )
                self.logger.info("文章生成成功")
                return response.choices[0].message.content
                
            except Timeout:
                error_msg = f"API请求超时（第{attempt + 1}次尝试）"
                self.logger.warning(error_msg)
                if attempt == max_retries - 1:
                    raise Exception(f"{error_msg}，请稍后重试")
                time.sleep(retry_delay * (attempt + 1))
                
            except (ConnectionError, RequestException) as e:
                error_msg = f"API请求错误（第{attempt + 1}次尝试）：{str(e)}"
                self.logger.error(error_msg)
                if attempt == max_retries - 1:
                    raise Exception(f"{error_msg}\n请检查网络连接并重试")
                time.sleep(retry_delay * (attempt + 1))
                
            except Exception as e:
                error_msg = f"未知错误：{str(e)}"
                self.logger.error(error_msg)
                raise Exception(f"{error_msg}\n请联系技术支持")
                
        raise Exception('达到最大重试次数，请稍后重试')
    
    def _create_prompt(self, requirements, word_count):
        return f"""请生成一篇符合以下要求的SEO文章：
        要求：{requirements}
        字数：{word_count}
        要求：
        1. 符合SEO优化标准
        2. 段落结构清晰
        3. 适合配图的内容布局
        4. 关键词密度保持在2%-3%
        5. 标题和段落层次分明
        """