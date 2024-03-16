<script setup>
import { ref, onMounted, computed, provide, onUnmounted} from 'vue';
import axios from 'axios';

const userData = ref(null);
var modalWindow = ref(null);
provide('userData', userData)

const spanExit = function() {
    modalWindow.value.style.display = "none";
}
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
console.log(isActiveUser)
const AccessForm = function() {
  if (isActiveUser.value == false) {
    modalWindow.value.style.display = 'block';
  } else {
    window.location.href = "https://docs.google.com/forms/d/e/1FAIpQLSf-fyY3aowjJt6qIgEk1GWsrCsXrMSpTv_JybQGhyHj8qMRdg/viewform?usp=sf_link";
  }
}
</script>

<template>
  <header></header>
  <div id="app">
    <div id="modalAccess" class="modal" ref="modalWindow">
      <div class="modal-content2">
        <div class="modal-header2" id="modalHeader2">
          <span @click="spanExit" class="close">&times;</span>
          <h1>Error</h1>
        </div>
        <div class="modal-body2">
          <p>You cannot have an access to this form. Please, <router-link :to="`/register`">Sign Up</router-link> or <router-link :to="`/login`">Sign In</router-link> </p>
        </div>
      </div>
    </div>
    <ul>
      <li><img src="./assets/logo.png" width="64px" height="64px"></li>
      <li><h1>WinLinSoftHub</h1></li>
      <li><router-link :to="`/`">Home</router-link></li>
      <li><router-link :to="`/register`">Register</router-link></li>
      <li><router-link :to="`/login`">Login</router-link></li>
      <li><a @click="AccessForm">Add New App</a>
      </li>
    </ul>
    <router-view />
  </div>
</template>
<style scoped>
ul {
  width: 100%;
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

.modal-content2 {
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
.modal-body2 {padding: 25px 16px; font-size: 16px;}
.modal-header2 {
  border-radius: 10px;
  padding: 2px 16px;
  background-color: #f52a2a;
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