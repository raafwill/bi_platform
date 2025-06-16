<template>
  <div class="container">
    <h1>🚀 BI AI Platform</h1>
    <nav>
      <router-link to="/">🏠 Home</router-link> |
      <router-link to="/connections">🔗 Conexões</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
.container {
  text-align: center;
  margin-top: 20px;
}
nav a {
  margin: 0 10px;
  text-decoration: none;
  font-weight: bold;
}
</style>
