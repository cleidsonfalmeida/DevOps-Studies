# Livraria Virtual - CRUD de Livros com Docker

## Visão Geral da Aplicação

Esta aplicação simula uma livraria virtual, permitindo o cadastro, edição, listagem e exclusão de livros. O sistema é composto por três componentes principais:

- **Frontend:** Desenvolvido em Vue.js
- **Backend:** Desenvolvido em FastAPI
- **Banco de Dados:** PostgreSQL

A arquitetura foi preparada para rodar em um `cluster Kubernetes`, utilizando `Helm Charts` para facilitar o deploy, a configuração e o gerenciamento dos recursos.

---

## Como Executar a Aplicação Localmente com Minikube e Helm

1. **Inicie o Minikube:**
   ```sh
   minikube start
   ```

2. **Aplique o Helm Chart:**
    - No diretório raiz do projeto, execute:
    ```sh
    helm install livraria charts/livraria
    ```

3. **Verifique se os pods e ingress estão rodando:**
    ```sh
    kubectl get pods
    kubectl get ingress
    ```

4. **Adicione o domínio k8s.local ao seu arquivo /etc/hosts: Descubra o IP do Minikube:**
    ```sh
    minikube ip
    ```
    - Adicione a seguinte linha ao seu `/etc/hosts` (substitua `<IP-DO-MINIKUBE>` pelo IP retornado acima):
    - `<IP-DO-MINIKUBE>` k8s.local

