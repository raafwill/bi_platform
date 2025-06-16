<template>
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">📤 Importar Modelo PBIT</h1>
  
      <input type="file" @change="onFileChange" accept=".pbit" class="mb-4" />
  
      <button
        @click="enviarArquivo"
        class="px-4 py-2 bg-blue-600 text-white rounded"
        :disabled="!arquivo"
      >
        Enviar
      </button>
  
      <p class="mt-4" v-if="mensagem">{{ mensagem }}</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { ref } from "vue";
  
  export default {
    setup() {
      const arquivo = ref(null);
      const mensagem = ref("");
  
      const onFileChange = (e) => {
        arquivo.value = e.target.files[0];
      };
  
      const enviarArquivo = async () => {
        if (!arquivo.value) return;
  
        const formData = new FormData();
        formData.append("arquivo", arquivo.value);
  
        try {
          const response = await axios.post("/api/importar-pbit/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          mensagem.value = `✅ Sucesso: ${response.data.mensagem}`;
        } catch (error) {
          mensagem.value = `❌ Erro: ${JSON.stringify(error.response?.data || error.message)}`;
        }
      };
  
      return { arquivo, mensagem, onFileChange, enviarArquivo };
    },
  };
  </script>
  