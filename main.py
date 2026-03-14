"""
儿童绘本生成器 - Kids Story Generator
一个基于 AI 的儿童绘本故事生成应用
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="儿童绘本生成器",
    description="基于 AI 生成儿童绘本故事和插图",
    version="0.1.0"
)


class StoryRequest(BaseModel):
    """故事生成请求模型"""
    theme: str = Field(..., min_length=1, max_length=100, description="故事主题")
    age_range: str = Field(..., min_length=1, max_length=20, description="目标年龄段，如 '3-5 岁'")
    length: str = Field(default="short", description="故事长度：short/medium/long")
    style: Optional[str] = Field(default="fantasy", max_length=50, description="故事风格")


class StoryResponse(BaseModel):
    """故事生成响应模型"""
    title: str
    content: str
    illustrations: list[str]
    age_range: str


@app.get("/")
async def root():
    """健康检查端点"""
    return {"message": "儿童绘本生成器 API 已启动", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """
    生成儿童绘本故事
    
    - **theme**: 故事主题（如"勇敢的探险"、"友谊的力量"）
    - **age_range**: 目标年龄段
    - **length**: 故事长度
    - **style**: 故事风格
    """
    try:
        logger.info(f"收到故事生成请求：theme={request.theme}, age_range={request.age_range}")
        
        # TODO: 实现 AI 故事生成逻辑
        return StoryResponse(
            title=f"《{request.theme}的冒险》",
            content=f"这是一个关于{request.theme}的故事...",
            illustrations=["scene1.png", "scene2.png", "scene3.png"],
            age_range=request.age_range
        )
    except ValueError as e:
        logger.error(f"参数错误：{e}")
        raise HTTPException(status_code=400, detail=f"参数错误：{str(e)}")
    except Exception as e:
        logger.error(f"故事生成失败：{e}")
        raise HTTPException(status_code=500, detail="故事生成失败，请稍后重试")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
