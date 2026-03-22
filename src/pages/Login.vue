<script setup lang="ts">
import { onMounted, reactive, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import AutofillableField from '@/components/Core/AutofillableField.vue'
import PasswordField from '@/components/Core/PasswordField.vue'
import { useI18nUtils } from '@/composables'
import { useAppStore } from '@/stores'
import { LoginPayload } from '@/types/qbit/payloads'

const { t } = useI18nUtils()
const router = useRouter()
const route = useRoute()

const appStore = useAppStore()

const loginForm = reactive<LoginPayload>({
  username: '',
  password: '',
})

async function login() {
  const response = await appStore.login(loginForm.username, loginForm.password)

  if (appStore.isAuthenticated) {
    toast.success(t('login.success'))
    redirectOnSuccess()
  } else {
    let message = t('login.error')
    message += `\nError code: ${response.status} (${response.data})`
    toast.error(message)
  }
}

function redirectOnSuccess() {
  const redirect = route.query.redirect as string | undefined
  // Only allow relative paths — reject absolute URLs and protocol-relative paths
  // to prevent open redirect attacks (e.g. ?redirect=https://evil.com)
  if (redirect && redirect.startsWith('/') && !redirect.startsWith('//')) {
    void router.push(redirect)
  } else {
    void router.push({ name: 'dashboard' })
  }
}

onMounted(() => {
  // Auto-login via URL query params (?username=&password=) was removed —
  // credentials in URLs are stored in browser history and server access logs.
})

watchEffect(() => {
  if (appStore.isAuthenticated) {
    redirectOnSuccess()
  }
})
</script>

<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="mx-auto pa-4 elevation-10" rounded="xl" min-width="320" max-width="450" width="100%" style="background: rgba(var(--v-theme-surface), 0.8); backdrop-filter: blur(10px);">
      <div class="text-center mb-4">
        <v-card-title class="text-h4 font-weight-bold text-accent">{{ t('login.title') }}</v-card-title>
        <v-card-subtitle class="text-h6 mt-1">{{ t('login.subtitle') }}</v-card-subtitle>
      </div>
      <v-card-text>
        <form @submit.prevent="login">
          <AutofillableField
            id="username"
            v-model="loginForm.username"
            :title="t('login.username')"
            autocomplete="username"
            autofocus
            name="username"
            prepend-icon="mdi-account"
            @submit="login" />
          <PasswordField
            id="password"
            v-model="loginForm.password"
            :title="t('login.password')"
            autocomplete="current-password"
            name="password"
            prepend-icon="mdi-lock"
            @submit="login" />
        </form>
      </v-card-text>
      <v-card-actions>
        <v-btn variant="elevated" block color="accent" @click="login">
          {{ t('login.submit') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
