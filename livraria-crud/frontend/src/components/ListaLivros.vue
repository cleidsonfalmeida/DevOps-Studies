<template>
  <div>
    <h2>Lista de Livros</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Autor</th>
          <th>Preço</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="livro in livros" :key="livro.id">
          <td>{{ livro.id }}</td>
          <td>{{ livro.titulo }}</td>
          <td>{{ livro.autor }}</td>
          <td>{{ livro.preco }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ListaLivros',
  data() {
    return {
      livros: []
    }
  },
  mounted() {
    fetch('http://localhost:8000/livros')  // Substituir depois por http://backend:8000 em produção
      .then(response => response.json())
      .then(data => {
        this.livros = data
      })
      .catch(error => {
        console.error('Erro ao buscar livros:', error)
      })
  }
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 8px;
  border: 1px solid #ccc;
}
</style>
