<script setup>
    const data = ['windows', 'linux']
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
    </div>
</template>