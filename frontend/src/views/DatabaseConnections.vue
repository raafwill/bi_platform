<template>
  <div>
    <h2>🔗 Conexões de Banco de Dados</h2>

    <!-- 🔹 Formulário para adicionar/editar conexões -->
    <form @submit.prevent="saveConnection">
      <input v-model="newConnection.name" placeholder="Nome" required />
      <input v-model="newConnection.db_type" placeholder="Tipo (MySQL, PostgreSQL...)" required />
      <input v-model="newConnection.host" placeholder="Host (ex: localhost)" required />
      <input v-model="newConnection.port" placeholder="Porta (ex: 5432)" required />
      <input v-model="newConnection.user" placeholder="Usuário" required />
      <input v-model="newConnection.password" placeholder="Senha" type="password" required />
      <input v-model="newConnection.database" placeholder="Nome do Banco" required />

      <button type="button" @click="testConnection">🛠️ Testar Conexão</button>
      <button type="submit">{{ editing ? "✏️ Atualizar Conexão" : "➕ Adicionar Conexão" }}</button>
      <button v-if="editing" @click="cancelEdit" type="button">❌ Cancelar</button>
    </form>

    <p v-if="testMessage">{{ testMessage }}</p>

    <button @click="fetchConnections">🔄 Atualizar</button>

    <ul>
      <li v-for="conn in connections" :key="conn.id">
        <strong>{{ conn.name }}</strong> - {{ conn.db_type }} @ {{ conn.host }}
        <button @click="editConnection(conn)">✏️ Editar</button>
        <button @click="deleteConnection(conn.id)">🗑️ Excluir</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const connections = ref([]);
const editing = ref(false);
const newConnection = ref({
  name: "",
  db_type: "",
  host: "",
  port: "",
  user: "",
  password: "",
  database: "",
});
const editingId = ref(null);
const testMessage = ref("");

const fetchConnections = async () => {
  try {
    const response = await api.get("connections/");
    connections.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar conexões:", error);
  }
};

const saveConnection = async () => {
  try {
    if (editing.value) {
      await api.put(`connections/update/${editingId.value}/`, newConnection.value);
    } else {
      await api.post("connections/create/", newConnection.value);
    }
    newConnection.value = { name: "", db_type: "", host: "", port: "", user: "", password: "", database: "" };
    editing.value = false;
    fetchConnections();
  } catch (error) {
    console.error("Erro ao salvar conexão:", error);
  }
};

const editConnection = (conn) => {
  newConnection.value = { ...conn };
  editing.value = true;
  editingId.value = conn.id;
};

const cancelEdit = () => {
  newConnection.value = { name: "", db_type: "", host: "", port: "", user: "", password: "", database: "" };
  editing.value = false;
  editingId.value = null;
};

const deleteConnection = async (id) => {
  try {
    await api.delete(`connections/delete/${id}/`);
    fetchConnections();
  } catch (error) {
    console.error("Erro ao deletar conexão:", error);
  }
};

const testConnection = async () => {
  console.log("Testando conexão...");
  try {
    const response = await api.post("connections/test/", newConnection.value);
    testMessage.value = `✅ ${response.data.message}`;
    console.log("Resposta:", response.data);
  } catch (error) {
    console.error("Erro na conexão:", error);
    testMessage.value = `❌ Erro: ${error.response?.data?.error || "Erro desconhecido"}`;
  }
};

onMounted(fetchConnections);
</script>
