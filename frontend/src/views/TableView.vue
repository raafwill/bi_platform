<template>
    <div class="container">
      <h2>📊 Dados da Tabela: {{ tableName }}</h2>
      <input v-model="tableName" placeholder="Digite o nome da tabela" @keyup.enter="fetchTableData" />
  
      <button @click="fetchTableData">🔄 Carregar Dados</button>
  
      <table v-if="tableData.length">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.id">
            <td v-for="col in columns" :key="col">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
  
      <p v-else>Nenhum dado encontrado.</p>
    </div>
  </template>
  
  <script>
  import api from "@/api";
  
  export default {
    data() {
      return {
        tableName: "",
        tableData: [],
        columns: [],
      };
    },
    methods: {
      async fetchTableData() {
        if (!this.tableName) return;
        try {
          const response = await api.get(`tables/${this.tableName}/`);
          this.tableData = response.data.data;
          this.columns = this.tableData.length ? Object.keys(this.tableData[0]) : [];
        } catch (error) {
          console.error("Erro ao buscar dados:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: auto;
    text-align: center;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background-color: #f4f4f4;
  }
  </style>
  