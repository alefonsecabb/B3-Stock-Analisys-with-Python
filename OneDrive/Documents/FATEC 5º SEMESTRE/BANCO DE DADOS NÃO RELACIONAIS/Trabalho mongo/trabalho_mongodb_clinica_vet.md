# Trabalho Prático – Banco de Dados Não Relacional com MongoDB
## Sistema de Gestão de Clínica Veterinária

**Alunos:** Alexandre da Fonseca / Riquelmy Henrique Silva / Carlos Eduardo Pereira de Rezende 
**Curso:** Ciência de Dados – FATEC  
**Disciplina:** Banco de Dados Não Relacionais 
**Professor:** Higor Antonio Delsoto  

## 1. Introdução

Este trabalho implementa um banco de dados orientado a documentos utilizando MongoDB para o gerenciamento de uma clínica veterinária. O sistema armazena informações sobre clientes, animais, veterinários e atendimentos realizados.

O banco de dados nomeado `clinica_vet` e contém quatro coleções principais: `clientes`, `animais`, `veterinarios` e `atendimentos`.

Para usar o banco, execute no `mongosh`:

```js
use clinica_vet
```

---

## 2. Modelagem das Coleções

### 2.1 Decisões de Modelagem

O MongoDB permite dois padrões principais para relacionamentos: **documentos embutidos (embedding)** e **referências (referencing)**. A escolha entre eles impacta diretamente o desempenho e a consistência dos dados.

| Dado | Estratégia | Justificativa |
|---|---|---|
| `endereco` em `clientes` | **Embutido** | O endereço é sempre lido junto com o cliente, não tem existência própria e não é compartilhado com outros documentos. |
| `historico_vacinas` em `animais` | **Embutido** | As vacinas pertencem ao animal; são sempre consultadas junto com ele. O número de vacinas por animal é limitado e previsível. |
| `medicamentos_prescritos` em `atendimentos` | **Embutido** | São específicos de cada atendimento, não reutilizados em outros contextos. |
| `id_cliente` em `animais` | **Referência** | Um cliente existe independentemente de seus animais e pode ser consultado separadamente. Evita duplicação dos dados do tutor. |
| `id_animal` em `atendimentos` | **Referência** | Um animal pode ter múltiplos atendimentos. Referenciar evita replicar todo o documento do animal em cada consulta. |
| `id_veterinario` em `atendimentos` | **Referência** | O veterinário é uma entidade independente com ciclo de vida próprio (pode ser desligado, ter especialidade alterada, etc.). |

### 2.2 Schema das Coleções

#### Coleção `clientes`
```json
{
  "_id": "ObjectId",
  "nome": "String",
  "cpf": "String",
  "telefone": "String",
  "email": "String",
  "endereco": {
    "logradouro": "String",
    "numero": "String",
    "bairro": "String",
    "cidade": "String",
    "estado": "String",
    "cep": "String"
  },
  "data_cadastro": "ISODate"
}
```

#### Coleção `animais`
```json
{
  "_id": "ObjectId",
  "nome": "String",
  "especie": "String",
  "raca": "String",
  "sexo": "String",
  "data_nascimento": "ISODate",
  "peso_kg": "Number",
  "id_cliente": "ObjectId (ref: clientes)",
  "historico_vacinas": [
    {
      "vacina": "String",
      "data_aplicacao": "ISODate",
      "veterinario": "String",
      "proxima_dose": "ISODate"
    }
  ]
}
```

#### Coleção `veterinarios`
```json
{
  "_id": "ObjectId",
  "nome": "String",
  "crmv": "String",
  "especialidade": "String",
  "telefone": "String",
  "email": "String",
  "horarios_disponiveis": ["String"]
}
```

#### Coleção `atendimentos`
```json
{
  "_id": "ObjectId",
  "data_atendimento": "ISODate",
  "id_animal": "ObjectId (ref: animais)",
  "id_veterinario": "ObjectId (ref: veterinarios)",
  "tipo": "String",
  "queixa_principal": "String",
  "diagnostico": "String",
  "medicamentos_prescritos": [
    {
      "nome": "String",
      "dosagem": "String",
      "frequencia": "String",
      "duracao_dias": "Number"
    }
  ],
  "observacoes": "String",
  "valor_consulta": "Number",
  "tem_retorno": "Boolean",
  "data_retorno": "ISODate"
}
```

---

## 3. Inserção de Dados

