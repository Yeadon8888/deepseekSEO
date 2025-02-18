import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QSpinBox,
                             QPushButton, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from article_generator import ArticleGenerator
from image_generator import ImageGenerator
from seo_optimizer import SEOOptimizer
from document_writer import DocumentWriter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SEO文章智能生成系统')
        self.setMinimumWidth(600)
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 文章要求输入
        requirements_layout = QHBoxLayout()
        requirements_label = QLabel('文章要求：')
        self.requirements_input = QLineEdit()
        requirements_layout.addWidget(requirements_label)
        requirements_layout.addWidget(self.requirements_input)
        layout.addLayout(requirements_layout)
        
        # 文章字数设置
        word_count_layout = QHBoxLayout()
        word_count_label = QLabel('文章字数：')
        self.word_count_input = QSpinBox()
        self.word_count_input.setRange(100, 10000)
        self.word_count_input.setValue(1000)
        self.word_count_input.setSingleStep(100)
        word_count_layout.addWidget(word_count_label)
        word_count_layout.addWidget(self.word_count_input)
        layout.addLayout(word_count_layout)
        
        # 图片风格选择
        image_style_layout = QHBoxLayout()
        image_style_label = QLabel('图片风格：')
        self.image_style_input = QComboBox()
        self.image_style_input.addItems(['写实', '卡通', '艺术', '简约'])
        image_style_layout.addWidget(image_style_label)
        image_style_layout.addWidget(self.image_style_input)
        layout.addLayout(image_style_layout)
        
        # 水印位置选择
        watermark_pos_layout = QHBoxLayout()
        watermark_pos_label = QLabel('水印位置：')
        self.watermark_pos_input = QComboBox()
        self.watermark_pos_input.addItems(['左上角', '右上角', '左下角', '右下角', '中心'])
        watermark_pos_layout.addWidget(watermark_pos_label)
        watermark_pos_layout.addWidget(self.watermark_pos_input)
        layout.addLayout(watermark_pos_layout)
        
        # 水印内容输入
        watermark_text_layout = QHBoxLayout()
        watermark_text_label = QLabel('水印内容：')
        self.watermark_text_input = QLineEdit()
        watermark_text_layout.addWidget(watermark_text_label)
        watermark_text_layout.addWidget(self.watermark_text_input)
        layout.addLayout(watermark_text_layout)
        
        # 生成按钮
        self.generate_button = QPushButton('生成文章')
        self.generate_button.clicked.connect(self.generate_article)
        layout.addWidget(self.generate_button)
        
        # 初始化生成器
        self.article_gen = ArticleGenerator()
        self.image_gen = ImageGenerator()
        self.seo_opt = SEOOptimizer()
        self.doc_writer = DocumentWriter()
    
    def generate_article(self):
        try:
            # 获取输入值
            requirements = self.requirements_input.text()
            word_count = self.word_count_input.value()
            image_style = self.image_style_input.currentText()
            watermark_position = self.watermark_pos_input.currentText()
            watermark_text = self.watermark_text_input.text()
            
            # 验证输入
            if not requirements:
                QMessageBox.warning(self, '警告', '请输入文章要求')
                return
            if not watermark_text:
                QMessageBox.warning(self, '警告', '请输入水印内容')
                return
            
            # 转换水印位置格式
            position_map = {
                '左上角': 'top-left',
                '右上角': 'top-right',
                '左下角': 'bottom-left',
                '右下角': 'bottom-right',
                '中心': 'center'
            }
            watermark_position = position_map[watermark_position]
            
            # 生成文章内容
            self.generate_button.setEnabled(False)
            self.generate_button.setText('正在生成...')
            
            article_content = self.article_gen.generate(requirements, word_count)
            optimized_content = self.seo_opt.optimize(article_content)
            images = self.image_gen.generate(
                article_content,
                image_style,
                watermark_position,
                watermark_text
            )
            
            # 输出Word文档
            self.doc_writer.create_document(optimized_content, images)
            
            QMessageBox.information(self, '成功', '文章生成完成！')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成过程中出现错误：{str(e)}')
        
        finally:
            self.generate_button.setEnabled(True)
            self.generate_button.setText('生成文章')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()