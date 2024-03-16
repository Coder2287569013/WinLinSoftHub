<script setup>
  import axios from 'axios';
  import {ref, computed, onMounted, onUnmounted} from 'vue';
  import { RouterLink } from 'vue-router';

  async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  };
  const newUser = ref({ username: '', email: '', password: '' });
  var checkStatus = ref("");
  var state = ref("");
  var modalWindow = ref(null);
  console.log(modalWindow);

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
  const addUser = async () => {
    try {
      newUser.value.password = await hashPassword(newUser.value.password);
      const response = await axios.post('https://wlshback.onrender.com/register', newUser.value);
      checkStatus.value = `${response.data.message}. Go to the`;
      document.getElementById('modalHeader').style.backgroundColor = '#5cb85c';
      state.value = "Success";
    } catch (error) {
      document.getElementById('modalHeader').style.backgroundColor = '#f52a2a';
      state.value = "Error";
      if (error.response && error.response.data && error.response.data.message) {
        checkStatus.value = error.response.data.message;
      } else {
        console.log(error);
        checkStatus.value = 'An error occurred while trying to register. Please try again later.';
      }
    }
    modalWindow.value.style.display='block';
  };

  const emailErrors = computed(() => {
    const userEmail = newUser.value.email;
    const errors = [];
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!userEmail.match(emailPattern)) {
        errors.push('Please enter a valid email address.');
    }
    return errors;
  })

  const passwordErrors = computed(() => {
    const userPassword = newUser.value.password;
    const errors = [];
    if (typeof userPassword === 'string') {
      if (userPassword.length < 8) {
          errors.push('Password must be at least 8 characters long.');
      }
      if (!userPassword.match(/[A-Z]/)) {
          errors.push('Password must contain at least one uppercase letter.');
      }
      if (!userPassword.match(/[a-z]/)) {
          errors.push('Password must contain at least one lowercase letter.');
      }
    }
    return errors;
  })

  const isFormInvalid = computed(() => {
    return emailErrors.value.length > 0 || passwordErrors.value.length > 0;
  })

</script>

<template>
  <head>
    <title>WinLinSoftHub: Register</title>
  </head>

    <div id="modalRegister" class="modal" ref="modalWindow">
      <div class="modal-content">
        <div class="modal-header" id="modalHeader">
          <span @click="spanExit" class="close">&times;</span>
          <h1>{{ state }}</h1>
        </div>
        <div class="modal-body">
          <p>{{ checkStatus }}<router-link :to="`/login`" v-if="state.includes('Success')">Login Page</router-link></p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="description">Register</div>
      <div class="input-group">
        <label for="username">Username:</label>
        <input v-model="newUser.username" placeholder="Enter Username" id="username"><br>
      </div>
      <div class="input-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="newUser.email" placeholder="Enter Email"><br>
      </div>
      <div v-if="emailErrors.length">
          <li v-for="error in emailErrors" :key="error">{{ error }}</li>
      </div>
      <div class="input-group">
        <label for="password">Password:</label>
        <input type="password" v-model="newUser.password" placeholder="Enter Password"><br>
      </div>
      <div v-if="passwordErrors.length">
          <p>Password requirements:</p>
          <ul>
              <li v-for="error in passwordErrors" :key="error">{{ error }}</li>
          </ul>
      </div>
      <button @click="addUser" :disabled="isFormInvalid">Register</button>
    </div>

    <!-- Продолжение следует, доделать модалку, оформить все красиво, и прописать себе леща, если будет выглядеть как всегда -->
</template>

<style scoped>
.container {
  font-size: 16px;
  margin: auto;
  width: 600px;
  height: 60rch;
  margin-top: 20px;
  border-radius: 10px;
  background-color: #333;
  padding: 20px;
}
.container .description {
    text-align: center;
    font-size: 16px;
}
.container .input-group label {
  width: 100px;
  padding: 12px 12px 12px 0;
  display: inline-block;
}
.container .input-group input{
  font-size: 16px;
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  width: calc(100% - 100px - 24px);
  margin-left: 12px;
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
  font-size: 16px;
  background-color: #04AA6D;
  color: white;
  border: none;
  padding: 12px 40px;
  border-radius: 4px;
  cursor: pointer;
  float: right;
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