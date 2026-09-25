<template>
  <q-page class="q-pa-lg">
    <div class="text-h5 q-mb-md">
      SOMI API Connectivity Test
    </div>

    <q-btn
      label="Test Departments API"
      color="primary"
      :loading="loading"
      @click="testApi"
    />

    <q-banner
      v-if="success"
      class="bg-positive text-white q-mt-md"
    >
      API connection successful.
    </q-banner>

    <q-banner
      v-if="errorMessage"
      class="bg-negative text-white q-mt-md"
    >
      {{ errorMessage }}
    </q-banner>

    <div v-if="departments.length" class="q-mt-lg">
      <div class="text-h6 q-mb-sm">
        Departments
      </div>

      <q-list bordered separator>
        <q-item
          v-for="department in departments"
          :key="department.id"
        >
          <q-item-section>
            <q-item-label>
              {{ department.name }}
            </q-item-label>

            <q-item-label caption>
              Code: {{ department.code }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import api from 'src/services/api'

export default {
  name: 'ApiTest',

  setup () {
    const loading = ref(false)
    const success = ref(false)
    const errorMessage = ref('')
    const departments = ref([])

    const testApi = async () => {
      loading.value = true
      success.value = false
      errorMessage.value = ''
      departments.value = []

      try {
        const response = await api.get('/departments/')

        departments.value = response.data
        success.value = true

        console.log('Departments API response:', response.data)
      } catch (error) {
        console.error('Departments API error:', error)

        if (error.response) {
          errorMessage.value =
            `API Error ${error.response.status}: ${JSON.stringify(error.response.data)}`
        } else {
          errorMessage.value =
            `Network Error: ${error.message}`
        }
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      success,
      errorMessage,
      departments,
      testApi
    }
  }
}
</script>