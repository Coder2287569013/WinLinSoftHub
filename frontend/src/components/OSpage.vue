<script setup>
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
<style scoped>
.links-os {
    display: flex;
    justify-content: center; 
    align-items: center; 
    height: 100vh;
}
.windows a {
    font-size: 50px;
    color: rgb(0,170,255);
    margin-right: 50vh;
}
.linux a {
    font-size: 50px;
    background: linear-gradient(to left,
                    black,white,yellow,white,black);
    -webkit-background-clip: text;
    color: transparent;
}
</style>