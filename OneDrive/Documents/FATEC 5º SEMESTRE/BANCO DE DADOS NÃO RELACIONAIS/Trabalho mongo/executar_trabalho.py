import sys
sys.stdout.reconfigure(encoding="utf-8")

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from bson import ObjectId
from datetime import datetime
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["clinica_vet"]

# Limpa coleções para reexecução idempotente
for col in ["clientes", "veterinarios", "animais", "atendimentos"]:
    db[col].drop()

print("=" * 60)
print("TRABALHO MONGODB – CLÍNICA VETERINÁRIA")
print("=" * 60)

# ── CLIENTES ──────────────────────────────────────────────────
print("\n[1/4] Inserindo clientes...")
db.clientes.insert_many([
    {
        "_id": ObjectId("665000000000000000000001"),
        "nome": "Ana Paula Souza", "cpf": "123.456.789-00",
        "telefone": "(11) 98765-4321", "email": "ana.souza@email.com",
        "endereco": {"logradouro": "Rua das Flores", "numero": "142",
                     "bairro": "Jardim Primavera", "cidade": "São Paulo",
                     "estado": "SP", "cep": "01310-100"},
        "data_cadastro": datetime(2023, 3, 15)
    },
    {
        "_id": ObjectId("665000000000000000000002"),
        "nome": "Carlos Eduardo Lima", "cpf": "987.654.321-00",
        "telefone": "(11) 91234-5678", "email": "carlos.lima@email.com",
        "endereco": {"logradouro": "Av. Paulista", "numero": "900",
                     "bairro": "Bela Vista", "cidade": "São Paulo",
                     "estado": "SP", "cep": "01310-200"},
        "data_cadastro": datetime(2023, 6, 20)
    },
    {
        "_id": ObjectId("665000000000000000000003"),
        "nome": "Fernanda Rodrigues", "cpf": "111.222.333-44",
        "telefone": "(11) 97777-8888", "email": "fernanda.rodrigues@email.com",
        "endereco": {"logradouro": "Rua Oscar Freire", "numero": "55",
                     "bairro": "Jardins", "cidade": "São Paulo",
                     "estado": "SP", "cep": "01426-001"},
        "data_cadastro": datetime(2023, 8, 10)
    },
    {
        "_id": ObjectId("665000000000000000000004"),
        "nome": "Roberto Alves Santos", "cpf": "444.555.666-77",
        "telefone": "(11) 96666-5555", "email": "roberto.santos@email.com",
        "endereco": {"logradouro": "Rua Augusta", "numero": "210",
                     "bairro": "Consolação", "cidade": "São Paulo",
                     "estado": "SP", "cep": "01305-000"},
        "data_cadastro": datetime(2024, 1, 5)
    },
    {
        "_id": ObjectId("665000000000000000000005"),
        "nome": "Juliana Ferreira Costa", "cpf": "888.999.000-11",
        "telefone": "(11) 95555-4444", "email": "juliana.costa@email.com",
        "endereco": {"logradouro": "Alameda Santos", "numero": "780",
                     "bairro": "Cerqueira César", "cidade": "São Paulo",
                     "estado": "SP", "cep": "01419-001"},
        "data_cadastro": datetime(2024, 3, 22)
    },
])
print(f"  ✔ {db.clientes.count_documents({})} clientes inseridos")

# ── VETERINÁRIOS ──────────────────────────────────────────────
print("\n[2/4] Inserindo veterinários...")
db.veterinarios.insert_many([
    {
        "_id": ObjectId("665000000000000000000101"),
        "nome": "Dr. Marcelo Andrade", "crmv": "CRMV-SP 12345",
        "especialidade": "Clínica Geral",
        "telefone": "(11) 3333-1111", "email": "marcelo.andrade@clinicavet.com",
        "horarios_disponiveis": ["Segunda 08h-17h", "Quarta 08h-17h", "Sexta 08h-12h"]
    },
    {
        "_id": ObjectId("665000000000000000000102"),
        "nome": "Dra. Camila Torres", "crmv": "CRMV-SP 23456",
        "especialidade": "Dermatologia Veterinária",
        "telefone": "(11) 3333-2222", "email": "camila.torres@clinicavet.com",
        "horarios_disponiveis": ["Terça 09h-18h", "Quinta 09h-18h"]
    },
    {
        "_id": ObjectId("665000000000000000000103"),
        "nome": "Dr. Felipe Nascimento", "crmv": "CRMV-SP 34567",
        "especialidade": "Ortopedia Veterinária",
        "telefone": "(11) 3333-3333", "email": "felipe.nascimento@clinicavet.com",
        "horarios_disponiveis": ["Segunda 13h-18h", "Quarta 13h-18h", "Sexta 08h-17h"]
    },
])
print(f"  ✔ {db.veterinarios.count_documents({})} veterinários inseridos")

