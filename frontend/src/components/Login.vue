<script setup>
import axios from 'axios';
import {ref, onMounted, computed, inject} from 'vue';

const existUser = ref({login: '', password: ''});
const userActivity = ref({username: '', is_active: false});
const dataUsers = ref();
const userData = inject('userData');
var userActive = false;
var foundUser = false;

async function hashPassword(password) {
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
            foundUser = true;
            if (existUser.value.password == dataUsers.value[i][2]) {
                userActive = true;
                userActivity.value.username = existUser.value.login;
                userActivity.value.is_active = userActive;
                console.log(userActivity);
                try {
                    const resp = await axios.post('https://wlshback.onrender.com/post-users-activity', userActivity);
                    alert(resp.data.message || "Successfully logined!");
                    const responseActivity = await axios.get("https://wlshback.onrender.com/get-user-activity");
                    userData.value = responseActivity.data;
                } catch (error) {
                    console.log(error);
                    alert(error.response.data.message);
                }
            }
            else {
                alert("Incorrect username or password!");
            }
        } 
    }
    if (!foundUser) {
        alert("User is not existing");
    }
}
</script>

<template>
    <head>
        <title>WinLinSoftHub: Login</title>
    </head>
    <div class="container">
        <div class="description">Login</div>
        <div class="input-group">
            <label for="usernoe">Username or Email:</label>
            <input v-model="existUser.login" id="usernoe" placeholder="Type Username or Email"><br>
        </div>
        <div class="input-group">
            <label for="password">Password:</label>
            <input type="password" v-model="existUser.password" id="password" placeholder=" Type Password"><br>
        </div>
        <button @click="checkUser">Login</button>
    </div>
</template>
<style scoped>
.container {
  margin: auto;
  width: 50rch;
  height: 30rch;
  margin-top: 50px;
  border-radius: 10px;
  background-color: #333;
  padding: 20px;
}
.container .description {
    text-align: center;
}
.container .input-group label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}
.container .input-group input{
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}
.container .input-group {
  margin: 10px 0px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.container .input-group input {
    flex-grow: 1;
}
.container button {
  background-color: #04AA6D;
  color: white;
  border: none;
  padding: 12px 40px;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}
</style>