from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional
import requests

# 导入本地模块
from app.models import StoryRequest, StoryResponse
from app.utils import validate_story_content, format_story_for_children, count_words

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 百炼平台 API 配置
DASHSCOPE_API_KEY = "sk-2d15da9e8c1c48e4bad320251a2d5345"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DASHSCOPE_MODEL = "qwen3.5-plus"

app = FastAPI(
    title="儿童故事生成器 API",
    description="为 9-15 岁儿童生成有趣、安全的短篇故事",
    version="1.0.0"
)

# 配置 CORS - 支持外网访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中建议限制为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_story_ai(theme: str, max_words: int = 500) -> str:
    """
    使用百炼平台 qwen3.5-plus 模型生成儿童故事
    
    Args:
        theme: 故事主题
        max_words: 最大字数限制
    
    Returns:
        生成的故事内容
    """
    # 构建适合儿童的 prompt
    system_prompt = """你是一位专业的儿童文学作家，专门为 9-15 岁儿童创作故事。
你的故事特点：
1. 内容安全、积极向上，适合儿童阅读
2. 语言生动有趣，易于理解
3. 故事结构完整（有开头、发展、结尾）
4. 传递正能量和正确的价值观（友谊、勇气、善良、诚实等）
5. 字数控制在要求范围内"""

    user_prompt = f"""请为 9-15 岁儿童创作一个短篇故事。

故事主题：{theme}
字数要求：不超过{max_words}字

要求：
- 故事要有趣、富有想象力
- 语言简洁生动，适合儿童阅读
- 有完整的故事结构
- 传递积极向上的价值观

请直接输出故事内容，不需要标题和额外说明。"""

    try:
        logger.info(f"调用百炼 API 生成故事，主题='{theme}', max_words={max_words}")
        
        # 重试机制：最多重试 2 次（超时 30 秒）
        max_retries = 2
        last_error = None
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"第 {attempt} 次尝试调用百炼 API...")
                
                response = requests.post(
                    f"{DASHSCOPE_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": DASHSCOPE_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "max_tokens": 2048,
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                
                logger.info(f"百炼 API 响应状态码：{response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    story = result["choices"][0]["message"]["content"].strip()
                    logger.info(f"故事生成成功，原始长度={len(story)}")
                    return story
                else:
                    logger.error(f"百炼 API 调用失败：{response.status_code} - {response.text}")
                    raise Exception(f"AI 服务调用失败：{response.status_code}")
                    
            except requests.Timeout as e:
                last_error = e
                logger.warning(f"第 {attempt} 次尝试超时：{str(e)}")
                if attempt < max_retries:
                    import time
                    time.sleep(1)  # 等待 1 秒后重试
                    continue
                raise
            except requests.RequestException as e:
                last_error = e
                logger.warning(f"第 {attempt} 次尝试失败：{str(e)}")
                if attempt < max_retries:
                    import time
                    time.sleep(1)
                    continue
                raise
        
        # 所有重试都失败
        raise last_error
                
    except requests.Timeout as e:
        logger.error(f"百炼 API 请求超时（已重试{max_retries}次）: {str(e)}")
        raise HTTPException(status_code=503, detail="AI 服务响应超时，请稍后重试")
    except requests.RequestException as e:
        logger.error(f"百炼 API 请求错误（已重试{max_retries}次）: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI 服务请求失败：{str(e)}")
    except Exception as e:
        logger.error(f"故事生成异常：{str(e)}")
        raise HTTPException(status_code=500, detail=f"故事生成失败：{str(e)}")

@app.get("/")
async def root():
    """健康检查端点"""
    return {"message": "儿童故事生成器 API 正常运行", "version": "1.0.0"}

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """
    生成儿童故事
    
    - **theme**: 故事主题（必填）
    - **max_words**: 最大字数（默认 500，范围 100-500）
    """
    try:
        logger.info(f"收到故事生成请求：主题='{request.theme}', 最大字数={request.max_words}")
        
        # 生成故事
        raw_story = generate_story_ai(request.theme, request.max_words)
        
        # 格式化故事
        formatted_story = format_story_for_children(raw_story)
        
        # 验证故事内容
        if not validate_story_content(formatted_story, request.max_words):
            raise HTTPException(status_code=500, detail="生成的故事内容不符合要求")
        
        word_count = count_words(formatted_story)
        
        logger.info(f"故事生成成功：字数={word_count}")
        
        return StoryResponse(
            story=formatted_story,
            word_count=word_count,
            theme=request.theme
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"故事生成失败：{str(e)}")
        raise HTTPException(status_code=500, detail=f"故事生成失败：{str(e)}")

if __name__ == "__main__":
    import uvicorn
    # 绑定到所有网络接口，允许外网访问
    uvicorn.run(app, host="0.0.0.0", port=8000)
