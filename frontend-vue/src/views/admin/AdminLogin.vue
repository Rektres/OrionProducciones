<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { adminAuth } from '@/services/adminAuth';

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const error = ref('');

const form = reactive({
  username: '',
  password: '',
});

const onSubmit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await adminAuth.login(form.username, form.password);
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/admin/servicios';
    router.push(redirect);
  } catch (e) {
    error.value = 'Usuario o contraseña incorrectos.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="admin-shell text-white min-vh-100 d-flex align-items-center justify-content-center" data-bs-theme="dark">
    <div class="card admin-card p-4" style="width: 100%; max-width: 380px">
      <h4 class="text-center mb-4">Administración Orion</h4>
      <form @submit.prevent="onSubmit">
        <div class="mb-3">
          <label class="form-label">Usuario</label>
          <input v-model="form.username" type="text" required class="form-control" autocomplete="username" />
        </div>
        <div class="mb-3">
          <label class="form-label">Contraseña</label>
          <input v-model="form.password" type="password" required class="form-control" autocomplete="current-password" />
        </div>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <button type="submit" class="btn btn-orion w-100" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>
    </div>
  </div>
</template>
