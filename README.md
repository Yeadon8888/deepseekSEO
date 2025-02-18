# SEO文章智能生成系统

## 项目简介
基于Python的SEO文章智能生成系统，通过AI接口实现文章内容生成、图片生成及排版的自动化，输出符合SEO标准的图文并茂的Word文档。

## 功能特性
- 文章内容智能生成
- AI图片生成与处理
- 水印添加
- Word文档排版与输出
- SEO优化

## 环境要求
- Python 3.8+
- 内存：至少4GB
- 磁盘空间：至少1GB
- 网络：稳定的互联网连接

## 安装步骤
1. 克隆项目到本地
2. 安装依赖包：
```bash
pip install -r requirements.txt
```
3. 配置API密钥：
   - 在config目录下创建config.yaml文件
   - 配置以下内容：
     ```yaml
     deepseek_api_key: 'your_deepseek_api_key'
     flux_api_key: 'your_flux_api_key'
     output_dir: 'output'
     log_dir: 'logs'
     ```

## 使用方法
```bash
python src/main.py --requirements "写一篇关于人工智能的科技文章" --word_count 2000 --image_style "科技风" --watermark_position "bottom-right" --watermark_text "AI科技"
```

### 参数说明
- `--requirements`: 文章要求
- `--word_count`: 文章字数
- `--image_style`: 图片风格
- `--watermark_position`: 水印位置（可选：top-left, top-right, bottom-left, bottom-right）
- `--watermark_text`: 水印内容

## 目录结构
```
├── src/                  # 源代码目录
│   ├── main.py          # 主程序入口
│   ├── article_generator.py  # 文章生成模块
│   ├── image_generator.py    # 图片生成模块
│   ├── seo_optimizer.py      # SEO优化模块
│   ├── document_writer.py    # 文档处理模块
│   └── utils/           # 工具模块
│       ├── config.py    # 配置文件
│       └── logger.py    # 日志模块
├── config/              # 配置文件目录
├── output/             # 输出目录
├── logs/               # 日志目录
└── requirements.txt    # 依赖包列表
```

## 注意事项
1. API调用限制
   - 注意各API的调用频率限制
   - 建议实现请求队列和错误重试机制
2. 图片处理
   - 注意图片分辨率和大小的控制
   - 水印要求清晰但不影响主图观感
3. SEO优化
   - 关键词密度保持在2%-3%
   - 确保文章结构符合搜索引擎友好原则