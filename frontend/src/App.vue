<template>
  <div>
    <router-view></router-view>
    <Toast />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Toast from './components/shared/Toast.vue'
</script>
