<template>
  <nav>
    <ul>
      <li><a href="http://localhost:8080/">Home</a></li>
      <li><a href="https://www.linkedin.com/in/lorenzo-padoan-4521a2154/">About</a></li>
      <li>
        <a href="#">API</a>
        <ul class="dropdown" :class="{'error': showError}">
          <li>
            <form @submit.prevent="submitApiKey">
              <label for="api-key">API Key:</label>
              <input type="text" id="api-key" v-model="apiKey" required>
                <!--<label for="model">Model:</label>-->
                <!--<input type="text" id="model" v-model="model" required>-->
              <button type="submit">Confirm</button>
            </form>
            <p v-if="showError" class="error-message">API key error</p>
            <p v-if="showSuccess" class="success-message">Credentials ok</p>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      apiKey: '',
      model: '',
      showError: false,
      showSuccess: false
    }
  },
  methods: {
    async submitApiKey() {
      try {
        const response = await axios.post('http://localhost:8000/api-key', {
          apiKey: this.apiKey,
          model: "" // to do
        })
        console.log(response.data)
        this.showError = false
        this.showSuccess = true
      } catch (error) {
        if (error.response) {
          console.error(error.response.data)
          console.error(error.response.status)
          console.error(error.response.headers)
        } else if (error.request) {
          console.error(error.request)
        } else {
          console.error('Error', error.message)
        }
        this.showError = true
        this.showSuccess = false
      }
    }
  }
}
</script>


<style>
nav {
  background-color: #333;
  color: #fff;
  display: flex;
  justify-content: space-between;
  padding: 1rem;
}

ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin: 0 1rem;
  position: relative;
}

a {
  color: #fff;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0.5rem;
  transition: all 0.2s ease-in-out;
}

a:hover {
  background-color: #fff;
  color: #333;
}

.dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #333;
  padding: 1rem;
}

.dropdown.error {
  display: block;
  color: red;
}

li:hover .dropdown {
  display: block;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  color: #fff;
  margin-bottom: 0.5rem;
}

input[type="text"] {
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  border: none;
  background-color: #fff;
  color: #333;
  font-size: 1rem;
}

button[type="submit"] {
  padding: 0.5rem;
  border-radius: 0.25rem;
  border: none;
  background-color: #fff;
  color: #333;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

button[type="submit"]:hover {
  background-color: #333;
  color: #fff;
}

.error-message {
  margin-top: 0.5rem;
}

.success-message {
  margin-top: 0.5rem;
  color: green;
}
</style>
