// API 配置文件
const getApiBaseUrl = () => {
  // 如果当前页面是通过 trycloudflare.com 访问的，使用对应的后端 API
  if (window.location.hostname.includes('trycloudflare.com')) {
    return 'https://ict-exemption-shipping-colored.trycloudflare.com'
  }
  // 本地开发环境
  return 'http://localhost:8000'
}

export const API_BASE_URL = getApiBaseUrl()

// 生成故事 API
export const generateStoryApi = async (data) => {
  const response = await fetch(`${API_BASE_URL}/generate-story`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '请求失败')
  }
  
  return await response.json()
}