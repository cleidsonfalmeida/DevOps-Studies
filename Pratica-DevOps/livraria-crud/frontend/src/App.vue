<template>
  <div id="app">
    <h1>Livraria Virtual</h1>
    <ListaLivros />
  </div>
</template>

<script>
import ListaLivros from './components/ListaLivros.vue'

export default {
  components: {
    ListaLivros
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 20px;
}
</style>
