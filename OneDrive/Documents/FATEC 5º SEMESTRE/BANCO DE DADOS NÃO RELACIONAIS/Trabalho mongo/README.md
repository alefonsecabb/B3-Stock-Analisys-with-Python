<div align="center">

# 🐾 Clínica Veterinária — MongoDB

### Sistema de Gestão com Banco de Dados Não Relacional

[![MongoDB](https://img.shields.io/badge/MongoDB-8.3-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyMongo](https://img.shields.io/badge/PyMongo-4.17-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://pymongo.readthedocs.io/)
[![FATEC](https://img.shields.io/badge/FATEC-Ciência_de_Dados-003087?style=for-the-badge)](https://fatecsp.br/)

<br/>

> Trabalho prático da disciplina **Banco de Dados Não Relacionais**  
> Curso de **Ciência de Dados** · 5º Semestre · 2026  
> Professor: **Higor Antonio Delsoto**

</div>

---

## 👥 Equipe

| Aluno | Curso | Semestre |
|---|---|---|
| Alexandre da Fonseca | Ciência de Dados – FATEC | 5º |
| Riquelmy Henrique Silva | Ciência de Dados – FATEC | 5º |
| Carlos Eduardo Pereira de Rezende | Ciência de Dados – FATEC | 5º |

---

## 📌 Sobre o Projeto

Este trabalho implementa um **banco de dados orientado a documentos** usando **MongoDB** para gerenciar uma clínica veterinária fictícia chamada `clinica_vet`. O projeto demonstra na prática as principais decisões de modelagem NoSQL — **embedding** vs. **referencing** — com dados realistas, consultas variadas e pipelines de agregação.

O banco cobre o ciclo completo de atendimento: cadastro de clientes e seus animais, agenda de veterinários, histórico de vacinas e registro de consultas com diagnósticos e prescrições.

---

## 🗂️ Estrutura do Repositório

```
🐾 banco_nao_relacional_MongoDB/
│
├── 📄 README.md                           ← Visão geral do projeto (este arquivo)
├── 📋 trabalho_mongodb_clinica_vet.md     ← Documentação completa (schemas, queries, respostas)
├── 📑 trabalho_mongodb_clinica_vet.pdf    ← Versão PDF da documentação
├── 🐍 gerar_pdf.py                        ← Script para gerar o PDF a partir do markdown
├── 🐍 executar_trabalho.py                ← Script Python para popular e testar o banco
└── 📝 Proposta de Trabalho_Mongo.docx     ← Enunciado original da atividade
```

---

## 🏗️ Modelagem do Banco de Dados

O banco `clinica_vet` é composto por **4 coleções** com uma estratégia híbrida de embedding e referências:

```
┌─────────────────────────────────────────────────────────────────────┐
│                          clinica_vet                                │
├──────────────┬──────────────┬───────────────┬───────────────────────┤
│   clientes   │    animais   │  veterinarios │     atendimentos      │
│──────────────│──────────────│───────────────│───────────────────────│
│ _id          │ _id          │ _id           │ _id                   │
│ nome         │ nome         │ nome          │ data_atendimento      │
│ cpf          │ especie      │ crmv          │ id_animal ──────────► │
│ telefone     │ raca         │ especialidade │ id_veterinario ─────► │
│ email        │ sexo         │ telefone      │ tipo                  │
│ endereco {}  │ peso_kg      │ email         │ diagnostico           │
│   logradouro │ id_cliente ► │ horarios []   │ medicamentos []       │
│   bairro     │ historico_   │               │ valor_consulta        │
│   cidade     │   vacinas [] │               │ tem_retorno           │
│ data_cad.    │              │               │ data_retorno          │
└──────────────┴──────────────┴───────────────┴───────────────────────┘
                     ► = referência (ObjectId)
                     {} = documento embutido
                     [] = array embutido
```

### 🔗 Decisões de Modelagem

| Campo | Estratégia | Justificativa |
|---|---|---|
| `endereco` em `clientes` | 📦 **Embutido** | Sempre lido junto com o cliente; sem existência independente |
| `historico_vacinas` em `animais` | 📦 **Embutido** | Pertence ao animal, tamanho limitado e previsível |
| `medicamentos_prescritos` em `atendimentos` | 📦 **Embutido** | Específicos de cada atendimento, não reutilizados |
| `id_cliente` em `animais` | 🔗 **Referência** | Cliente existe independentemente; evita duplicação |
| `id_animal` em `atendimentos` | 🔗 **Referência** | Animal tem múltiplos atendimentos; normaliza os dados |
| `id_veterinario` em `atendimentos` | 🔗 **Referência** | Veterinário tem ciclo de vida independente |

---

## 📊 Coleções e Dados

| Coleção | Documentos | Destaques |
|---|---|---|
| 🧑‍💼 `clientes` | 5 | Endereço completo embutido; todos em São Paulo |
| 🐶 `animais` | 8 | Cães, gatos e um coelho; histórico de vacinas embutido |
| 🩺 `veterinarios` | 3 | Clínica geral, dermatologia e ortopedia |
| 📋 `atendimentos` | 10 | Consultas, retornos e emergências; com prescrições |

### 🐾 Animais cadastrados

| Nome | Espécie | Raça | Tutor |
|---|---|---|---|
| Rex | Cão | Pastor Alemão | Ana Paula Souza |
| Bolinha | Gato | Persa | Ana Paula Souza |
| Thor | Cão | Golden Retriever | Carlos Eduardo Lima |
| Mimi | Gato | Siamês | Carlos Eduardo Lima |
| Pingo | Cão | Poodle | Fernanda Rodrigues |
| Nina | Coelho | Mini Lop | Fernanda Rodrigues |
| Simba | Gato | Maine Coon | Roberto Alves Santos |
| Duque | Cão | Rottweiler | Roberto Alves Santos |

---

## 📚 Conteúdo da Documentação

O arquivo [`trabalho_mongodb_clinica_vet.md`](./trabalho_mongodb_clinica_vet.md) cobre:

### 1️⃣ Modelagem das Coleções
Schemas JSON das 4 coleções com decisões documentadas de embedding vs. referencing.

### 2️⃣ Inserção de Dados
Comandos `insertMany` com ObjectIds fixos para garantir consistência das referências entre coleções.

### 3️⃣ Consultas `find()` — 10 queries
- Filtros simples e compostos
- Projeção de campos
- Consulta em campos de documentos embutidos (`endereco.cidade`)
- Consulta em arrays embutidos (`historico_vacinas.vacina`)
- Filtros por intervalo de datas
- Ordenação por valor

### 4️⃣ Atualizações e Remoções
- `updateOne` com `$set` para campos simples
- `updateOne` com `$push` para inserir em arrays embutidos
- `deleteOne` e `deleteMany`

### 5️⃣ Agregações — 5 pipelines
| Pipeline | Operadores |
|---|---|
| Contagem de animais por espécie | `$group`, `$sort` |
| Valor médio por veterinário | `$group`, `$lookup`, `$unwind`, `$project` |
| Total de atendimentos por tipo | `$group`, `$sort` |
| Faturamento mensal | `$group` com `$year`/`$month`, `$concat` |
| Top animais com mais atendimentos | `$group`, `$lookup`, `$unwind` |

### 6️⃣ Questões Conceituais
5 respostas teóricas sobre embedding vs. referencing, integridade referencial no MongoDB e vantagens sobre bancos relacionais.

---

## 🚀 Como Executar

### Pré-requisitos

- ✅ MongoDB Server 6+ rodando em `localhost:27017`
- ✅ Python 3.10+
- ✅ PyMongo instalado

```bash
pip install pymongo
```

### ▶️ Populando e testando o banco

```bash
python executar_trabalho.py
```

O script executa de forma idempotente:
1. 🗑️ Dropa e recria as 4 coleções
2. 📥 Insere todos os documentos com ObjectIds fixos
3. 🔍 Executa e imprime todas as consultas `find()`
4. ✏️ Executa todas as atualizações e remoções
5. 📊 Executa e imprime todos os pipelines de agregação

### 🧭 Acessando via MongoDB Compass

1. Abra o **MongoDB Compass**
2. Conecte em `mongodb://localhost:27017`
3. Selecione o banco `clinica_vet`
4. Explore as coleções e rode queries na aba **Aggregations**

### 📑 Gerando o PDF da documentação

```bash
pip install markdown xhtml2pdf
python gerar_pdf.py
```

O PDF será salvo como `trabalho_mongodb_clinica_vet.pdf` na mesma pasta.

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| [MongoDB](https://www.mongodb.com/) | 8.3 | Banco de dados orientado a documentos |
| [Python](https://www.python.org/) | 3.12 | Scripts de população e geração de PDF |
| [PyMongo](https://pymongo.readthedocs.io/) | 4.17 | Driver Python para MongoDB |
| [xhtml2pdf](https://xhtml2pdf.readthedocs.io/) | — | Geração de PDF a partir de HTML/CSS |
| [Markdown](https://python-markdown.github.io/) | 3.x | Conversão de markdown para HTML |

---

## 📝 Critérios de Avaliação

| Critério | Pontuação |
|---|---|
| Modelagem das coleções | 1,0 pt |
| Inserção correta dos documentos | 1,5 pt |
| Uso de documentos embutidos | 1,0 pt |
| Uso de referências entre coleções | 1,0 pt |
| Consultas `find()` | 1,5 pt |
| Atualizações e remoções | 1,0 pt |
| Consultas `aggregate()` | 1,5 pt |
| Respostas conceituais e justificativas | 1,0 pt |
| Organização da entrega | 0,5 pt |
| **Total** | **10,0 pt** |

---

## 🤖 Declaração de Uso de IA

Os dados fictícios das quatro coleções (`clientes`, `animais`, `veterinarios` e `atendimentos`) foram gerados com auxílio do **Claude (Anthropic)**.

---

<div align="center">

Feito com ☕ e 🐾 &nbsp;·&nbsp; FATEC · Ciência de Dados · 2026

</div>