> **Nota:** Os ObjectIds abaixo são fixos para que as referências entre coleções funcionem  

### 3.1 Coleção `clientes`

```js
db.clientes.insertMany([
  {
    _id: ObjectId("665000000000000000000001"),
    nome: "Ana Paula Souza",
    cpf: "123.456.789-00",
    telefone: "(11) 98765-4321",
    email: "ana.souza@email.com",
    endereco: {
      logradouro: "Rua das Flores",
      numero: "142",
      bairro: "Jardim Primavera",
      cidade: "São Paulo",
      estado: "SP",
      cep: "01310-100"
    },
    data_cadastro: ISODate("2023-03-15")
  },
  {
    _id: ObjectId("665000000000000000000002"),
    nome: "Carlos Eduardo Lima",
    cpf: "987.654.321-00",
    telefone: "(11) 91234-5678",
    email: "carlos.lima@email.com",
    endereco: {
      logradouro: "Av. Paulista",
      numero: "900",
      bairro: "Bela Vista",
      cidade: "São Paulo",
      estado: "SP",
      cep: "01310-200"
    },
    data_cadastro: ISODate("2023-06-20")
  },
  {
    _id: ObjectId("665000000000000000000003"),
    nome: "Fernanda Rodrigues",
    cpf: "111.222.333-44",
    telefone: "(11) 97777-8888",
    email: "fernanda.rodrigues@email.com",
    endereco: {
      logradouro: "Rua Oscar Freire",
      numero: "55",
      bairro: "Jardins",
      cidade: "São Paulo",
      estado: "SP",
      cep: "01426-001"
    },
    data_cadastro: ISODate("2023-08-10")
  },
  {
    _id: ObjectId("665000000000000000000004"),
    nome: "Roberto Alves Santos",
    cpf: "444.555.666-77",
    telefone: "(11) 96666-5555",
    email: "roberto.santos@email.com",
    endereco: {
      logradouro: "Rua Augusta",
      numero: "210",
      bairro: "Consolação",
      cidade: "São Paulo",
      estado: "SP",
      cep: "01305-000"
    },
    data_cadastro: ISODate("2024-01-05")
  },
  {
    _id: ObjectId("665000000000000000000005"),
    nome: "Juliana Ferreira Costa",
    cpf: "888.999.000-11",
    telefone: "(11) 95555-4444",
    email: "juliana.costa@email.com",
    endereco: {
      logradouro: "Alameda Santos",
      numero: "780",
      bairro: "Cerqueira César",
      cidade: "São Paulo",
      estado: "SP",
      cep: "01419-001"
    },
    data_cadastro: ISODate("2024-03-22")
  }
])
```

### 3.2 Coleção `veterinarios`

```js
db.veterinarios.insertMany([
  {
    _id: ObjectId("665000000000000000000101"),
    nome: "Dr. Marcelo Andrade",
    crmv: "CRMV-SP 12345",
    especialidade: "Clínica Geral",
    telefone: "(11) 3333-1111",
    email: "marcelo.andrade@clinicavet.com",
    horarios_disponiveis: ["Segunda 08h-17h", "Quarta 08h-17h", "Sexta 08h-12h"]
  },
  {
    _id: ObjectId("665000000000000000000102"),
    nome: "Dra. Camila Torres",
    crmv: "CRMV-SP 23456",
    especialidade: "Dermatologia Veterinária",
    telefone: "(11) 3333-2222",
    email: "camila.torres@clinicavet.com",
    horarios_disponiveis: ["Terça 09h-18h", "Quinta 09h-18h"]
  },
  {
    _id: ObjectId("665000000000000000000103"),
    nome: "Dr. Felipe Nascimento",
    crmv: "CRMV-SP 34567",
    especialidade: "Ortopedia Veterinária",
    telefone: "(11) 3333-3333",
    email: "felipe.nascimento@clinicavet.com",
    horarios_disponiveis: ["Segunda 13h-18h", "Quarta 13h-18h", "Sexta 08h-17h"]
  }
])
```

### 3.3 Coleção `animais`

