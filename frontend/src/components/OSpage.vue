<script setup>
import axios from 'axios';
import {ref, onMounted, computed} from 'vue';
const data = ref();
onMounted(async () => {
    try {
        const response = await axios.get("https://wlshback.onrender.com/get-user-activity");
        data.value = response.data;
        console.log(data.value);
    } catch (error) {
        console.log(error);
    }
const isNotActive = computed(() => {
    return data.value == '1';
})
})
</script>

<template> 
    <head>
        <title>WinLinSoftHub: Home</title>
    </head>
    <div class="links-os">
        <div class="windows">
            <router-link :to="`/win/category`">
                Windows
            </router-link>
        </div>
        <div class="linux">
            <router-link :to="`/lin/os-page`">
                Linux
            </router-link>
        </div>
        <button class="from for" :disabled="isNotActive">
            Hello
        </button>
    </div>
</template>