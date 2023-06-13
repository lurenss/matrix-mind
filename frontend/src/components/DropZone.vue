<template>
  <div v-if="!uploadComplete">
    <div
      class="dropzone"
      @dragover.prevent
      @dragleave="dragging = false"
      @drop="onDrop"
      :class="{ dragging }"
    >
      <div class="upload-icon">
        <i class="fas fa-cloud-upload-alt"></i>
      </div>
      <input type="file" @change="onDrop" ref="fileInput" />
      <div class="upload-text">
        <div v-if="!dragging && !file">Drag & Drop file here</div>
        <div v-else-if="dragging && !file">Drop it, it's hot!</div>
        <div v-else-if="file">{{ file.name }}</div>
      </div>
    </div>
  </div>
  <div v-else>
    <ChatComponent></ChatComponent>
  </div>
  <div v-if="uploadStatus" class="upload-status" :style="{ color: uploadStatusColor }">{{ uploadStatus }}</div>
</template>

<script>
import axios from 'axios'
import ChatComponent from './ChatComponent.vue'

export default {
  data() {
    return {
      dragging: false,
      file: null,
      uploadStatus: null,
      uploadStatusColor: 'inherit',
      uploadComplete: false,
    }
  },
    methods: {
      async onDrop(e) {
        this.dragging = false

        const files = e.dataTransfer ? e.dataTransfer.files : e.target.files
        const file = [...files][0]

        // Check if the file is a CSV file
        if (!file.name.endsWith('.csv')) {
          this.uploadStatus = 'Error: Only CSV files are allowed'
          this.uploadStatusColor = 'red'
          return
        }

        // Reset file input value so the same file can be selected multiple times
        this.$refs.fileInput.value = null

        // Start the file upload
        const formData = new FormData()
        formData.append('file', file)

        try {
          this.uploadStatus = 'Uploading...'
          const response = await axios.post('http://localhost:8000/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          this.file = file
          this.uploadStatus = `Uploaded successfully: ${response.data.filename}`
          this.uploadStatusColor = 'green'
        } catch (error) {
          if (error.response.status === 400) {
            this.uploadStatus = `Error: Insert your API key`
            this.uploadStatusColor = 'red'
            return
          }
        }

        // set uploadComplete to true and start the timer
        setTimeout(() => {
          this.uploadComplete = true
        }, 2000)
      },
    },
    components: {
      ChatComponent,
    },
  }
  </script>

<style scoped>
.dropzone {
  width: 400px;
  height: 200px;
  border: 3px dashed #ccc;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: #aaa;
  transition: border-color 0.3s ease-in-out;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.2);
  padding-top: 40px; /* Added padding from the top */
}

.dropzone.dragging {
  border-color: #4caf50;
}

.upload-icon {
  font-size: 50px;
  color: #ccc;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 16px;
  color: #aaa;
}

input[type='file'] {
  display: none;
}

.upload-status {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #f2f2f2;
  font-family: Arial, sans-serif;
}

/* New styles */
.dropzone {
  background-color: #f5f5f5;
  border: 2px dashed #ccc;
  border-radius: 5px;
  padding: 20px;
  text-align: center;
  transition: border-color 0.3s ease-in-out;
}

.dropzone.dragging {
  border-color: #4caf50;
}

.upload-icon {
  font-size: 50px;
  color: #4caf50;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 16px;
  color: #555;
}

.upload-text span {
  font-weight: bold;
}

.upload-status {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #f2f2f2;
  font-family: Arial, sans-serif;
}
</style>