```js
db.animais.insertMany([
  {
    _id: ObjectId("665000000000000000000201"),
    nome: "Rex",
    especie: "Cão",
    raca: "Pastor Alemão",
    sexo: "Macho",
    data_nascimento: ISODate("2019-05-10"),
    peso_kg: 32.5,
    id_cliente: ObjectId("665000000000000000000001"),
    historico_vacinas: [
      {
        vacina: "V10",
        data_aplicacao: ISODate("2024-01-15"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2025-01-15")
      },
      {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2024-02-20"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2025-02-20")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000202"),
    nome: "Bolinha",
    especie: "Gato",
    raca: "Persa",
    sexo: "Fêmea",
    data_nascimento: ISODate("2021-08-22"),
    peso_kg: 4.2,
    id_cliente: ObjectId("665000000000000000000001"),
    historico_vacinas: [
      {
        vacina: "Tríplice Felina",
        data_aplicacao: ISODate("2024-03-10"),
        veterinario: "Dra. Camila Torres",
        proxima_dose: ISODate("2025-03-10")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000203"),
    nome: "Thor",
    especie: "Cão",
    raca: "Golden Retriever",
    sexo: "Macho",
    data_nascimento: ISODate("2020-11-03"),
    peso_kg: 28.0,
    id_cliente: ObjectId("665000000000000000000002"),
    historico_vacinas: [
      {
        vacina: "V10",
        data_aplicacao: ISODate("2023-11-20"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2024-11-20")
      },
      {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2023-11-20"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2024-11-20")
      },
      {
        vacina: "Gripe Canina",
        data_aplicacao: ISODate("2024-05-15"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2025-05-15")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000204"),
    nome: "Mimi",
    especie: "Gato",
    raca: "Siamês",
    sexo: "Fêmea",
    data_nascimento: ISODate("2022-04-17"),
    peso_kg: 3.8,
    id_cliente: ObjectId("665000000000000000000002"),
    historico_vacinas: [
      {
        vacina: "Tríplice Felina",
        data_aplicacao: ISODate("2024-04-17"),
        veterinario: "Dra. Camila Torres",
        proxima_dose: ISODate("2025-04-17")
      },
      {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2024-04-17"),
        veterinario: "Dra. Camila Torres",
        proxima_dose: ISODate("2025-04-17")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000205"),
    nome: "Pingo",
    especie: "Cão",
    raca: "Poodle",
    sexo: "Macho",
    data_nascimento: ISODate("2023-01-30"),
    peso_kg: 5.5,
    id_cliente: ObjectId("665000000000000000000003"),
    historico_vacinas: [
      {
        vacina: "V8",
        data_aplicacao: ISODate("2024-02-01"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2025-02-01")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000206"),
    nome: "Nina",
    especie: "Coelho",
    raca: "Mini Lop",
    sexo: "Fêmea",
    data_nascimento: ISODate("2023-06-15"),
    peso_kg: 1.8,
    id_cliente: ObjectId("665000000000000000000003"),
    historico_vacinas: []
  },
  {
    _id: ObjectId("665000000000000000000207"),
    nome: "Simba",
    especie: "Gato",
    raca: "Maine Coon",
    sexo: "Macho",
    data_nascimento: ISODate("2018-09-05"),
    peso_kg: 7.1,
    id_cliente: ObjectId("665000000000000000000004"),
    historico_vacinas: [
      {
        vacina: "Tríplice Felina",
        data_aplicacao: ISODate("2024-09-05"),
        veterinario: "Dra. Camila Torres",
        proxima_dose: ISODate("2025-09-05")
      },
      {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2024-09-05"),
        veterinario: "Dra. Camila Torres",
        proxima_dose: ISODate("2025-09-05")
      }
    ]
  },
  {
    _id: ObjectId("665000000000000000000208"),
    nome: "Duque",
    especie: "Cão",
    raca: "Rottweiler",
    sexo: "Macho",
    data_nascimento: ISODate("2021-03-18"),
    peso_kg: 45.3,
    id_cliente: ObjectId("665000000000000000000004"),
    historico_vacinas: [
      {
        vacina: "V10",
        data_aplicacao: ISODate("2024-03-18"),
        veterinario: "Dr. Felipe Nascimento",
        proxima_dose: ISODate("2025-03-18")
      },
      {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2024-03-18"),
        veterinario: "Dr. Felipe Nascimento",
        proxima_dose: ISODate("2025-03-18")
      }
    ]
  }
])
```

### 3.4 Coleção `atendimentos`

