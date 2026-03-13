<template>
  <div class="app">
    <div class="card">
      <h1 class="title">✨ 儿童故事生成器 ✨</h1>
      <p class="subtitle">输入一个故事主题，让我为你创作一个精彩的小故事！</p>
      
      <div class="input-section">
        <label class="input-label" for="story-theme">故事主题：</label>
        <input
          id="story-theme"
          v-model="theme"
          @keyup.enter="generateStory"
          class="input-field"
          type="text"
          placeholder="例如：魔法森林、太空冒险、友谊、勇敢的小猫..."
          :disabled="loading"
        />
        <button
          class="generate-btn"
          @click="generateStory"
          :disabled="!theme.trim() || loading"
        >
          {{ loading ? '创作中...' : '生成故事 📖' }}
        </button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        🧙‍️ 敖广正在为你创作精彩故事...<br>
        <span class="loading-tip">⏱️ 生成时间大概 10-30 秒，请耐心等待，不要刷新界面</span>
      </div>
      
      <!-- 错误状态 -->
      <div v-if="error" class="error">
        ❌ {{ error }}
      </div>
      
      <!-- 故事显示 -->
      <div v-if="story" class="story-section card">
        <h2 class="story-title">📖 {{ story.theme }}的故事</h2>
        <div class="story-content">{{ story.story }}</div>
        <p style="margin-top: 15px; color: #666; font-size: 0.9rem;">
          字数：{{ story.word_count }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { generateStoryApi } from './api'

export default {
  name: 'App',
  setup() {
    const theme = ref('')
    const story = ref(null)
    const loading = ref(false)
    const error = ref(null)
    
    const generateStory = async () => {
      if (!theme.value.trim()) {
        error.value = '请输入故事主题'
        return
      }
      
      loading.value = true
      error.value = null
      story.value = null
      
      try {
        const data = await generateStoryApi({
          theme: theme.value.trim(),
          max_words: 500
        })
        story.value = data
        
        // 清空输入框
        // theme.value = ''
        
      } catch (err) {
        console.error('生成故事失败:', err)
        error.value = `故事生成失败: ${err.message}`
      } finally {
        loading.value = false
      }
    }
    
    return {
      theme,
      story,
      loading,
      error,
      generateStory
    }
  }
}
</script>