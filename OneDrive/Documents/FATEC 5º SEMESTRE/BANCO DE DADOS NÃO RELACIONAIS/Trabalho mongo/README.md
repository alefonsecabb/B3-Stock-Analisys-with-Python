# Banco de Dados Não Relacional – MongoDB
## Sistema de Gestão de Clínica Veterinária

> Trabalho prático da disciplina **Banco de Dados Não Relacionais** – FATEC  
> Aluno: **Alexandre da Fonseca** | Curso: Ciência de Dados | 5º Semestre | 2026

---

## Sobre o Projeto

Implementação de um banco de dados orientado a documentos utilizando **MongoDB** para o gerenciamento de uma clínica veterinária fictícia. O sistema modela quatro entidades principais com uso de **documentos embutidos** e **referências**, demonstrando as melhores práticas de modelagem NoSQL.

---

## Estrutura do Repositório

```
📦 banco_não_relacional_MongoDB
├── 📄 README.md                          ← Este arquivo
├── 📄 trabalho_mongodb_clinica_vet.md    ← Documentação completa do trabalho
├── 📄 executar_trabalho.py               ← Script Python para popular e consultar o banco
└── 📄 Proposta de Trabalho_Mongo.docx    ← Enunciado original da atividade
```

---

## Banco de Dados: `clinica_vet`

### Coleções

| Coleção | Registros | Descrição |
|---|---|---|
| `clientes` | 5 | Tutores dos animais, com endereço embutido |
| `animais` | 8 | Pets, com histórico de vacinas embutido e referência ao cliente |
| `veterinarios` | 3 | Profissionais da clínica |
| `atendimentos` | 10 | Consultas, retornos e emergências, com medicamentos embutidos |

### Estratégia de Modelagem

```
clientes
  └── endereco { }            ← embedding (sempre lido junto)

animais
  ├── id_cliente → clientes   ← reference (entidade independente)
  └── historico_vacinas [ ]   ← embedding (pertence ao animal, tamanho limitado)

atendimentos
  ├── id_animal  → animais    ← reference (ciclo de vida próprio)
  ├── id_veterinario → vets   ← reference (entidade independente)
  └── medicamentos_prescritos [ ] ← embedding (específicos do atendimento)
```

---

## Conteúdo da Documentação

O arquivo [`trabalho_mongodb_clinica_vet.md`](./trabalho_mongodb_clinica_vet.md) contém:

1. **Modelagem** – schemas das 4 coleções e justificativas de embedding vs. referência
2. **Inserção de dados** – comandos `insertMany` com dados reais para todas as coleções
3. **Consultas `find()`** – 10 queries variadas (filtros, projeção, campos aninhados, arrays, ordenação, intervalo de datas)
4. **Atualizações e remoções** – `$set`, `$push` em arrays embutidos, `deleteOne`, `deleteMany`
5. **Agregações** – 5 pipelines com `$group`, `$lookup`, `$unwind`, `$project`, `$sort`
6. **Questões conceituais** – 5 respostas sobre modelagem NoSQL, embedding vs. referencing, integridade referencial

---

## Como Executar

### Pré-requisitos

- MongoDB Server 6+ rodando em `localhost:27017`
- Python 3.10+
- PyMongo instalado

```bash
pip install pymongo
```

### Populando e testando o banco

```bash
python executar_trabalho.py
```

O script:
- Dropa e recria as 4 coleções (idempotente)
- Insere todos os documentos com ObjectIds fixos
- Executa todas as consultas e imprime os resultados
- Executa todas as atualizações/remoções
- Executa todas as agregações

### Acessando via MongoDB Compass

1. Abra o **MongoDB Compass**
2. Conecte em `mongodb://localhost:27017`
3. Selecione o banco `clinica_vet`

---

## Tecnologias

![MongoDB](https://img.shields.io/badge/MongoDB-8.3-47A248?style=flat&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![PyMongo](https://img.shields.io/badge/PyMongo-4.17-47A248?style=flat)

---

## Distribuição de Pontos (10 pts)

| Critério | Peso |
|---|---|
| Modelagem das coleções | 1,0 |
| Inserção correta dos documentos | 1,5 |
| Uso de documentos embutidos | 1,0 |
| Uso de referências | 1,0 |
| Consultas `find()` | 1,5 |
| Atualizações e remoções | 1,0 |
| Consultas `aggregate()` | 1,5 |
| Respostas conceituais e justificativas | 1,0 |
| Organização da entrega | 0,5 |

---

*Disciplina ministrada na FATEC – 2026*
