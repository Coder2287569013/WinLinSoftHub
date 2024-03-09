<script setup>
  import axios from 'axios';
  import {ref, onMounted, computed} from 'vue';

  async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  };
  const newUser = ref({ username: '', email: '', password: '' });

  const addUser = async () => {
    try {
      newUser.value.password = await hashPassword(newUser.value.password);
      const response = await axios.post('https://wlshback.onrender.com/register', newUser.value);
      alert(response.data.message || 'User added successfully');
    } catch (error) {
      if (error.response && error.response.data && error.response.data.message) {
        alert(error.response.data.message);
      } else {
        console.log(error);
        alert('An error occurred while trying to register. Please try again later.');
      }
    }
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
</template>
<style scoped>
.container {
  margin: auto;
  width: 50rch;
  height: 60rch;
  margin-top: 20px;
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