```js
db.atendimentos.insertMany([
  {
    _id: ObjectId("665000000000000000000301"),
    data_atendimento: ISODate("2024-04-10T09:00:00"),
    id_animal: ObjectId("665000000000000000000201"),
    id_veterinario: ObjectId("665000000000000000000101"),
    tipo: "consulta",
    queixa_principal: "Coceira excessiva e vermelhidão na pele",
    diagnostico: "Dermatite alérgica",
    medicamentos_prescritos: [
      { nome: "Prednisolona", dosagem: "20mg", frequencia: "1x ao dia", duracao_dias: 7 },
      { nome: "Shampoo antialérgico", dosagem: "uso externo", frequencia: "3x na semana", duracao_dias: 30 }
    ],
    observacoes: "Evitar contato com grama molhada",
    valor_consulta: 180.00,
    tem_retorno: true,
    data_retorno: ISODate("2024-04-24")
  },
  {
    _id: ObjectId("665000000000000000000302"),
    data_atendimento: ISODate("2024-04-24T10:30:00"),
    id_animal: ObjectId("665000000000000000000201"),
    id_veterinario: ObjectId("665000000000000000000101"),
    tipo: "retorno",
    queixa_principal: "Acompanhamento do tratamento de dermatite",
    diagnostico: "Melhora significativa. Manter protocolo.",
    medicamentos_prescritos: [],
    observacoes: "Reduzir dose da prednisolona pela metade",
    valor_consulta: 90.00,
    tem_retorno: false
  },
  {
    _id: ObjectId("665000000000000000000303"),
    data_atendimento: ISODate("2024-05-05T14:00:00"),
    id_animal: ObjectId("665000000000000000000203"),
    id_veterinario: ObjectId("665000000000000000000101"),
    tipo: "consulta",
    queixa_principal: "Vômito frequente e falta de apetite há 2 dias",
    diagnostico: "Gastroenterite",
    medicamentos_prescritos: [
      { nome: "Metronidazol", dosagem: "250mg", frequencia: "2x ao dia", duracao_dias: 5 },
      { nome: "Cerenia", dosagem: "16mg", frequencia: "1x ao dia", duracao_dias: 3 }
    ],
    observacoes: "Dieta branda por 5 dias",
    valor_consulta: 180.00,
    tem_retorno: false
  },
  {
    _id: ObjectId("665000000000000000000304"),
    data_atendimento: ISODate("2024-05-12T11:00:00"),
    id_animal: ObjectId("665000000000000000000208"),
    id_veterinario: ObjectId("665000000000000000000103"),
    tipo: "consulta",
    queixa_principal: "Claudicação no membro posterior esquerdo",
    diagnostico: "Displasia coxofemoral moderada",
    medicamentos_prescritos: [
      { nome: "Meloxicam", dosagem: "1mg/kg", frequencia: "1x ao dia", duracao_dias: 14 },
      { nome: "Condroitina + Glucosamina", dosagem: "1 comprimido", frequencia: "1x ao dia", duracao_dias: 60 }
    ],
    observacoes: "Recomendado fisioterapia veterinária. Restringir exercícios intensos.",
    valor_consulta: 280.00,
    tem_retorno: true,
    data_retorno: ISODate("2024-05-26")
  },
  {
    _id: ObjectId("665000000000000000000305"),
    data_atendimento: ISODate("2024-06-01T08:30:00"),
    id_animal: ObjectId("665000000000000000000202"),
    id_veterinario: ObjectId("665000000000000000000102"),
    tipo: "consulta",
    queixa_principal: "Queda de pelo e descamação na cabeça",
    diagnostico: "Dermatofitose (Microsporum canis)",
    medicamentos_prescritos: [
      { nome: "Itraconazol", dosagem: "5mg/kg", frequencia: "1x ao dia", duracao_dias: 21 },
      { nome: "Shampoo antifúngico", dosagem: "uso externo", frequencia: "2x na semana", duracao_dias: 30 }
    ],
    observacoes: "Isolamento do animal recomendado. Higienizar ambiente.",
    valor_consulta: 220.00,
    tem_retorno: true,
    data_retorno: ISODate("2024-06-22")
  },
  {
    _id: ObjectId("665000000000000000000306"),
    data_atendimento: ISODate("2024-06-22T15:00:00"),
    id_animal: ObjectId("665000000000000000000202"),
    id_veterinario: ObjectId("665000000000000000000102"),
    tipo: "retorno",
    queixa_principal: "Reavaliação da dermatofitose",
    diagnostico: "Cura micológica confirmada",
    medicamentos_prescritos: [],
    observacoes: "Alta médica",
    valor_consulta: 90.00,
    tem_retorno: false
  },
  {
    _id: ObjectId("665000000000000000000307"),
    data_atendimento: ISODate("2024-07-08T09:30:00"),
    id_animal: ObjectId("665000000000000000000205"),
    id_veterinario: ObjectId("665000000000000000000101"),
    tipo: "consulta",
    queixa_principal: "Vacinação anual",
    diagnostico: "Animal saudável",
    medicamentos_prescritos: [],
    observacoes: "Vacinação V8 aplicada. Próxima em julho/2025.",
    valor_consulta: 120.00,
    tem_retorno: false
  },
  {
    _id: ObjectId("665000000000000000000308"),
    data_atendimento: ISODate("2024-08-14T16:00:00"),
    id_animal: ObjectId("665000000000000000000207"),
    id_veterinario: ObjectId("665000000000000000000102"),
    tipo: "emergência",
    queixa_principal: "Obstrução urinária, animal com dor intensa",
    diagnostico: "Urolitíase – cálculo uretral",
    medicamentos_prescritos: [
      { nome: "Prazosin", dosagem: "0,25mg/kg", frequencia: "2x ao dia", duracao_dias: 10 },
      { nome: "Ração urinary", dosagem: "conforme indicação", frequencia: "alimentação exclusiva", duracao_dias: 90 }
    ],
    observacoes: "Desobstrução realizada com cateterismo. Alta após 6h de observação.",
    valor_consulta: 650.00,
    tem_retorno: true,
    data_retorno: ISODate("2024-08-21")
  },
  {
    _id: ObjectId("665000000000000000000309"),
    data_atendimento: ISODate("2024-09-03T10:00:00"),
    id_animal: ObjectId("665000000000000000000206"),
    id_veterinario: ObjectId("665000000000000000000101"),
    tipo: "consulta",
    queixa_principal: "Animal letárgico e com diarreia",
    diagnostico: "Estresse ambiental com disbiose intestinal",
    medicamentos_prescritos: [
      { nome: "Probiótico veterinário", dosagem: "1 sachê", frequencia: "1x ao dia", duracao_dias: 14 }
    ],
    observacoes: "Enriquecer o ambiente do animal. Verificar alimentação.",
    valor_consulta: 150.00,
    tem_retorno: false
  },
  {
    _id: ObjectId("665000000000000000000310"),
    data_atendimento: ISODate("2024-10-21T13:30:00"),
    id_animal: ObjectId("665000000000000000000204"),
    id_veterinario: ObjectId("665000000000000000000102"),
    tipo: "consulta",
    queixa_principal: "Otite recorrente, coçando ouvido esquerdo",
    diagnostico: "Otite externa bacteriana",
    medicamentos_prescritos: [
      { nome: "Otomax gotas", dosagem: "4 gotas", frequencia: "2x ao dia", duracao_dias: 10 }
    ],
    observacoes: "Higienizar ouvidos semanalmente com solução própria.",
    valor_consulta: 160.00,
    tem_retorno: false
  }
])
```

