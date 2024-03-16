<script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';

  const data = ref({});

  onMounted(async () => {
    try {
      const response = await axios.get("https://wlshback.onrender.com/categories");
      data.value = response.data;
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
    <router-link class="info-category" :to="`/win/progs/${category_dt}`" v-for="category_dt in data">
      {{ category_dt }}
    </router-link>
  </div>
</template>
<style scoped>
.db-info-w {
  display: grid;
  grid-template-columns: auto auto auto;
}
.info-category {
  font-size: 22px;
}
</style>