5. **Acesse a aplicação no navegador: Abra [http://k8s.local](http://k8s.local) para acessar o frontend da livraria virtual.**


6. **acessar o frontend diretamente usando o Minikube:**
    ```sh
    minikube service frontend
    ```

## Explicação Detalhada dos Arquivos Kubernetes/Helm

### Chart.yaml

Este arquivo define o Helm Chart, que é um pacote de recursos Kubernetes.

**Principais campos:**

- `apiVersion`: Versão da API do Helm Chart (ex: `v2`).
- `name`: Nome do chart (ex: `meu-app`).
- `description`: Descrição do chart.
- `type`: Tipo do chart (ex: `application`).
- `version`: Versão do chart.
- `appVersion`: Versão da aplicação empacotada.

**Exemplo de uso:**  
O Helm utiliza este arquivo para identificar o pacote, suas dependências e metadados. É obrigatório em qualquer chart.

---

### values.yaml

Arquivo de valores padrão do Helm.

**Principais campos:**

- `frontend.image.repository`: Repositório da imagem do frontend.
- `frontend.image.tag`: Tag da imagem do frontend.
- `frontend.replicas`: Número de réplicas do frontend.
- `backend.image.repository`: Repositório da imagem do backend.
- `backend.image.tag`: Tag da imagem do backend.
- `backend.replicas`: Número de réplicas do backend.
- `db.image.repository`: Repositório da imagem do banco de dados.
- `db.image.tag`: Tag da imagem do banco de dados.
- `db.storage`: Tamanho do volume persistente do banco.
- `service`: Configurações de portas dos serviços.
- `ingress`: Configurações de domínio, TLS e paths do Ingress.

**Exemplo de uso:**  
Se o `deployment-frontend.yaml` usa `{{ .Values.frontend.image.repository }}`, o valor real vem deste arquivo. Isso permite reusar o mesmo chart em diferentes ambientes apenas mudando o `values.yaml`.

---

### deployment-frontend.yaml

Cria e gerencia os pods do frontend.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (ex: `apps/v1`).
- `kind`: Tipo do recurso (`Deployment`).
- `metadata.name`: Nome do deployment.
- `spec.replicas`: Quantidade de réplicas do frontend.
- `spec.selector.matchLabels`: Seletores para identificar os pods gerenciados.
- `spec.template.metadata.labels`: Labels dos pods.
- `spec.template.spec.containers`:
  - `name`: Nome do container.
  - `image`: Imagem do container.
  - `ports`: Portas expostas pelo container.
  - `env`: Variáveis de ambiente.
  - `resources`: Limites e requisições de CPU/memória (opcional).

**Exemplo de uso:**  
Garante que sempre existam X réplicas do frontend rodando, atualizando de forma controlada quando há mudanças na imagem ou configuração.

---

### service-frontend.yaml

Expõe o frontend para outros serviços ou para o Ingress.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (`v1`).
- `kind`: Tipo do recurso (`Service`).
- `metadata.name`: Nome do service.
- `spec.selector`: Seletores para identificar os pods do frontend.
- `spec.ports`:
  - `port`: Porta exposta pelo service.
  - `targetPort`: Porta do container que recebe o tráfego.
- `spec.type`: Tipo do serviço (geralmente `ClusterIP` para uso interno).

**Exemplo de uso:**  
Permite que o Ingress ou outros pods acessem o frontend via um endereço DNS interno.

---

### deployment-backend.yaml

Gerencia os pods do backend.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (ex: `apps/v1`).
- `kind`: Tipo do recurso (`Deployment`).
- `metadata.name`: Nome do deployment.
- `spec.replicas`: Quantidade de réplicas do backend.
- `spec.selector.matchLabels`: Seletores para identificar os pods gerenciados.
- `spec.template.metadata.labels`: Labels dos pods.
- `spec.template.spec.containers`:
  - `name`: Nome do container.
  - `image`: Imagem do container.
  - `ports`: Portas expostas pelo container.
  - `env`: Variáveis de ambiente (ex: conexão com banco de dados).
  - `resources`: Limites e requisições de CPU/memória (opcional).

**Exemplo de uso:**  
Mantém o backend disponível e atualizado, com configurações específicas para acessar o banco de dados e se comunicar com o frontend.

---

### service-backend.yaml

Expõe o backend para o frontend e outros serviços.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (`v1`).
- `kind`: Tipo do recurso (`Service`).
- `metadata.name`: Nome do service.
- `spec.selector`: Seletores para identificar os pods do backend.
- `spec.ports`:
  - `port`: Porta exposta pelo service.
  - `targetPort`: Porta do container que recebe o tráfego.
- `spec.type`: Tipo do serviço (geralmente `ClusterIP`).

**Exemplo de uso:**  
Permite que o frontend envie requisições para o backend usando o nome do serviço como hostname.

---

### deployment-db.yaml

Gerencia o pod do banco de dados.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (ex: `apps/v1`).
- `kind`: Tipo do recurso (`Deployment`).
- `metadata.name`: Nome do deployment.
- `spec.replicas`: Quantidade de réplicas (geralmente 1 para banco).
- `spec.selector.matchLabels`: Seletores para identificar os pods gerenciados.
- `spec.template.metadata.labels`: Labels dos pods.
- `spec.template.spec.containers`:
  - `name`: Nome do container.
  - `image`: Imagem do banco de dados.
  - `ports`: Porta exposta pelo banco.
  - `envFrom`: Referência para secrets com variáveis sensíveis.
  - `volumeMounts`: Monta o volume persistente no container.
- `spec.template.spec.volumes`: Define o PVC a ser montado.

**Exemplo de uso:**  
Garante que o banco de dados esteja sempre disponível e que os dados persistam mesmo se o pod for reiniciado.

---

### service-db.yaml

Expõe o banco de dados para o backend.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (`v1`).
- `kind`: Tipo do recurso (`Service`).
- `metadata.name`: Nome do service.
- `spec.selector`: Seletores para identificar o pod do banco de dados.
- `spec.ports`:
  - `port`: Porta exposta pelo service (ex: `5432`).
  - `targetPort`: Porta do container do banco.
- `spec.type`: Tipo do serviço (`ClusterIP`).

**Exemplo de uso:**  
Permite que o backend acesse o banco de dados usando o nome do serviço como hostname.

---

### pvc-db.yaml

Solicita armazenamento persistente para o banco de dados.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (`v1`).
- `kind`: Tipo do recurso (`PersistentVolumeClaim`).
- `metadata.name`: Nome do PVC.
- `spec.accessModes`: Modos de acesso (ex: `ReadWriteOnce`).
- `spec.resources.requests.storage`: Quantidade de armazenamento solicitada (ex: `1Gi`).

**Exemplo de uso:**  
Garante que os dados do banco não sejam perdidos em caso de reinício ou realocação do pod.

---

### secret-db.yaml

Armazena informações sensíveis do banco de dados.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (`v1`).
- `kind`: Tipo do recurso (`Secret`).
- `metadata.name`: Nome do secret.
- `type`: Tipo do secret (ex: `Opaque`).
- `data`: Chaves e valores codificados em base64 (ex: `usuário`, `senha`).

**Exemplo de uso:**  
Evita expor credenciais em texto plano nos manifests. Os deployments referenciam este secret para obter as variáveis de ambiente sensíveis.

---

### ingress.yaml

Gerencia o acesso externo à aplicação.

**Principais campos:**

- `apiVersion`: Versão da API do recurso (ex: `networking.k8s.io/v1`).
- `kind`: Tipo do recurso (`Ingress`).
- `metadata.name`: Nome do ingress.
- `metadata.annotations`: Anotações para configurações extras (ex: TLS, redirecionamentos).
- `spec.rules`:
  - `host`: Domínio público.
  - `http.paths`: Paths e serviços de destino (frontend, backend).
- `spec.tls`: (Opcional) Configura certificados TLS para HTTPS.

**Exemplo de uso:**  
Permite acessar a aplicação via um domínio público, roteando requisições para o frontend e backend conforme o path.

---

## Resumo Visual de Relações

- **Ingress** → encaminha tráfego externo para **Service Frontend** e/ou **Service Backend**
- **Service Frontend** → expõe o **Deployment Frontend**
- **Service Backend** → expõe o **Deployment Backend**
- **Service DB** → expõe o **Deployment DB**
- **Deployment Backend** → acessa o **Service DB** usando credenciais do **Secret DB**
- **Deployment DB** → usa o **PVC DB** para persistência de dados

## Equipe

* Nome: Cleidson Almeida

## Licença

Este projeto possui licença GNU GENERAL PUBLIC LICENSE.

---

> Para mais detalhes, consulte os códigos nos diretórios `backend/`, `frontend/` e `chart/`.