---

## 4. Consultas `find()`

### 4.1 Listar todos os clientes

```js
db.clientes.find()
```

**Resultado esperado:** retorna os 5 documentos da coleção `clientes` com todos os campos.

---

### 4.2 Listar todos os animais da espécie "Gato"

```js
db.animais.find({ especie: "Gato" })
```

**Resultado esperado:** Bolinha, Mimi, Simba (3 documentos).

---

### 4.3 Animais com peso acima de 20 kg

```js
db.animais.find({ peso_kg: { $gt: 20 } })
```

**Resultado esperado:** Rex (32,5 kg), Thor (28 kg), Duque (45,3 kg).

---

### 4.4 Atendimentos do tipo "emergência"

```js
db.atendimentos.find({ tipo: "emergência" })
```

**Resultado esperado:** atendimento do Simba em 14/08/2024 (obstrução urinária).

---

### 4.5 Atendimentos realizados pelo Dr. Marcelo Andrade

```js
db.atendimentos.find({
  id_veterinario: ObjectId("665000000000000000000101")
})
```

**Resultado esperado:** atendimentos 301, 302, 303, 307 e 309 (5 documentos).

---

### 4.6 Projeção – listar apenas nome, espécie e raça dos animais

```js
db.animais.find(
  {},
  { nome: 1, especie: 1, raca: 1, _id: 0 }
)
```

