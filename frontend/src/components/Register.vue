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

  const addUser = async() => {
    try {
        newUser.value.password =  await hashPassword(newUser.value.password);
        await axios.post('http://127.0.0.1:8000/new-user-register', newUser.value);
        await axios.get('http://127.0.0.1:8000/add-new-user');
        newUser.value = { username: '', email: '', password: '' };
        alert('User added successfully');
    } catch (error) {
      console.error(error);
      alert('Failed to add user');
    }
  }

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
    <div>
        <input v-model="newUser.username" placeholder="User"><br>
        <input type="email" id="email" v-model="newUser.email" placeholder="Email"><br>
        <div v-if="emailErrors.length">
            <li v-for="error in emailErrors" :key="error">{{ error }}</li>
        </div>
        <input type="password" v-model="newUser.password" placeholder="Password"><br>
        <div v-if="passwordErrors.length">
            <p>Password requirements:</p>
            <ul>
                <li v-for="error in passwordErrors" :key="error">{{ error }}</li>
            </ul>
        </div>
        <button @click="addUser" :disabled="isFormInvalid">Submit</button>
    </div>
</template>