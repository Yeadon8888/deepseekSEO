# SEO文章智能生成系统

## 项目简介
基于Python的SEO文章智能生成系统，采用Qt6构建现代化界面，通过deepseek-R1和FLUX.1-dev API实现文章内容生成、AI配图及水印处理的自动化，提供一站式内容生产解决方案。

## 功能特性
### 1. 现代化Qt6界面
- 参数配置区
- 实时预览区
- 任务进度展示
- 文章列表管理
- 明暗主题切换
- 自适应布局
- 高DPI支持

### 2. 内容生成引擎
- 基于deepseek-R1的文章生成
- 多轮优化机制
- 结构化输出
- 基于FLUX.1-dev的智能配图
- 多种图片风格预设
- 图文智能匹配

### 3. 水印处理系统
- 文字水印生成
- 位置精确控制
- 透明度调节
- 批量处理能力

## 系统参数配置
### 1. 文章基础参数
- 目标关键词
- 文章数量设置
- 字数范围（1000-2000字）
- 地域信息（可选）

### 2. 图片生成参数
- 是否启用配图
- 图片风格选择：
  - 写实风格
  - 水彩画风
  - 油画风格
  - 插画风格
  - 素描风格

### 3. 水印设置
- 水印文字内容
- 水印位置选择：
  - 左上角
  - 右上角
  - 左下角
  - 右下角
  - 居中
- 水印透明度（30%-70%）

## 环境要求
- Windows 10/11
- Python 3.8+
- 内存：8GB以上
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
1. 启动程序：
```bash
python src/main.py
```
2. 在GUI界面配置参数
3. 点击生成按钮开始任务

## 性能指标
- 单篇文章生成：≤3分钟
- 图片生成：≤1分钟/张
- 界面响应：≤5秒

## 目录结构
```
├── src/                  # 源代码目录
│   ├── main.py          # 主程序入口
│   ├── gui.py           # GUI界面模块
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
1. API使用
   - 文章生成API费用需自行承担
   - 图片生成API费用需自行承担
   - 建议提前准备API账号
   - 注意遵守API使用规范

2. 系统使用
   - 定期备份生成内容
   - 合理控制生成频率
   - 保持网络环境稳定

3. SEO优化
   - 关键词密度保持在2%-3%
   - 确保文章结构符合搜索引擎友好原则

## 技术支持
- 服务期限：2周免费技术支持
- 响应时间：2小时内
- 支持方式：远程协助