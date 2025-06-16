<template>
    <div class="container">
      <h2>📥 Importar Mapeamento Semântico</h2>
      
      <textarea v-model="jsonData" rows="15" placeholder="Cole aqui o JSON com os mapeamentos"></textarea>
      
      <button @click="sendMappings">🚀 Enviar para API</button>
  
      <p v-if="message" :class="{'success': success, 'error': !success}">
        {{ message }}
      </p>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import api from "@/api";
  
  const jsonData = ref('');
  const message = ref('');
  const success = ref(false);
  
  const sendMappings = async () => {
    try {
      const data = JSON.parse(jsonData.value);
      const response = await api.post("tabelas-semanticas/", data);
      message.value = `✅ ${Array.isArray(response.data) ? response.data.length : 1} mapeamento(s) enviado(s) com sucesso!`;
      success.value = true;
    } catch (error) {
      console.error("Erro ao enviar dados:", error);
      message.value = `❌ Erro ao enviar: ${JSON.stringify(error.response?.data || error.message)}`;
      success.value = false;
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 700px;
    margin: auto;
    padding: 20px;
  }
  textarea {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    font-family: monospace;
  }
  button {
    margin-top: 10px;
    padding: 10px 15px;
  }
  .success {
    color: green;
  }
  .error {
    color: red;
  }
  </style>
  