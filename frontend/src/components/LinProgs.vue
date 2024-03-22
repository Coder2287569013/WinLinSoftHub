<script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';

  const data = ref([]);
  const route = useRoute();
  const categoryParam = ref(route.params.category_l || '');
  const osParam = ref(route.params.os || '');
  const sortOrder = ref('high-to-low'); 
  const osList = ["Ubuntu", "Arch Linux"];
  const isOsParam = (element) => element == osParam.value;

  onMounted(async () => {
    try {
      const response = await axios.get("https://wlshback.onrender.com/info-lin");
      data.value = response.data;
    } catch (error) {
      console.log(error);
    }
  });

  const parseCommands = function(cmd_install) {
    var listCommands = cmd_install.split('||');
    console.log(listCommands);
    var index = 0;
    if (osParam.value == "Linux Mint") {
      index = 0;
    } else {
      index = osList.findIndex(isOsParam);
    }
    var commands = listCommands[index].split(',');
    return commands
  }

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
                        <li v-for="(command, index) in parseCommands(item.cmd_install)" :key="index">
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