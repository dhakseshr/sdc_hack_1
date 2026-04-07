import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFeed } from '../services/api'

export const useFeedStore = defineStore('feed', () => {
  const posts = ref([])
  const loading = ref(false)

  async function fetchFeed() {
    loading.value = true
    try {
      const res = await getFeed()
      posts.value = res.data.posts || res.data
    } catch (err) {
      console.error('Failed to fetch feed:', err)
      posts.value = []
    } finally {
      loading.value = false
    }
  }

  return { posts, loading, fetchFeed }
})
