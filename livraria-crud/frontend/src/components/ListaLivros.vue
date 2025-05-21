<template>
  <div>
    <h2>Cadastro de Livro</h2>
    <form @submit.prevent="salvarLivro">
      <input v-model="form.titulo" placeholder="Título" required />
      <input v-model="form.autor" placeholder="Autor" required />
      <input v-model.number="form.preco" type="number" placeholder="Preco" required step="0.01" />
      <button type="submit">{{ editando ? 'Atualizar' : 'Salvar' }}</button>
    </form>

    <div v-if="mensagem" :class="{ sucesso: sucesso, erro: !sucesso }">
      {{ mensagem }}
    </div>

    <table>
      <thead>
        <tr>
          <th>Título</th>
          <th>Autor</th>
          <th>Preço</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="livro in livros" :key="livro.id">
          <td>{{ livro.titulo }}</td>
          <td>{{ livro.autor }}</td>
          <td>{{ livro.preco.toFixed(2) }}</td>
          <td>
            <button @click="editarLivro(livro)">Editar</button>
            <button class="btn-excluir" @click="excluirLivro(livro.id)">Excluir</button>
          </td>
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
      livros: [],
      form: { titulo: '', autor: '', preco: 0 },
      editando: false,
      editId: null,
      mensagem: '',
      sucesso: true,
    }
  },
  mounted() {
    this.buscarLivros()
  },
  methods: {
    async buscarLivros() {
      try {
        const res = await fetch('/api/livros')
        if (!res.ok) throw new Error('Erro ao carregar')
        this.livros = await res.json()
      } catch (err) {
        this.mostrarMensagem('Erro ao carregar livros', false)
      }
    },
    async salvarLivro() {
      const url = this.editando ? `/api/livros/${this.editId}` : '/api/livros'
      const metodo = this.editando ? 'PUT' : 'POST'

      try {
        const res = await fetch(url, {
          method: metodo,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form)
        })
        if (!res.ok) {
          const erro = await res.json()
          throw new Error(erro.detail || 'Erro desconhecido')
        }
        this.buscarLivros()
        this.resetarFormulario()
        this.mostrarMensagem(this.editando ? 'Livro atualizado' : 'Livro cadastrado', true)
      } catch (err) {
        this.mostrarMensagem(`Erro ao salvar livro: ${err.message}`, false)
      }
    },
    editarLivro(livro) {
      this.form = { titulo: livro.titulo, autor: livro.autor, preco: livro.preco }
      this.editando = true
      this.editId = livro.id
    },
    async excluirLivro(id) {
      try {
        const res = await fetch(`/api/livros/${id}`, { method: 'DELETE' })
        if (!res.ok) throw new Error('Erro ao excluir')
        this.buscarLivros()
        this.mostrarMensagem('Livro excluído', true)
      } catch (err) {
        this.mostrarMensagem(`Erro ao excluir livro: ${err.message}`, false)
      }
    },
    resetarFormulario() {
      this.form = { titulo: '', autor: '', preco: 0 }
      this.editando = false
      this.editId = null
    },
    mostrarMensagem(msg, sucesso) {
      this.mensagem = msg
      this.sucesso = sucesso
      setTimeout(() => this.mensagem = '', 3000)
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body {
  background-color: #f7f7f7;
  color: #333;
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

h2 {
  text-align: center;
  margin-top: 20px;
  color: #2c3e50;
}

form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 14px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

.btn-excluir {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-excluir:hover {
  background-color: #c0392b;
}

table {
  width: 90%;
  margin: 0 auto;
  border-collapse: collapse;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

th {
  background-color: #f8f8f8;
  font-weight: bold;
  color: #222;
}

tr:hover {
  background-color: #f9f9f9;
}

td {
  color: #333 !important;
}

.sucesso {
  text-align: center;
  color: green;
  margin-top: 10px;
}

.erro {
  text-align: center;
  color: red;
  margin-top: 10px;
}

</style>
