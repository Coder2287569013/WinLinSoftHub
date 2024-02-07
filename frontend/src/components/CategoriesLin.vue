<script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  const route = useRoute();
  const osParam = ref(route.params.os || '');

  const data = ref({});

  onMounted(async () => {
    try {
      await axios.post('http://127.0.0.1:8000/get-lin-os', osParam);
      const response = await axios.get("http://127.0.0.1:8000/categories-lin");
      data.value = response.data;
      console.log(data.value);
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
    <div class="info-category" v-for="category_dt in data">
      <router-link :to="`/lin/${osParam}/progs/${category_dt}`">
        {{ category_dt }}
      </router-link>
    </div>
  </div>
</template>