**Resultado esperado:**
```json
{ "nome": "Rex", "especie": "Cão", "raca": "Pastor Alemão" }
{ "nome": "Bolinha", "especie": "Gato", "raca": "Persa" }
{ "nome": "Thor", "especie": "Cão", "raca": "Golden Retriever" }
...
```

---

### 4.7 Animais que tomaram a vacina "Antirrábica" (campo em array embutido)

```js
db.animais.find({
  "historico_vacinas.vacina": "Antirrábica"
})
```

**Resultado esperado:** Rex, Thor, Mimi, Simba, Duque (5 documentos).

---

### 4.8 Atendimentos realizados entre junho e outubro de 2024

```js
db.atendimentos.find({
  data_atendimento: {
    $gte: ISODate("2024-06-01"),
    $lte: ISODate("2024-10-31")
  }
})
```

**Resultado esperado:** atendimentos 305, 306, 307, 308, 309 e 310 (6 documentos).

---

### 4.9 Clientes da cidade de São Paulo, estado SP (campo embutido)

```js
db.clientes.find({
  "endereco.cidade": "São Paulo",
  "endereco.estado": "SP"
})
```

**Resultado esperado:** todos os 5 clientes.

---

### 4.10 Atendimentos com valor acima de R$ 200,00, ordenados do maior para o menor

```js
db.atendimentos.find(
  { valor_consulta: { $gt: 200 } },
  { tipo: 1, valor_consulta: 1, id_animal: 1 }
).sort({ valor_consulta: -1 })
```

**Resultado esperado:** Simba/emergência (R$650), Duque/ortopedia (R$280), Bolinha/dermatologia (R$220).

---

## 5. Atualizações e Remoções

### 5.1 Atualizar o telefone do cliente Carlos Eduardo Lima

```js
db.clientes.updateOne(
  { _id: ObjectId("665000000000000000000002") },
  { $set: { telefone: "(11) 99999-0001" } }
)
```

**Verificação:**
```js
db.clientes.findOne(
  { _id: ObjectId("665000000000000000000002") },
  { nome: 1, telefone: 1 }
)
// Resultado: { nome: "Carlos Eduardo Lima", telefone: "(11) 99999-0001" }
```

---

### 5.2 Atualizar o peso do animal Duque

```js
db.animais.updateOne(
  { _id: ObjectId("665000000000000000000208") },
  { $set: { peso_kg: 46.8 } }
)
```

---

### 5.3 Adicionar nova vacina ao histórico do animal Pingo (`$push`)

```js
db.animais.updateOne(
  { _id: ObjectId("665000000000000000000205") },
  {
    $push: {
      historico_vacinas: {
        vacina: "Antirrábica",
        data_aplicacao: ISODate("2025-02-01"),
        veterinario: "Dr. Marcelo Andrade",
        proxima_dose: ISODate("2026-02-01")
      }
    }
  }
)
```

---

### 5.4 Marcar atendimento 309 com retorno agendado

```js
db.atendimentos.updateOne(
  { _id: ObjectId("665000000000000000000309") },
  {
    $set: {
      tem_retorno: true,
      data_retorno: ISODate("2024-09-17")
    }
  }
)
```

---

### 5.5 Remover o atendimento de retorno do Simba (ID 306 era do Bolinha; removemos o de número 302)

```js
db.atendimentos.deleteOne({
  _id: ObjectId("665000000000000000000302")
})
```

**Verificação:**
```js
db.atendimentos.countDocuments()
// Resultado: 9
```

---

### 5.6 Remover todos os atendimentos do tipo "retorno" (remoção múltipla)

> **Atenção:** Exemplo demonstrativo. Não execute se quiser manter os dados para poder fazer as agregações depois.

```js
db.atendimentos.deleteMany({ tipo: "retorno" })
```

---

## 6. Agregações (`aggregate`)

### 6.1 Contagem de animais por espécie

```js
db.animais.aggregate([
  {
    $group: {
      _id: "$especie",
      total: { $sum: 1 }
    }
  },
  {
    $sort: { total: -1 }
  }
])
```

**Resultado esperado:**
```json
{ "_id": "Cão", "total": 4 }
{ "_id": "Gato", "total": 3 }
{ "_id": "Coelho", "total": 1 }
```

---

### 6.2 Valor médio de consulta por veterinário

