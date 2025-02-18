import re
from collections import Counter

class SEOOptimizer:
    def optimize(self, content):
        """
        对文章内容进行SEO优化
        """
        optimized_content = self._optimize_keywords(content)
        optimized_content = self._optimize_structure(optimized_content)
        optimized_content = self._add_meta_tags(optimized_content)
        
        return optimized_content
    
    def _optimize_keywords(self, content):
        """
        优化关键词密度，保持在2%-3%之间
        """
        # 分析当前关键词密度
        words = re.findall(r'\w+', content.lower())
        word_count = len(words)
        word_freq = Counter(words)
        
        # 获取频率最高的词作为关键词
        keywords = [word for word, count in word_freq.most_common(5)
                   if len(word) > 1]  # 排除单字词
        
        # 调整关键词密度
        for keyword in keywords:
            current_density = word_freq[keyword] / word_count * 100
            if current_density < 2:
                # 增加关键词出现次数
                content = self._add_keywords(content, keyword)
            elif current_density > 3:
                # 减少关键词出现次数
                content = self._reduce_keywords(content, keyword)
        
        return content
    
    def _optimize_structure(self, content):
        """
        优化文章结构，确保层次分明
        """
        # 分析并调整标题层级
        lines = content.split('\n')
        current_level = 0
        structured_lines = []
        
        for line in lines:
            if line.strip().startswith('#'):
                level = len(re.match(r'^#+', line).group())
                if level - current_level > 1:
                    # 调整标题层级
                    line = '#' * (current_level + 1) + line[level:]
                current_level = level
            structured_lines.append(line)
        
        # 确保段落长度适中
        content = '\n'.join(structured_lines)
        paragraphs = re.split(r'\n\s*\n', content)
        optimized_paragraphs = []
        
        for para in paragraphs:
            if len(para.strip()) > 500:  # 段落过长
                sentences = re.split(r'[。！？]', para)
                mid = len(sentences) // 2
                para = '。'.join(sentences[:mid]) + '。\n\n' + \
                       '。'.join(sentences[mid:]) + '。'
            optimized_paragraphs.append(para)
        
        return '\n\n'.join(optimized_paragraphs)
    
    def _add_meta_tags(self, content):
        """
        添加SEO相关的META信息
        """
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = "SEO优化文章"
        
        # 提取描述
        first_para = re.search(r'\n\n([^#\n].+?)\n\n', content)
        description = first_para.group(1) if first_para else title
        
        # 提取关键词
        words = re.findall(r'\w+', content.lower())
        word_freq = Counter(words)
        keywords = ', '.join(word for word, _ in word_freq.most_common(5)
                           if len(word) > 1)
        
        # 添加META标签
        meta_tags = f"""<!--SEO Meta Tags-->
<title>{title}</title>
<meta name=\"description\" content=\"{description[:200]}\">
<meta name=\"keywords\" content=\"{keywords}\">
<!--End SEO Meta Tags-->

"""
        
        return meta_tags + content
    
    def _add_keywords(self, content, keyword):
        """
        增加关键词出现频率
        """
        paragraphs = content.split('\n\n')
        for i in range(len(paragraphs)):
            if i % 3 == 0 and keyword not in paragraphs[i].lower():
                sentences = paragraphs[i].split('。')
                if len(sentences) > 1:
                    sentences.insert(1, f"关于{keyword}，")
                    paragraphs[i] = '。'.join(sentences)
        return '\n\n'.join(paragraphs)
    
    def _reduce_keywords(self, content, keyword):
        """
        减少关键词出现频率
        """
        # 使用同义词替换部分关键词
        synonyms = {
            '技术': ['科技', '工艺', '方法'],
            '智能': ['智慧', '聪明', '智囊'],
            '系统': ['平台', '框架', '体系'],
            '开发': ['研发', '创建', '构建'],
            '应用': ['使用', '运用', '实施']
        }
        
        if keyword in synonyms:
            for synonym in synonyms[keyword]:
                content = content.replace(keyword, synonym, 
                                        content.count(keyword) // 3)
        
        return content