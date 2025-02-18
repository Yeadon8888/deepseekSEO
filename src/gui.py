import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QSpinBox,
                             QPushButton, QComboBox, QMessageBox, QProgressBar,
                             QStatusBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from article_generator import ArticleGenerator
from image_generator import ImageGenerator
from seo_optimizer import SEOOptimizer
from document_writer import DocumentWriter
from utils.config import Config
from utils.state import TaskStatus, GenerationState
from utils.exceptions import SEOGeneratorException, APIError, ConfigError
import logging

class GenerationThread(QThread):
    """异步生成线程"""
    progress_updated = pyqtSignal(GenerationState)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        try:
            # 更新状态：开始生成文章
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.RUNNING,
                progress=0.0,
                message="正在生成文章..."
            ))
            
            # 生成文章
            article_gen = ArticleGenerator()
            article_content = article_gen.generate(
                self.params['requirements'],
                self.params['word_count']
            )
            
            # 更新状态：开始SEO优化
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.RUNNING,
                progress=0.3,
                message="正在进行SEO优化..."
            ))
            
            # SEO优化
            seo_opt = SEOOptimizer()
            optimized_content = seo_opt.optimize(article_content)
            
            # 更新状态：开始生成图片
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.RUNNING,
                progress=0.6,
                message="正在生成配图..."
            ))
            
            # 生成图片
            image_gen = ImageGenerator()
            images = image_gen.generate(
                optimized_content,
                self.params['image_style'],
                self.params['watermark_text']
            )
            
            # 更新状态：开始生成文档
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.RUNNING,
                progress=0.9,
                message="正在生成文档..."
            ))
            
            # 生成文档
            doc_writer = DocumentWriter()
            doc_path = doc_writer.create_document(optimized_content, images)
            
            # 完成
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.COMPLETED,
                progress=1.0,
                message="生成完成"
            ))
            
            self.finished.emit(True, doc_path)
            
        except Exception as e:
            self.logger.error(f"生成失败: {str(e)}")
            self.progress_updated.emit(GenerationState(
                status=TaskStatus.FAILED,
                progress=0.0,
                message=f"生成失败: {str(e)}"
            ))
            self.finished.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SEO文章智能生成系统')
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # 初始化配置
        try:
            self.config = Config()
        except ConfigError as e:
            QMessageBox.critical(self, '配置错误', str(e))
            sys.exit(1)
        
        # 创建主窗口部件和布局
        self._setup_ui()
        
        # 初始化状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('就绪')
        
        # 初始化日志
        self.logger = logging.getLogger(__name__)
    
    def _setup_ui(self):
        """设置UI界面"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 文章要求输入
        requirements_layout = QHBoxLayout()
        requirements_label = QLabel('文章要求：')
        self.requirements_input = QLineEdit()
        self.requirements_input.setPlaceholderText('请输入文章主题和要求')
        requirements_layout.addWidget(requirements_label)
        requirements_layout.addWidget(self.requirements_input)
        layout.addLayout(requirements_layout)
        
        # 文章字数设置
        word_count_layout = QHBoxLayout()
        word_count_label = QLabel('文章字数：')
        self.word_count_input = QSpinBox()
        self.word_count_input.setRange(500, 5000)
        self.word_count_input.setValue(1000)
        self.word_count_input.setSingleStep(100)
        word_count_layout.addWidget(word_count_label)
        word_count_layout.addWidget(self.word_count_input)
        layout.addLayout(word_count_layout)
        
        # 图片风格选择
        image_style_layout = QHBoxLayout()
        image_style_label = QLabel('图片风格：')
        self.image_style_input = QComboBox()
        self.image_style_input.addItems(['写实风格', '水彩画风', '油画风格', '插画风格', '素描风格'])
        image_style_layout.addWidget(image_style_label)
        image_style_layout.addWidget(self.image_style_input)
        layout.addLayout(image_style_layout)
        
        # 水印位置选择
        watermark_pos_layout = QHBoxLayout()
        watermark_pos_label = QLabel('水印位置：')
        self.watermark_pos_input = QComboBox()
        self.watermark_pos_input.addItems(['左上角', '右上角', '左下角', '右下角', '居中'])
        watermark_pos_layout.addWidget(watermark_pos_label)
        watermark_pos_layout.addWidget(self.watermark_pos_input)
        layout.addLayout(watermark_pos_layout)
        
        # 水印内容输入
        watermark_text_layout = QHBoxLayout()
        watermark_text_label = QLabel('水印内容：')
        self.watermark_text_input = QLineEdit()
        self.watermark_text_input.setPlaceholderText('请输入水印文字')
        watermark_text_layout.addWidget(watermark_text_label)
        watermark_text_layout.addWidget(self.watermark_text_input)
        layout.addLayout(watermark_text_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 生成按钮
        self.generate_button = QPushButton('生成文章')
        self.generate_button.clicked.connect(self.generate_article)
        layout.addWidget(self.generate_button)
        
        # 添加弹性空间
        layout.addStretch()
    
    def generate_article(self):
        """开始生成文章"""
        # 验证输入
        if not self._validate_inputs():
            return
        
        # 禁用界面
        self._set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        
        # 准备参数
        params = {
            'requirements': self.requirements_input.text(),
            'word_count': self.word_count_input.value(),
            'image_style': self.image_style_input.currentText(),
            'watermark_position': self.watermark_pos_input.currentText(),
            'watermark_text': self.watermark_text_input.text()
        }
        
        # 创建并启动生成线程
        self.generation_thread = GenerationThread(params)
        self.generation_thread.progress_updated.connect(self._update_progress)
        self.generation_thread.finished.connect(self._generation_finished)
        self.generation_thread.start()
    
    def _validate_inputs(self) -> bool:
        """验证输入参数"""
        if not self.requirements_input.text().strip():
            QMessageBox.warning(self, '警告', '请输入文章要求')
            return False
        
        if not self.watermark_text_input.text().strip():
            QMessageBox.warning(self, '警告', '请输入水印内容')
            return False
        
        return True
    
    def _set_ui_enabled(self, enabled: bool):
        """设置UI控件的启用状态"""
        self.requirements_input.setEnabled(enabled)
        self.word_count_input.setEnabled(enabled)
        self.image_style_input.setEnabled(enabled)
        self.watermark_pos_input.setEnabled(enabled)
        self.watermark_text_input.setEnabled(enabled)
        self.generate_button.setEnabled(enabled)
    
    def _update_progress(self, state: GenerationState):
        """更新进度状态"""
        self.progress_bar.setValue(int(state.progress * 100))
        self.statusBar.showMessage(state.message)
    
    def _generation_finished(self, success: bool, result: str):
        """生成完成的处理"""
        self._set_ui_enabled(True)
        
        if success:
            QMessageBox.information(self, '成功', f'文章生成完成！\n文档保存路径：{result}')
        else:
            QMessageBox.critical(self, '错误', f'生成失败：{result}')
        
        self.progress_bar.setVisible(False)
        self.statusBar.showMessage('就绪')

def start_gui():
    """启动GUI界面"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    start_gui()