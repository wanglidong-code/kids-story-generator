import re
from typing import Optional

def count_words(text: str) -> int:
    """计算中文字数（包括标点符号）"""
    # 移除多余的空白字符
    text = re.sub(r'\s+', '', text)
    return len(text)

def validate_story_content(story: str, max_words: int = 500) -> bool:
    """验证故事内容是否符合要求"""
    if not story or len(story.strip()) == 0:
        return False
    
    word_count = count_words(story)
    if word_count > max_words:
        return False
    
    # 检查是否包含不适宜儿童的内容（简单过滤）
    inappropriate_keywords = ['暴力', '恐怖', '血腥', '成人', '色情']
    for keyword in inappropriate_keywords:
        if keyword in story:
            return False
    
    return True

def format_story_for_children(story: str) -> str:
    """格式化故事内容，使其更适合儿童阅读"""
    # 确保故事以句号结尾
    story = story.strip()
    if not story.endswith('。') and not story.endswith('.') and not story.endswith('!') and not story.endswith('！') and not story.endswith('?') and not story.endswith('？'):
        story += '。'
    
    # 添加适当的段落分隔（如果故事较长）
    if len(story) > 200:
        # 在适当的位置添加换行
        sentences = re.split(r'[。！？]', story)
        formatted_sentences = []
        current_length = 0
        
        for sentence in sentences:
            if sentence.strip():
                formatted_sentences.append(sentence + '。')
                current_length += len(sentence)
                
                # 每150-200字左右分段
                if current_length > 180:
                    formatted_sentences.append('\n')
                    current_length = 0
        
        story = ''.join(formatted_sentences).strip()
        # 移除最后的换行符
        if story.endswith('\n'):
            story = story[:-1]
    
    return story