# ── ANIMAIS ───────────────────────────────────────────────────
print("\n[3/4] Inserindo animais...")
db.animais.insert_many([
    {
        "_id": ObjectId("665000000000000000000201"),
        "nome": "Rex", "especie": "Cão", "raca": "Pastor Alemão",
        "sexo": "Macho", "data_nascimento": datetime(2019, 5, 10),
        "peso_kg": 32.5, "id_cliente": ObjectId("665000000000000000000001"),
        "historico_vacinas": [
            {"vacina": "V10", "data_aplicacao": datetime(2024, 1, 15),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2025, 1, 15)},
            {"vacina": "Antirrábica", "data_aplicacao": datetime(2024, 2, 20),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2025, 2, 20)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000202"),
        "nome": "Bolinha", "especie": "Gato", "raca": "Persa",
        "sexo": "Fêmea", "data_nascimento": datetime(2021, 8, 22),
        "peso_kg": 4.2, "id_cliente": ObjectId("665000000000000000000001"),
        "historico_vacinas": [
            {"vacina": "Tríplice Felina", "data_aplicacao": datetime(2024, 3, 10),
             "veterinario": "Dra. Camila Torres", "proxima_dose": datetime(2025, 3, 10)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000203"),
        "nome": "Thor", "especie": "Cão", "raca": "Golden Retriever",
        "sexo": "Macho", "data_nascimento": datetime(2020, 11, 3),
        "peso_kg": 28.0, "id_cliente": ObjectId("665000000000000000000002"),
        "historico_vacinas": [
            {"vacina": "V10", "data_aplicacao": datetime(2023, 11, 20),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2024, 11, 20)},
            {"vacina": "Antirrábica", "data_aplicacao": datetime(2023, 11, 20),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2024, 11, 20)},
            {"vacina": "Gripe Canina", "data_aplicacao": datetime(2024, 5, 15),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2025, 5, 15)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000204"),
        "nome": "Mimi", "especie": "Gato", "raca": "Siamês",
        "sexo": "Fêmea", "data_nascimento": datetime(2022, 4, 17),
        "peso_kg": 3.8, "id_cliente": ObjectId("665000000000000000000002"),
        "historico_vacinas": [
            {"vacina": "Tríplice Felina", "data_aplicacao": datetime(2024, 4, 17),
             "veterinario": "Dra. Camila Torres", "proxima_dose": datetime(2025, 4, 17)},
            {"vacina": "Antirrábica", "data_aplicacao": datetime(2024, 4, 17),
             "veterinario": "Dra. Camila Torres", "proxima_dose": datetime(2025, 4, 17)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000205"),
        "nome": "Pingo", "especie": "Cão", "raca": "Poodle",
        "sexo": "Macho", "data_nascimento": datetime(2023, 1, 30),
        "peso_kg": 5.5, "id_cliente": ObjectId("665000000000000000000003"),
        "historico_vacinas": [
            {"vacina": "V8", "data_aplicacao": datetime(2024, 2, 1),
             "veterinario": "Dr. Marcelo Andrade", "proxima_dose": datetime(2025, 2, 1)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000206"),
        "nome": "Nina", "especie": "Coelho", "raca": "Mini Lop",
        "sexo": "Fêmea", "data_nascimento": datetime(2023, 6, 15),
        "peso_kg": 1.8, "id_cliente": ObjectId("665000000000000000000003"),
        "historico_vacinas": []
    },
    {
        "_id": ObjectId("665000000000000000000207"),
        "nome": "Simba", "especie": "Gato", "raca": "Maine Coon",
        "sexo": "Macho", "data_nascimento": datetime(2018, 9, 5),
        "peso_kg": 7.1, "id_cliente": ObjectId("665000000000000000000004"),
        "historico_vacinas": [
            {"vacina": "Tríplice Felina", "data_aplicacao": datetime(2024, 9, 5),
             "veterinario": "Dra. Camila Torres", "proxima_dose": datetime(2025, 9, 5)},
            {"vacina": "Antirrábica", "data_aplicacao": datetime(2024, 9, 5),
             "veterinario": "Dra. Camila Torres", "proxima_dose": datetime(2025, 9, 5)},
        ]
    },
    {
        "_id": ObjectId("665000000000000000000208"),
        "nome": "Duque", "especie": "Cão", "raca": "Rottweiler",
        "sexo": "Macho", "data_nascimento": datetime(2021, 3, 18),
        "peso_kg": 45.3, "id_cliente": ObjectId("665000000000000000000004"),
        "historico_vacinas": [
            {"vacina": "V10", "data_aplicacao": datetime(2024, 3, 18),
             "veterinario": "Dr. Felipe Nascimento", "proxima_dose": datetime(2025, 3, 18)},
            {"vacina": "Antirrábica", "data_aplicacao": datetime(2024, 3, 18),
             "veterinario": "Dr. Felipe Nascimento", "proxima_dose": datetime(2025, 3, 18)},
        ]
    },
])
print(f"  ✔ {db.animais.count_documents({})} animais inseridos")

# ── ATENDIMENTOS ──────────────────────────────────────────────
print("\n[4/4] Inserindo atendimentos...")
db.atendimentos.insert_many([
    {
        "_id": ObjectId("665000000000000000000301"),
        "data_atendimento": datetime(2024, 4, 10, 9, 0),
        "id_animal": ObjectId("665000000000000000000201"),
        "id_veterinario": ObjectId("665000000000000000000101"),
        "tipo": "consulta", "queixa_principal": "Coceira excessiva e vermelhidão na pele",
        "diagnostico": "Dermatite alérgica",
        "medicamentos_prescritos": [
            {"nome": "Prednisolona", "dosagem": "20mg", "frequencia": "1x ao dia", "duracao_dias": 7},
            {"nome": "Shampoo antialérgico", "dosagem": "uso externo", "frequencia": "3x na semana", "duracao_dias": 30},
        ],
        "observacoes": "Evitar contato com grama molhada",
        "valor_consulta": 180.00, "tem_retorno": True, "data_retorno": datetime(2024, 4, 24)
    },
    {
        "_id": ObjectId("665000000000000000000302"),
        "data_atendimento": datetime(2024, 4, 24, 10, 30),
        "id_animal": ObjectId("665000000000000000000201"),
        "id_veterinario": ObjectId("665000000000000000000101"),
        "tipo": "retorno", "queixa_principal": "Acompanhamento do tratamento de dermatite",
        "diagnostico": "Melhora significativa. Manter protocolo.",
        "medicamentos_prescritos": [],
        "observacoes": "Reduzir dose da prednisolona pela metade",
        "valor_consulta": 90.00, "tem_retorno": False
    },
    {
        "_id": ObjectId("665000000000000000000303"),
        "data_atendimento": datetime(2024, 5, 5, 14, 0),
        "id_animal": ObjectId("665000000000000000000203"),
        "id_veterinario": ObjectId("665000000000000000000101"),
        "tipo": "consulta", "queixa_principal": "Vômito frequente e falta de apetite há 2 dias",
        "diagnostico": "Gastroenterite",
        "medicamentos_prescritos": [
            {"nome": "Metronidazol", "dosagem": "250mg", "frequencia": "2x ao dia", "duracao_dias": 5},
            {"nome": "Cerenia", "dosagem": "16mg", "frequencia": "1x ao dia", "duracao_dias": 3},
        ],
        "observacoes": "Dieta branda por 5 dias",
        "valor_consulta": 180.00, "tem_retorno": False
    },
    {
        "_id": ObjectId("665000000000000000000304"),
        "data_atendimento": datetime(2024, 5, 12, 11, 0),
        "id_animal": ObjectId("665000000000000000000208"),
        "id_veterinario": ObjectId("665000000000000000000103"),
        "tipo": "consulta", "queixa_principal": "Claudicação no membro posterior esquerdo",
        "diagnostico": "Displasia coxofemoral moderada",
        "medicamentos_prescritos": [
            {"nome": "Meloxicam", "dosagem": "1mg/kg", "frequencia": "1x ao dia", "duracao_dias": 14},
            {"nome": "Condroitina + Glucosamina", "dosagem": "1 comprimido", "frequencia": "1x ao dia", "duracao_dias": 60},
        ],
        "observacoes": "Recomendado fisioterapia veterinária. Restringir exercícios intensos.",
        "valor_consulta": 280.00, "tem_retorno": True, "data_retorno": datetime(2024, 5, 26)
    },
    {
        "_id": ObjectId("665000000000000000000305"),
        "data_atendimento": datetime(2024, 6, 1, 8, 30),
        "id_animal": ObjectId("665000000000000000000202"),
        "id_veterinario": ObjectId("665000000000000000000102"),
        "tipo": "consulta", "queixa_principal": "Queda de pelo e descamação na cabeça",
        "diagnostico": "Dermatofitose (Microsporum canis)",
        "medicamentos_prescritos": [
            {"nome": "Itraconazol", "dosagem": "5mg/kg", "frequencia": "1x ao dia", "duracao_dias": 21},
            {"nome": "Shampoo antifúngico", "dosagem": "uso externo", "frequencia": "2x na semana", "duracao_dias": 30},
        ],
        "observacoes": "Isolamento do animal recomendado. Higienizar ambiente.",
        "valor_consulta": 220.00, "tem_retorno": True, "data_retorno": datetime(2024, 6, 22)
    },
    {
        "_id": ObjectId("665000000000000000000306"),
        "data_atendimento": datetime(2024, 6, 22, 15, 0),
        "id_animal": ObjectId("665000000000000000000202"),
        "id_veterinario": ObjectId("665000000000000000000102"),
        "tipo": "retorno", "queixa_principal": "Reavaliação da dermatofitose",
        "diagnostico": "Cura micológica confirmada",
        "medicamentos_prescritos": [],
        "observacoes": "Alta médica",
        "valor_consulta": 90.00, "tem_retorno": False
    },
    {
        "_id": ObjectId("665000000000000000000307"),
        "data_atendimento": datetime(2024, 7, 8, 9, 30),
        "id_animal": ObjectId("665000000000000000000205"),
        "id_veterinario": ObjectId("665000000000000000000101"),
        "tipo": "consulta", "queixa_principal": "Vacinação anual",
        "diagnostico": "Animal saudável",
        "medicamentos_prescritos": [],
        "observacoes": "Vacinação V8 aplicada. Próxima em julho/2025.",
        "valor_consulta": 120.00, "tem_retorno": False
    },
    {
        "_id": ObjectId("665000000000000000000308"),
        "data_atendimento": datetime(2024, 8, 14, 16, 0),
        "id_animal": ObjectId("665000000000000000000207"),
        "id_veterinario": ObjectId("665000000000000000000102"),
        "tipo": "emergência", "queixa_principal": "Obstrução urinária, animal com dor intensa",
        "diagnostico": "Urolitíase – cálculo uretral",
        "medicamentos_prescritos": [
            {"nome": "Prazosin", "dosagem": "0,25mg/kg", "frequencia": "2x ao dia", "duracao_dias": 10},
            {"nome": "Ração urinary", "dosagem": "conforme indicação", "frequencia": "alimentação exclusiva", "duracao_dias": 90},
        ],
        "observacoes": "Desobstrução realizada com cateterismo. Alta após 6h de observação.",
        "valor_consulta": 650.00, "tem_retorno": True, "data_retorno": datetime(2024, 8, 21)
    },
    {
        "_id": ObjectId("665000000000000000000309"),
        "data_atendimento": datetime(2024, 9, 3, 10, 0),
        "id_animal": ObjectId("665000000000000000000206"),
        "id_veterinario": ObjectId("665000000000000000000101"),
        "tipo": "consulta", "queixa_principal": "Animal letárgico e com diarreia",
        "diagnostico": "Estresse ambiental com disbiose intestinal",
        "medicamentos_prescritos": [
            {"nome": "Probiótico veterinário", "dosagem": "1 sachê", "frequencia": "1x ao dia", "duracao_dias": 14},
        ],
        "observacoes": "Enriquecer o ambiente do animal. Verificar alimentação.",
        "valor_consulta": 150.00, "tem_retorno": False
    },
    {
        "_id": ObjectId("665000000000000000000310"),
        "data_atendimento": datetime(2024, 10, 21, 13, 30),
        "id_animal": ObjectId("665000000000000000000204"),
        "id_veterinario": ObjectId("665000000000000000000102"),
        "tipo": "consulta", "queixa_principal": "Otite recorrente, coçando ouvido esquerdo",
        "diagnostico": "Otite externa bacteriana",
        "medicamentos_prescritos": [
            {"nome": "Otomax gotas", "dosagem": "4 gotas", "frequencia": "2x ao dia", "duracao_dias": 10},
        ],
        "observacoes": "Higienizar ouvidos semanalmente com solução própria.",
        "valor_consulta": 160.00, "tem_retorno": False
    },
])
print(f"  ✔ {db.atendimentos.count_documents({})} atendimentos inseridos")

# ── CONSULTAS find() ──────────────────────────────────────────
print("\n" + "=" * 60)
print("CONSULTAS find()")
print("=" * 60)

def show(label, cursor_or_list):
    docs = list(cursor_or_list) if not isinstance(cursor_or_list, list) else cursor_or_list
    print(f"\n▸ {label} ({len(docs)} doc(s)):")
    for d in docs:
        d.pop("_id", None)
        print("  ", json.dumps(d, default=str, ensure_ascii=False))

show("4.1 Todos os clientes (nome + cidade)",
     db.clientes.find({}, {"nome": 1, "endereco.cidade": 1, "_id": 0}))

show("4.2 Animais da espécie Gato",
     db.animais.find({"especie": "Gato"}, {"nome": 1, "raca": 1, "_id": 0}))

show("4.3 Animais com peso > 20 kg",
     db.animais.find({"peso_kg": {"$gt": 20}}, {"nome": 1, "peso_kg": 1, "_id": 0}))

show("4.4 Atendimentos do tipo emergência",
     db.atendimentos.find({"tipo": "emergência"}, {"tipo": 1, "diagnostico": 1, "valor_consulta": 1, "_id": 0}))

show("4.5 Atendimentos do Dr. Marcelo Andrade",
     db.atendimentos.find(
         {"id_veterinario": ObjectId("665000000000000000000101")},
         {"tipo": 1, "queixa_principal": 1, "_id": 0}))

show("4.6 Projeção – nome, espécie e raça dos animais",
     db.animais.find({}, {"nome": 1, "especie": 1, "raca": 1, "_id": 0}))

show("4.7 Animais que tomaram Antirrábica",
     db.animais.find(
         {"historico_vacinas.vacina": "Antirrábica"},
         {"nome": 1, "especie": 1, "_id": 0}))

show("4.8 Atendimentos entre jun-out/2024",
     db.atendimentos.find(
         {"data_atendimento": {"$gte": datetime(2024, 6, 1), "$lte": datetime(2024, 10, 31)}},
         {"tipo": 1, "data_atendimento": 1, "valor_consulta": 1, "_id": 0}))

show("4.9 Clientes em São Paulo/SP",
     db.clientes.find(
         {"endereco.cidade": "São Paulo", "endereco.estado": "SP"},
         {"nome": 1, "endereco.bairro": 1, "_id": 0}))

show("4.10 Atendimentos com valor > R$200 (ordenado DESC)",
     db.atendimentos.find(
         {"valor_consulta": {"$gt": 200}},
         {"tipo": 1, "valor_consulta": 1, "_id": 0}
     ).sort("valor_consulta", -1))

# ── ATUALIZAÇÕES E REMOÇÕES ───────────────────────────────────
print("\n" + "=" * 60)
print("ATUALIZAÇÕES E REMOÇÕES")
print("=" * 60)

res = db.clientes.update_one(
    {"_id": ObjectId("665000000000000000000002")},
    {"$set": {"telefone": "(11) 99999-0001"}})
print(f"\n▸ 5.1 Atualizar telefone Carlos: {res.modified_count} doc modificado")
doc = db.clientes.find_one({"_id": ObjectId("665000000000000000000002")}, {"nome": 1, "telefone": 1, "_id": 0})
print(f"  Novo valor: {doc}")

res = db.animais.update_one(
    {"_id": ObjectId("665000000000000000000208")},
    {"$set": {"peso_kg": 46.8}})
print(f"\n▸ 5.2 Atualizar peso do Duque: {res.modified_count} doc modificado")

res = db.animais.update_one(
    {"_id": ObjectId("665000000000000000000205")},
    {"$push": {"historico_vacinas": {
        "vacina": "Antirrábica",
        "data_aplicacao": datetime(2025, 2, 1),
        "veterinario": "Dr. Marcelo Andrade",
        "proxima_dose": datetime(2026, 2, 1)
    }}})
print(f"\n▸ 5.3 Adicionar Antirrábica ao Pingo ($push): {res.modified_count} doc modificado")
pingo = db.animais.find_one({"_id": ObjectId("665000000000000000000205")}, {"nome": 1, "historico_vacinas": 1, "_id": 0})
print(f"  Vacinas do Pingo: {[v['vacina'] for v in pingo['historico_vacinas']]}")

res = db.atendimentos.update_one(
    {"_id": ObjectId("665000000000000000000309")},
    {"$set": {"tem_retorno": True, "data_retorno": datetime(2024, 9, 17)}})
print(f"\n▸ 5.4 Marcar retorno do atendimento 309: {res.modified_count} doc modificado")

res = db.atendimentos.delete_one({"_id": ObjectId("665000000000000000000302")})
print(f"\n▸ 5.5 Remover atendimento 302 (retorno Rex): {res.deleted_count} doc removido")
print(f"  Total atendimentos restantes: {db.atendimentos.count_documents({})}")

# ── AGREGAÇÕES ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("AGREGAÇÕES")
print("=" * 60)

print("\n▸ 6.1 Animais por espécie:")
for r in db.animais.aggregate([
    {"$group": {"_id": "$especie", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]):
    print(f"  {r['_id']}: {r['total']}")

print("\n▸ 6.2 Valor médio por veterinário:")
for r in db.atendimentos.aggregate([
    {"$group": {"_id": "$id_veterinario", "media": {"$avg": "$valor_consulta"}, "total": {"$sum": 1}}},
    {"$lookup": {"from": "veterinarios", "localField": "_id", "foreignField": "_id", "as": "vet"}},
    {"$unwind": "$vet"},
    {"$project": {"_id": 0, "veterinario": "$vet.nome",
                  "media": {"$round": ["$media", 2]}, "total": 1}},
    {"$sort": {"media": -1}}
]):
    print(f"  {r['veterinario']}: R${r['media']:.2f} ({r['total']} atend.)")

print("\n▸ 6.3 Atendimentos por tipo:")
for r in db.atendimentos.aggregate([
    {"$group": {"_id": "$tipo", "quantidade": {"$sum": 1}, "faturamento": {"$sum": "$valor_consulta"}}},
    {"$sort": {"quantidade": -1}}
]):
    print(f"  {r['_id']}: {r['quantidade']} atend. | R${r['faturamento']:.2f}")

print("\n▸ 6.4 Faturamento mensal:")
for r in db.atendimentos.aggregate([
    {"$group": {
        "_id": {"ano": {"$year": "$data_atendimento"}, "mes": {"$month": "$data_atendimento"}},
        "faturamento": {"$sum": "$valor_consulta"}, "qtd": {"$sum": 1}
    }},
    {"$sort": {"_id.ano": 1, "_id.mes": 1}}
]):
    print(f"  {r['_id']['mes']:02d}/{r['_id']['ano']}: R${r['faturamento']:.2f} ({r['qtd']} atend.)")

print("\n▸ 6.5 Top animais por atendimentos:")
for r in db.atendimentos.aggregate([
    {"$group": {"_id": "$id_animal", "total": {"$sum": 1}, "gasto": {"$sum": "$valor_consulta"}}},
    {"$lookup": {"from": "animais", "localField": "_id", "foreignField": "_id", "as": "animal"}},
    {"$unwind": "$animal"},
    {"$project": {"_id": 0, "animal": "$animal.nome", "especie": "$animal.especie",
                  "total": 1, "gasto": 1}},
    {"$sort": {"total": -1}}
]):
    print(f"  {r['animal']} ({r['especie']}): {r['total']} atend. | R${r['gasto']:.2f}")

print("\n" + "=" * 60)
print("Banco de dados 'clinica_vet' populado e validado com sucesso!")
print("=" * 60)
client.close()