```js
db.atendimentos.aggregate([
  {
    $group: {
      _id: "$id_veterinario",
      media_valor: { $avg: "$valor_consulta" },
      total_atendimentos: { $sum: 1 }
    }
  },
  {
    $lookup: {
      from: "veterinarios",
      localField: "_id",
      foreignField: "_id",
      as: "veterinario"
    }
  },
  {
    $unwind: "$veterinario"
  },
  {
    $project: {
      _id: 0,
      veterinario: "$veterinario.nome",
      media_valor: { $round: ["$media_valor", 2] },
      total_atendimentos: 1
    }
  },
  {
    $sort: { media_valor: -1 }
  }
])
```

**Resultado esperado:**
```json
{ "veterinario": "Dra. Camila Torres",    "media_valor": 280.00, "total_atendimentos": 4 }
{ "veterinario": "Dr. Felipe Nascimento", "media_valor": 280.00, "total_atendimentos": 1 }
{ "veterinario": "Dr. Marcelo Andrade",   "media_valor": 144.00, "total_atendimentos": 5 }
```

---

### 6.3 Total de atendimentos por tipo

```js
db.atendimentos.aggregate([
  {
    $group: {
      _id: "$tipo",
      quantidade: { $sum: 1 },
      faturamento_total: { $sum: "$valor_consulta" }
    }
  },
  {
    $sort: { quantidade: -1 }
  }
])
```

**Resultado esperado:**
```json
{ "_id": "consulta",    "quantidade": 7, "faturamento_total": 1340.00 }
{ "_id": "retorno",     "quantidade": 2, "faturamento_total":  180.00 }
{ "_id": "emergência",  "quantidade": 1, "faturamento_total":  650.00 }
```

---

### 6.4 Faturamento total por mês/ano

```js
db.atendimentos.aggregate([
  {
    $group: {
      _id: {
        ano: { $year: "$data_atendimento" },
        mes: { $month: "$data_atendimento" }
      },
      faturamento: { $sum: "$valor_consulta" },
      quantidade_atendimentos: { $sum: 1 }
    }
  },
  {
    $sort: { "_id.ano": 1, "_id.mes": 1 }
  },
  {
    $project: {
      _id: 0,
      periodo: {
        $concat: [
          { $toString: "$_id.mes" }, "/", { $toString: "$_id.ano" }
        ]
      },
      faturamento: 1,
      quantidade_atendimentos: 1
    }
  }
])
```

**Resultado esperado:**
```json
{ "periodo": "4/2024",  "faturamento": 450.00, "quantidade_atendimentos": 3 }
{ "periodo": "5/2024",  "faturamento": 460.00, "quantidade_atendimentos": 2 }
{ "periodo": "6/2024",  "faturamento": 310.00, "quantidade_atendimentos": 2 }
{ "periodo": "7/2024",  "faturamento": 120.00, "quantidade_atendimentos": 1 }
{ "periodo": "8/2024",  "faturamento": 800.00, "quantidade_atendimentos": 2 }
{ "periodo": "10/2024", "faturamento": 160.00, "quantidade_atendimentos": 1 }
```

---

### 6.5 Top animais com mais atendimentos

```js
db.atendimentos.aggregate([
  {
    $group: {
      _id: "$id_animal",
      total_atendimentos: { $sum: 1 },
      gasto_total: { $sum: "$valor_consulta" }
    }
  },
  {
    $lookup: {
      from: "animais",
      localField: "_id",
      foreignField: "_id",
      as: "animal"
    }
  },
  {
    $unwind: "$animal"
  },
  {
    $project: {
      _id: 0,
      animal: "$animal.nome",
      especie: "$animal.especie",
      total_atendimentos: 1,
      gasto_total: 1
    }
  },
  {
    $sort: { total_atendimentos: -1 }
  }
])
```

**Resultado esperado:**
```json
{ "animal": "Bolinha", "especie": "Gato", "total_atendimentos": 2, "gasto_total": 310.00 }
{ "animal": "Rex",     "especie": "Cão",  "total_atendimentos": 2, "gasto_total": 270.00 }
{ "animal": "Simba",   "especie": "Gato", "total_atendimentos": 1, "gasto_total": 650.00 }
...
```

---

## 7. Questões Conceituais sobre Modelagem

### Q1 – Qual a diferença entre embedding e referencing no MongoDB? Quando usar cada um?

