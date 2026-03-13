from pydantic import BaseModel, Field
from typing import Optional

class StoryRequest(BaseModel):
    """故事生成请求模型"""
    theme: str = Field(..., min_length=1, max_length=100, description="故事主题")
    max_words: int = Field(500, ge=100, le=500, description="最大字数限制")

class StoryResponse(BaseModel):
    """故事生成响应模型"""
    story: str = Field(..., description="生成的故事内容")
    word_count: int = Field(..., description="故事字数")
    theme: str = Field(..., description="故事主题")