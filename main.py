"""
儿童绘本生成器 - Kids Story Generator
一个基于 AI 的儿童绘本故事生成应用
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="儿童绘本生成器",
    description="基于 AI 生成儿童绘本故事和插图",
    version="0.1.0"
)


class StoryRequest(BaseModel):
    """故事生成请求模型"""
    theme: str  # 故事主题
    age_range: str  # 目标年龄段，如 "3-5 岁"
    length: str = "short"  # 故事长度：short/medium/long
    style: Optional[str] = "fantasy"  # 故事风格


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
    # TODO: 实现 AI 故事生成逻辑
    return StoryResponse(
        title=f"《{request.theme}的冒险》",
        content=f"这是一个关于{request.theme}的故事...",
        illustrations=["scene1.png", "scene2.png", "scene3.png"],
        age_range=request.age_range
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# TODO: 实现故事生成逻辑