**Embedding (documentos embutidos)** significa armazenar dados relacionados dentro do próprio documento. **Referencing (referências)** significa armazenar apenas o `_id` do documento relacionado em outra coleção, similar a uma chave estrangeira.

**Use embedding quando:**
- Os dados relacionados são sempre lidos juntos (alta coesão de acesso).
- O subdocumento não possui existência ou consulta independente.
- O tamanho do subdocumento é previsível e limitado (evitar ultrapassar o limite de 16 MB por documento).

**Use referencing quando:**
- Os dados relacionados são entidades independentes com ciclo de vida próprio.
- O mesmo dado é reutilizado em vários outros documentos (evitar duplicação).
- O tamanho do array pode crescer indefinidamente (ex.: todos os atendimentos de um animal).

---

### Q2 – Por que o histórico de vacinas foi embutido em `animais` e não em uma coleção separada?

O histórico de vacinas é uma informação inerente ao animal, é quase sempre consultado junto com os dados do animal (ex.: "quais vacinas o Rex tomou?"). Como o número de vacinas por animal é limitado e previsível (em média 3 a 6 por ano), o risco de o documento crescer além do limite é baixo. Criar uma coleção separada (`vacinas`) exigiria um `$lookup` a cada consulta, adicionando complexidade e reduzindo a performance sem benefício real neste contexto.

---

### Q3 – Por que `id_animal` e `id_veterinario` são referências em `atendimentos`?

Porque ambas as entidades têm existência, identidade e ciclo de vida independentes da consulta:

- Um animal existe antes do primeiro atendimento e continuará existindo depois.
- Um veterinário pode ser desligado, ter sua especialidade alterada ou ser consultado separadamente de seus atendimentos.
- Um animal pode ter dezenas de atendimentos ao longo dos anos; embutir o documento completo do animal em cada atendimento causaria enorme duplicação e inconsistência (se o peso for atualizado, seria preciso atualizar todos os atendimentos).

Usar referências mantém os dados normalizados, consistentes e fáceis de atualizar.

---

### Q4 – O MongoDB garante integridade referencial automaticamente?

**Não.** Diferentemente de bancos relacionais, o MongoDB **não possui chave estrangeira com constraint automático**. Se um animal for deletado, os atendimentos que o referenciam continuarão existindo com um `id_animal` que não aponta mais para nenhum documento válido (referência "quebrada").

A integridade referencial é responsabilidade da **aplicação**. Boas práticas incluem:
- Verificar existência antes de inserir referências.
- Usar operações em cascata no código da aplicação (ex.: ao deletar um cliente, deletar também seus animais e atendimentos).
- Utilizar o operador `$lookup` com validação para detectar referências inválidas.

---

### Q5 – Quais foram as vantagens de usar MongoDB para este sistema em vez de um banco relacional?

| Aspecto | MongoDB | Banco Relacional |
|---|---|---|
| Esquema flexível | Cada animal pode ter número diferente de vacinas sem alterar a estrutura | Schema fixo exigiria tabela separada e JOIN |
| Documentos aninhados | Endereço e vacinas ficam dentro do mesmo documento | Seriam tabelas separadas |
| Leitura com um acesso | Um `find` traz o animal com todo o histórico | Exigiria JOIN entre 2+ tabelas |
| Escalabilidade horizontal | Sharding nativo | Mais complexo |
| Desvantagem | Sem integridade referencial automática | Garantias de integridade e transações ACID |

Para um sistema de clínica com dados variáveis por espécie/raça e forte relação de pertencimento (vacinas pertencem ao animal), o MongoDB oferece maior naturalidade de modelagem e performance de leitura.

---

## 8. Conclusão

O banco de dados `clinica_vet` foi modelado com foco na eficiência de leitura e na naturalidade dos relacionamentos entre entidades veterinárias. A combinação de **documentos embutidos** (endereço, vacinas, medicamentos) com **referências** (cliente→animal, animal→atendimento, veterinário→atendimento) reflete as melhores práticas do MongoDB: embutir o que sempre é lido junto, referenciar o que tem existência independente.

O sistema suporta todas as operações CRUD, consultas simples e complexas com projeção e filtros em campos aninhados, além de pipelines de agregação para relatórios gerenciais.


# Declaração do uso de IA
# Foi utilizado o Claude para geração dos dados fictícios das quatro coleções principais: `clientes`, `animais`, `veterinarios` e `atendimentos`.