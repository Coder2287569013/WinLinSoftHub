<script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';

  const data = ref({});

  onMounted(async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/categories");
      data.value = response.data;
      console.log(data.value);
    } catch (error) {
      console.log(error);
    }
  });
</script>

<template> 
  <head>
    <title>WinLinSoftHub: Windows Categories</title>
  </head>
  <div class="db-info-w" v-if="data">
    <div class="info-category" v-for="category_dt in data">
      <router-link :to="`/win/progs/${category_dt}`">
        {{ category_dt }}
      </router-link>
    </div>
  </div>
</template>