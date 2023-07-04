<template>
    <div class="chat-container">
        <div class="chat-header">
            <h2>Chat with Matrix Mind <img class="logo" src="@/assets/logo.png" alt="Logo" /></h2>
        </div>
        <div class="chat-body" style="max-height: 500px; overflow-y: auto;">
            <div class="message-list" ref="messageList">
                <div v-for="(message, index) in messages" :key="index" :class="message.type">
                    <div class="message-wrapper">
                        <div class="message-content">{{ message.text }}</div>
                        <div class="message-timestamp" style="margin-right: 10px; margin-top: 20px">{{ message.timestamp }}</div>
                    </div>
                </div>
            </div>
            <div v-if="loading" class="loading-icon">Loading...</div>
        </div>
        <div class="chat-footer">
            <form class="message-form" @submit.prevent="sendMessage('user'); newMessage = ''">
                <div class="message-input-container">
                    <input type="text" v-model="newMessage" placeholder="Type your message here" />
                    <button type="submit" class="send-button" style="margin-left: 30px"></button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            messages: [],
            newMessage: '',
            loading: false
        };
    },
    async created() {
        try {
            this.loading = true;
            const res = await axios.get('http://localhost:8000/first_generate');
            console.log(res)
            const message = {
                text: res.data.message,
                type: 'received',
                timestamp: new Date().toLocaleTimeString()
            };
            this.messages.push(message);
        } catch (err) {
            console.error(err);
        } finally {
            this.loading = false;
        }
    },
    methods: {
        async sendMessage(type) {
            if (this.newMessage.trim() !== '') {
                const userMessage = {
                    text: this.newMessage,
                    type: type === 'user' ? 'sent' : 'received',
                    sender: type === 'user' ? 'user' : 'bot',
                    timestamp: new Date().toLocaleTimeString()
                };
                this.messages.push(userMessage);

                try {
                    this.loading = true;
                    const res = await axios.post('http://localhost:8000/generate', { msg: this.newMessage });
                    const botMessage = {
                        text: res.data.message,
                        type: 'received',
                        sender: 'bot',
                        timestamp: new Date().toLocaleTimeString()
                    };
                this.messages.push(botMessage);
                } catch (err) {
                    console.error(err);
                    const botMessage = {
                        text: "There was some error. Please try again.",
                        type: 'received',
                        sender: 'bot',
                        timestamp: new Date().toLocaleTimeString()
                    };
                    this.messages.push(botMessage);
                } finally {
                    this.loading = false;
                }
                this.newMessage = '';
            }
        }        
    }
}
</script>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    max-width: 800px;
    margin: 0 auto;
    height: 100%;
    padding: 0 20px;
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60px;
    background-color: #fff;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.chat-header h2 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
}

.chat-header .logo {
    width: 40px;
    height: 40px;
    margin-left: 10px;
}

.chat-body {
    flex: 1;
    padding: 20px;
}

.sent {
    display: flex;
    flex-direction: row-reverse;
    margin-bottom: 10px;
}

.received {
    display: flex;
    flex-direction: row;
    margin-bottom: 10px;
}

.sent .message-wrapper {
    display: flex;
    flex-direction: row-reverse;
}

.received .message-wrapper {
    display: flex;
    flex-direction: row;
}

.message-wrapper {
    display: flex;
    flex-direction: row-reverse;
}

.message-content {
    padding: 10px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    max-width: 70%;
    word-wrap: break-word;
    text-align: left; /* added this line */

}

.message-timestamp {
    font-size: 12px;
    color: #999;
    margin-top: 5px;
    margin-right: 3px;
    text-align: right;
}

.chat-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80px;
    background-color: #fff;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.message-form {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.message-input-container {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 600px;
    margin-right: 10px;
    display: flex;
    align-items: center;
}

.message-input-container input[type="text"] {
    flex: 1;
    padding: 10px;
    border-radius: 30px;
    border: none;
    background-color: #f5f5f5;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    color: #333;
}

.send-button {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #979498;
    border: none;
    cursor: pointer;
    background-image: url("@/assets/sand.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 50%;
}

.loading-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    font-weight: bold;
    margin-top: 20px;
}
</style>