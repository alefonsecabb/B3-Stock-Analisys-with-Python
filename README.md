 Clínica Veterinária — MongoDB
Sistema de Gestão com Banco de Dados Não Relacional
MongoDB Python PyMongo

📌 Sobre o Projeto
Este trabalho implementa um banco de dados orientado a documentos usando MongoDB para gerenciar uma clínica veterinária fictícia chamada clinica_vet. O projeto demonstra na prática as principais decisões de modelagem NoSQL — embedding vs. referencing — com dados realistas, consultas variadas e pipelines de agregação.

O banco cobre o ciclo completo de atendimento: cadastro de clientes e seus animais, agenda de veterinários, histórico de vacinas e registro de consultas com diagnósticos e prescrições.


🔗 Decisões de Modelagem
Campo	Estratégia	Justificativa
endereco em clientes	📦 Embutido	Sempre lido junto com o cliente; sem existência independente
historico_vacinas em animais	📦 Embutido	Pertence ao animal, tamanho limitado e previsível
medicamentos_prescritos em atendimentos	📦 Embutido	Específicos de cada atendimento, não reutilizados
id_cliente em animais	🔗 Referência	Cliente existe independentemente; evita duplicação
id_animal em atendimentos	🔗 Referência	Animal tem múltiplos atendimentos; normaliza os dados
id_veterinario em atendimentos	🔗 Referência	Veterinário tem ciclo de vida independente
📊 Coleções e Dados
Coleção	Documentos	Destaques
🧑‍💼 clientes	5	Endereço completo embutido; todos em São Paulo
🐶 animais	8	Cães, gatos e um coelho; histórico de vacinas embutido
🩺 veterinarios	3	Clínica geral, dermatologia e ortopedia
📋 atendimentos	10	Consultas, retornos e emergências; com prescrições
🐾 Animais cadastrados
Nome	Espécie	Raça	Tutor
Rex	Cão	Pastor Alemão	Ana Paula Souza
Bolinha	Gato	Persa	Ana Paula Souza
Thor	Cão	Golden Retriever	Carlos Eduardo Lima
Mimi	Gato	Siamês	Carlos Eduardo Lima
Pingo	Cão	Poodle	Fernanda Rodrigues
Nina	Coelho	Mini Lop	Fernanda Rodrigues
Simba	Gato	Maine Coon	Roberto Alves Santos
Duque	Cão	Rottweiler	Roberto Alves Santos
📚 Conteúdo da Documentação
O arquivo trabalho_mongodb_clinica_vet.md cobre:

1️⃣ Modelagem das Coleções
Schemas JSON das 4 coleções com decisões documentadas de embedding vs. referencing.

2️⃣ Inserção de Dados
Comandos insertMany com ObjectIds fixos para garantir consistência das referências entre coleções.

3️⃣ Consultas find() — 10 queries
Filtros simples e compostos
Projeção de campos
Consulta em campos de documentos embutidos (endereco.cidade)
Consulta em arrays embutidos (historico_vacinas.vacina)
Filtros por intervalo de datas
Ordenação por valor
4️⃣ Atualizações e Remoções
updateOne com $set para campos simples
updateOne com $push para inserir em arrays embutidos
deleteOne e deleteMany
5️⃣ Agregações — 5 pipelines
Pipeline	Operadores
Contagem de animais por espécie	$group, $sort
Valor médio por veterinário	$group, $lookup, $unwind, $project
Total de atendimentos por tipo	$group, $sort
Faturamento mensal	$group com $year/$month, $concat
Top animais com mais atendimentos	$group, $lookup, $unwind
6️⃣ Questões Conceituais
5 respostas teóricas sobre embedding vs. referencing, integridade referencial no MongoDB e vantagens sobre bancos relacionais.

🚀 Como Executar
Pré-requisitos
✅ MongoDB Server 6+ rodando em localhost:27017
✅ Python 3.10+
✅ PyMongo instalado
pip install pymongo
▶️ Populando e testando o banco
python executar_trabalho.py
O script executa de forma idempotente:

🗑️ Dropa e recria as 4 coleções
📥 Insere todos os documentos com ObjectIds fixos
🔍 Executa e imprime todas as consultas find()
✏️ Executa todas as atualizações e remoções
📊 Executa e imprime todos os pipelines de agregação
🧭 Acessando via MongoDB Compass
Abra o MongoDB Compass
Conecte em mongodb://localhost:27017
Selecione o banco clinica_vet
Explore as coleções e rode queries na aba Aggregations
📑 Gerando o PDF da documentação
pip install markdown xhtml2pdf
python gerar_pdf.py
O PDF será salvo como trabalho_mongodb_clinica_vet.pdf na mesma pasta.

🛠️ Tecnologias
Tecnologia	Versão	Uso
MongoDB	8.3	Banco de dados orientado a documentos
Python	3.12	Scripts de população e geração de PDF
PyMongo	4.17	Driver Python para MongoDB
xhtml2pdf	—	Geração de PDF a partir de HTML/CSS
Markdown	3.x	Conversão de markdown para HTML
📝 Critérios de Avaliação
Critério	Pontuação
Modelagem das coleções	1,0 pt
Inserção correta dos documentos	1,5 pt
Uso de documentos embutidos	1,0 pt
Uso de referências entre coleções	1,0 pt
Consultas find()	1,5 pt
Atualizações e remoções	1,0 pt
Consultas aggregate()	1,5 pt
Respostas conceituais e justificativas	1,0 pt
Organização da entrega	0,5 pt
Total	10,0 pt
🤖 Declaração de Uso de IA
Os dados fictícios das quatro coleções (clientes, animais, veterinarios e atendimentos) foram gerados com auxílio do Claude (Anthropic).

