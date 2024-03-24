<script setup>
import axios from 'axios';
import {ref, inject, onMounted, onUnmounted} from 'vue';

const existUser = ref({login: '', password: ''});
const userActivity = ref({username: '', is_active: false});
const dataUsers = ref();
const userData = inject('userData');
var userActive = false;
var foundUser = false;
var checkStatus = ref("");
var state = ref("");
var modalWindow = ref(null);

const spanExit = function() {
  modalWindow.value.style.display = "none";
};
onMounted(() => {
  const handleClickOutside = (event) => {
    if (modalWindow.value && event.target === modalWindow.value) {
      modalWindow.value.style.display = "none";
    }
  };

  window.addEventListener('click', handleClickOutside);
  
  modalWindow.handleClickOutside = handleClickOutside;
});

onUnmounted(() => {
  if (modalWindow.handleClickOutside) {
    window.removeEventListener('click', modalWindow.handleClickOutside);
  }
});

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
                    document.getElementById('modalHeader').style.backgroundColor = '#5cb85c';
                    state.value = "Success";
                    checkStatus.value = "Successfully logined!";
                    userData.value = true;
                } catch (error) {
                    console.log(error);
                    state.value = "Error";
                    checkStatus.value = error.response.data.message;
                    document.getElementById('modalHeader').style.backgroundColor = '#f52a2a';
                }
                modalWindow.value.style.display = 'block';
            }
            else {
              state.value = "Error";
              checkStatus.value = "Incorrect username or password!";
              modalWindow.value.style.display = 'block';
              document.getElementById('modalHeader').style.backgroundColor = '#f52a2a';
            }
        } 
    }
    if (!foundUser) {
      state.value = "Error";
      checkStatus.value = "User is not existing";
      modalWindow.value.style.display = 'block';
      document.getElementById('modalHeader').style.backgroundColor = '#f52a2a';
    }
}
</script>

<template>
    <head>
        <title>WinLinSoftHub: Login</title>
    </head>

    <div id="modalLogin" class="modal" ref="modalWindow">
      <div class="modal-content">
        <div class="modal-header" id="modalHeader">
          <span @click="spanExit" class="close">&times;</span>
          <h1>{{ state }}</h1>
        </div>
        <div class="modal-body">
          <p>{{ checkStatus }}</p>
        </div>
      </div>
    </div>

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
        <div class="ret-to-reg">Don't have an account? <router-link :to="`/register`">Register</router-link></div>
    </div>
</template>
<style scoped>
.container {
  margin: auto;
  font-size: 16px;
  width: 600px;
  height: 41rch;
  margin-top: 50px;
  border-radius: 10px;
  background-color: #333;
  padding: 20px;
}

.container .description {
  text-align: center;
  font-size: 16px;
}

.container .input-group {
  margin: 10px 0px;
  align-items: center;
  display: flex;
}

.container .input-group label {
  display: inline-block;
  padding: 12px 12px 12px 0;
  width: 100px;
}

.container .input-group input {
  box-sizing: border-box;
  font-size: 16px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  width: calc(100% - 100px - 24px); 
  margin-left: 12px; 
}

.container button {
  font-size: 16px;
  background-color: #04AA6D;
  color: white;
  border: none;
  padding: 12px 40px;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}
.container .ret-to-reg {
  padding-top: 80px;
}
.modal {
  display: none; 
  position: fixed; 
  z-index: 1; 
  padding-top: 100px; 
  left: 0;
  top: 0;
  width: 100%; 
  height: 100%; 
  overflow: auto; 
  background-color: rgb(0,0,0); 
  background-color: rgba(0,0,0,0.4); 
}

.modal-content {
  position: relative;
  border-radius: 10px;
  background-color: #333;
  margin: auto;
  border: 1px solid #888;
  width: 600px;
  -webkit-animation-name: animatetop;
  -webkit-animation-duration: 0.4s;
  animation-name: animatetop;
  animation-duration: 0.4s
}
.modal-body {padding: 25px 16px; font-size: 16px;}
.modal-header {
  border-radius: 10px;
  padding: 2px 16px;
  background-color: #5cb85c;
  color: white;
}

@-webkit-keyframes animatetop {
  from {top:-300px; opacity:0} 
  to {top:0; opacity:1}
}

@keyframes animatetop {
  from {top:-300px; opacity:0}
  to {top:0; opacity:1}
}

.close {
  color: white;
  float: right;
  margin-right: 10px;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>