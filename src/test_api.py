import os
import time
import requests
import json
from datetime import datetime
from pathlib import Path
import yaml

class APITester:
    def __init__(self):
        # 加载配置文件
        self.load_config()
        # 创建输出目录
        self.create_output_dirs()
        
    def load_config(self):
        """加载配置文件"""
        config_path = Path('config/config.yaml')
        if not config_path.exists():
            raise FileNotFoundError("配置文件不存在！")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        self.silicon_flow_api_key = config.get('flux_api_key')
        self.deepseek_api_key = config.get('deepseek_api_key')
        
    def create_output_dirs(self):
        """创建必要的输出目录"""
        self.output_dir = Path('output/test_results')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def test_silicon_flow_api(self, prompt=None, model=None, seed=None):
        """
        测试 SiliconFlow API 的图像生成功能
        
        Args:
            prompt (str): 图片生成提示词
            model (str): 使用的模型名称
            seed (int): 随机种子
        """
        print('\n测试 SiliconFlow API 图片生成...')
        
        # API配置
        api_url = 'https://api.siliconflow.com/v1/images/generations'
        headers = {
            'Authorization': f'Bearer {self.silicon_flow_api_key}',
            'Content-Type': 'application/json'
        }
        
        # 准备请求数据
        data = {
            'model': model or 'deepseek-ai/Janus-Pro-7B',
            'prompt': prompt or 'an island near sea, with seagulls, moon shining over the sea, light house, boats in the background',
        }
        
        if seed:
            data['seed'] = seed
            
        try:
            # 发送请求
            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 保存测试结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_file = self.output_dir / f'silicon_flow_test_{timestamp}.json'
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'request': data,
                    'response': result,
                    'timestamp': timestamp
                }, f, ensure_ascii=False, indent=2)
            
            print('SiliconFlow API 测试成功!')
            print(f'测试结果已保存至: {result_file}')
            
            if 'images' in result and len(result['images']) > 0:
                print('生成的图片URL:', result['images'][0]['url'])
                print('注意：图片URL有效期为1小时，请及时保存')
            
            if 'timings' in result:
                print('推理时间:', result['timings']['inference'], '秒')
                
        except requests.exceptions.Timeout:
            print('错误：SiliconFlow API 请求超时!')
        except requests.exceptions.RequestException as e:
            print('错误：SiliconFlow API 请求失败:', str(e))
        except Exception as e:
            print('错误：未预期的异常:', str(e))

def main():
    """主测试函数"""
    print('开始API测试...')
    print('='*50)
    
    try:
        tester = APITester()
        
        # 测试图片生成API
        test_cases = [
            {
                'prompt': '一只可爱的熊猫正在吃竹子，背景是青山绿水',
                'model': 'deepseek-ai/Janus-Pro-7B',
                'seed': 123456
            },
            {
                'prompt': 'A futuristic city with flying cars and neon lights',
                'model': 'deepseek-ai/Janus-Pro-7B',
                'seed': 789012
            }
        ]
        
        for case in test_cases:
            tester.test_silicon_flow_api(**case)
            time.sleep(2)  # 添加间隔，避免请求过于频繁
        
    except Exception as e:
        print(f'测试过程中发生错误: {str(e)}')
    
    print('\n' + '='*50)
    print('API测试完成!')

if __name__ == '__main__':
    main()