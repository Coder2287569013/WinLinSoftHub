<script setup>
    import axios from 'axios';
    import { ref, onMounted } from 'vue';

    const data = ref({});

    onMounted(async () => {
        try {
        const response = await axios.get("http://127.0.0.1:8000/lin-os");
        data.value = response.data;
        console.log(data.value);
        } catch (error) {
        console.log(error);
        }
    });
</script>
<!-- CONTINUE -->
<template> 
    <head>
        <title>WinLinSoftHub: Linux OS</title>
    </head>
    <div class="links-linOS" v-for="os in data">
        <router-link :to="`/lin/${os}/category`">
            {{ os }}
        </router-link>
    </div>
</template>