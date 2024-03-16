<script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';

  const data = ref([]);
  const route = useRoute();
  const categoryParam = ref(route.params.category || '');
  const sortOrder = ref('high-to-low'); 

  onMounted(async () => {
    try {
      const response = await axios.get("https://wlshback.onrender.com/info-win");
      data.value = response.data;
    } catch (error) {
      console.log(error);
    }
  });

  const sortedData = computed(() => {
    if (!data.value) return [];

    if (sortOrder.value == 'high-to-low') {
      return [...data.value].sort((a,b) => b.rating - a.rating);
    } 
    if (sortOrder.value == 'low-to-high') {
      return [...data.value].sort((a,b) => a.rating - b.rating);
    }
    if (sortOrder.value == 'alphabetical') {
      return [...data.value].sort((a,b) => a.name.localeCompare(b.name));
    }
  });

</script>

<template>
  <head>
    <title>Windows: {{ categoryParam }}</title>
  </head>
  <div>
    <select class="sortSelect" v-model="sortOrder">
      <option value="high-to-low">Rating: High to Low</option>
      <option value="low-to-high">Rating: Low to High</option>
      <option value="alphabetical">Alphabetical</option>
    </select>
    <div class="db-info" v-if="sortedData">
      <div class="info-progs" v-for="item in sortedData">
        <div class="prog-info" v-if="!categoryParam || item.category == categoryParam">
          <img :src="item.url_image" width="128px" height="128px"><br>
          <div class="prog-text">
            Name: {{ item.name }}<br>
            Compatibility: {{ item.compatibility }}<br>
            Rating: {{ item.rating }}<br>
            <a :href="item.url_download">Download {{ item.name }}</a><br>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>