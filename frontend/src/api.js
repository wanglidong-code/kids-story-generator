// API 配置文件
const getApiBaseUrl = () => {
  // 如果当前页面是通过 trycloudflare.com 访问的，使用对应的后端 API
  if (window.location.hostname.includes('trycloudflare.com')) {
    return 'https://ict-exemption-shipping-colored.trycloudflare.com'
  }
  // 生产环境：使用相对路径，通过 nginx 反向代理
  // 本地开发环境：使用 localhost
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000'
  }
  // 其他情况（生产环境）使用相对路径
  return ''
}

export const API_BASE_URL = getApiBaseUrl()

// 生成故事 API
export const generateStoryApi = async (data) => {
  const apiPath = API_BASE_URL ? API_BASE_URL + '/generate-story' : '/api/generate-story'
  const response = await fetch(apiPath, {
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