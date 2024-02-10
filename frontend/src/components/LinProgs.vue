<script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';

  const data = ref([]);
  const route = useRoute();
  const categoryParam = ref(route.params.category_l || '');
  const osParam = ref(route.params.os || '');
  const sortOrder = ref('high-to-low'); 

  onMounted(async () => {
    try {
      const response = await axios.get("https://127.0.0.1:8000/info-lin");
      data.value = response.data;
      console.log(data.value);
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
    <title>{{ osParam }}: {{ categoryParam }}</title>
  </head>
  <div>
    <select class="sortSelect" v-model="sortOrder">
      <option value="high-to-low">Rating: High to Low</option>
      <option value="low-to-high">Rating: Low to High</option>
      <option value="alphabetical">Alphabetical</option>
    </select>
    <div class="db-info" v-if="sortedData">
      <div class="info-progs" v-for="item in sortedData">
        <div class="prog-info" v-if="!categoryParam || item.category == categoryParam && item.compatibility.includes(osParam)">
          <img :src="item.url_image" width="128px" height="128px"><br>
          <div class="prog-text">
            Name: {{ item.name }}<br>
            Compatibility: {{ item.compatibility }}<br>
            Rating: {{ item.rating }}<br>
            <div class="install-section">
                <span class="install-label">How to install:</span>
                <ul class="install-commands">
                    <code>
                        <li v-for="(command, index) in item.cmd_install.split(',')" :key="index">
                          {{ index+1 }}. {{ command.trim() }} 
                        </li>
                    </code>
                </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>