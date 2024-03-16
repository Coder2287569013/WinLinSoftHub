<script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  const route = useRoute();
  const osParam = ref(route.params.os || '');

  const data = ref({});

  onMounted(async () => {
    try {
      await axios.post('https://wlshback.onrender.com/get-lin-os', osParam);
      const response = await axios.get("https://wlshback.onrender.com/categories-lin");
      data.value = response.data;
    } catch (error) {
      console.log(error);
    }
  });
</script>

<template> 
  <head>
    <title>WinLinSoftHub: {{ osParam }} Categories</title>
  </head>
  <div class="db-info-l" v-if="data">
      <router-link class="info-category" :to="`/lin/${osParam}/progs/${category_dt}`" v-for="category_dt in data">
        {{ category_dt }}
      </router-link>
  </div>
</template>

<style scoped>
.db-info-l {
  display: grid;
  grid-template-columns: auto auto auto;
}
.info-category {
  font-size: 22px;
}
</style>