<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const userData = ref(null);

onMounted(async () => {
    try {
        const response = await axios.get("https://wlshback.onrender.com/get-user-activity");
        userData.value = response.data;
    } catch (error) {
        console.error(error);
    }
});

const isActiveUser = computed(() => {
    return userData.value === true;
});
</script>

<template>
  <header></header>
  <div id="app">
    <ul>
      <li><img src="./assets/logo.png" width="64px" height="64px"></li>
      <li><h1>WinLinSoftHub</h1></li>
      <li><router-link :to="`/`">Home</router-link></li>
      <li><router-link :to="`/register`">Register</router-link></li>
      <li><router-link :to="`/login`">Login</router-link></li>
      <li><a :href="isActiveUser ? 'javascript:void(0);' : 'https://docs.google.com/forms/d/e/1FAIpQLSf-fyY3aowjJt6qIgEk1GWsrCsXrMSpTv_JybQGhyHj8qMRdg/viewform?usp=sf_link'">Add New App</a>
      </li>
    </ul>
    <router-view />
  </div>
</template>
<style scoped>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
  border-radius: 20px;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 24px 16px;
  text-decoration: none;
}
li h1 {
  color: white;
  text-align: left;
  margin-right: 50px;
  padding: 24px 0;
  text-decoration: none;
  font-size: 14px;
}

li a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #04AA6D;
}
</style>
