<script setup>
import {ref, onMounted, computed} from 'vue';
import axios from 'axios';

export const existUser = ref({login: '', password: ''});
export const userActivity = ref({username: '', is_active: false});
export const dataUsers = ref();
export var userActive = false;

export async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  };

const checkUser = async() => {
    try {
        existUser.value.password = await hashPassword(existUser.value.password);
        const response = await axios.get('https://wlshback.onrender.com/get-users-login');
        dataUsers.value = response.data;
    } catch(error) {
        alert(error);
    };
    for (let i = 0; i < dataUsers.value.length; i++) {
        if (existUser.value.login == dataUsers.value[i][1] || existUser.value.login == dataUsers.value[i][0]) {
            console.log('yes');
            if (existUser.value.password == dataUsers.value[i][2]) {
                alert("Successfully logined!");
                userActive = true;
                userActivity.value.username = existUser.value.login;
                userActivity.value.is_active = userActive;
                console.log(userActivity);
                await axios.post('https://wlshback.onrender.com/users-activity', userActivity);
            }
        }
    }
}
</script>

<template>
    <head>
        <title>WinLinSoftHub: Login</title>
    </head>
    <div>
        <input v-model="existUser.login" placeholder="Username of Login"><br>
        <input type="password" v-model="existUser.password" placeholder="Password"><br>
        <button @click="checkUser">Login</button>
    </div>
</template>