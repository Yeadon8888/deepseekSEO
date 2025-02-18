import argparse
import logging
import os
from article_generator import ArticleGenerator
from image_generator import ImageGenerator
from document_writer import DocumentWriter
from utils.config import Config

def setup_logging():
    """设置日志配置"""
    config = Config()
    log_dir = config.get('log_dir', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'app.log'), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def display_article(content):
    """
    在控制台显示文章内容
    """
    print("\n" + "="*50)
    print("生成的文章内容：")
    print("="*50)
    
    paragraphs = content.split('\n\n')
    for para in paragraphs:
        if para.strip():
            # 处理标题
            if para.strip().startswith('#'):
                level = len(para.split()[0])  # 计算#的数量
                text = ' '.join(para.split()[1:])
                print("\n" + "  " * (level-1) + text)
            else:
                print("\n" + para.strip())
    
    print("\n" + "="*50 + "\n")

def main():
    """统一的程序入口"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui', action='store_true', help='启动GUI界面')
    args = parser.parse_args()
    
    if args.gui:
        from gui import start_gui
        start_gui()
    else:
        start_cli()

def start_cli():
    parser = argparse.ArgumentParser(description='SEO文章智能生成系统')
    parser.add_argument('--requirements', '-r', type=str, help='文章要求，例如："写一篇关于人工智能的文章"')
    parser.add_argument('--word_count', '-w', type=int, help='文章字数，例如：1000')
    parser.add_argument('--watermark', '-m', type=str, help='水印文字，例如："版权所有"')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 如果没有通过命令行参数指定，使用默认值
        requirements = args.requirements or "写一篇关于人工智能在日常生活中的应用的文章"
        word_count = args.word_count or 1000
        watermark = args.watermark or "版权所有"
        
        print(f"\n开始生成文章...")
        print(f"要求：{requirements}")
        print(f"字数：{word_count}")
        print(f"水印：{watermark}")
        
        # 1. 生成文章内容
        article_gen = ArticleGenerator()
        article_content = article_gen.generate(requirements, word_count)
        logger.info("文章内容生成完成")
        
        # 显示文章内容
        display_article(article_content)
        
        print("正在生成配图...")
        # 2. 生成配图
        image_gen = ImageGenerator()
        image_paths = image_gen.generate(article_content, watermark_text=watermark)
        logger.info(f"生成了 {len(image_paths)} 张配图")
        
        print("正在生成文档...")
        # 3. 生成文档
        doc_writer = DocumentWriter()
        doc_path = doc_writer.create_document(article_content, image_paths)
        logger.info(f"文档已生成: {doc_path}")
        
        print(f"\n文章生成成功！")
        print(f"文档保存路径：{doc_path}")
        print(f"配图保存路径：{os.path.dirname(image_paths[0]) if image_paths else '无'}")
        
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        print(f"\n错误：{str(e)}")
        print("请检查配置文件和日志文件以获取详细信息。")

if __name__ == '__main__':
    main()