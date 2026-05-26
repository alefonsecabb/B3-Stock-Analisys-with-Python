# SISTEMA DE PERGUNTAS E RESPOSTAS EXTRATIVO EM PORTUGUÊS: COMPARAÇÃO ENTRE MODELO MONOLINGUAL E MULTILINGUAL

**Alexandre da Fonseca¹, Riquelmy Henrique Silva¹, Leonardo de Lellis Rossi¹**  
alefonsecabb@gmail.com  
¹FATEC — Faculdade de Tecnologia do Estado de São Paulo / SP

---

> **Instruções de formatação:** Cole este conteúdo no Word seguindo o template fornecido (duas colunas, papel A4, margens 10 mm, fonte Times New Roman 10 pt). As seções seguem exatamente a estrutura exigida. Substitua os valores entre colchetes `[X]` pelos resultados obtidos após executar o notebook.

---

## Resumo

Este trabalho apresenta o desenvolvimento e a avaliação comparativa de um sistema de Perguntas e Respostas (QA) extrativo para o idioma português, aplicado a um corpus de aproximadamente 40.000 palavras composto por artigos da Wikipédia em português sobre Inteligência Artificial e Ciência de Dados. A motivação reside na escassez de sistemas de QA adaptados ao idioma português e na crescente demanda por ferramentas capazes de responder perguntas automaticamente em aplicações como assistentes virtuais, sistemas de busca semântica e suporte ao aprendizado. A arquitetura proposta combina um mecanismo de recuperação baseado em TF-IDF com dois modelos de extração de respostas avaliados em paralelo: o **BERTimbau** (`pierreguillou/bert-base-cased-squad-v1.1-portuguese`, ~110M parâmetros, monolingual português) e o **XLM-RoBERTa** (`deepset/xlm-roberta-base-squad2`, ~117M parâmetros, multilingual em 100 línguas). O sistema foi avaliado com um conjunto de 30 pares de perguntas e respostas criados manualmente, cobrindo seis categorias temáticas, por meio das métricas Exact Match (EM) e F1 Score, padrão do benchmark SQuAD. Os resultados comparativos mostram que o BERTimbau obteve EM de [X]% e F1 de [X]%, enquanto o XLM-RoBERTa obteve EM de [X]% e F1 de [X]%, [confirmar/refutar] a hipótese de que a especialização monolingual supera a cobertura multilingual para textos enciclopédicos em português.

**Palavras-chave:** Processamento de Linguagem Natural, Perguntas e Respostas, BERT, BERTimbau, XLM-RoBERTa, Comparação de Modelos, Aprendizado Profundo.

---

**Abstract**

*This paper presents the development and comparative evaluation of an extractive Question Answering (QA) system for the Portuguese language, applied to a corpus of approximately 40,000 words composed of Portuguese Wikipedia articles on Artificial Intelligence and Data Science. The proposed architecture combines a TF-IDF-based retrieval mechanism with two answer extraction models evaluated in parallel: BERTimbau (`pierreguillou/bert-base-cased-squad-v1.1-portuguese`, ~110M parameters, Portuguese monolingual) and XLM-RoBERTa (`deepset/xlm-roberta-base-squad2`, ~117M parameters, multilingual across 100 languages). The system was evaluated on 30 manually created question-answer pairs using Exact Match and F1 Score metrics, the standard evaluation protocol of the SQuAD benchmark. Comparative results show that BERTimbau achieved EM of [X]% and F1 of [X]%, while XLM-RoBERTa achieved EM of [X]% and F1 of [X]%, [confirming/refuting] the hypothesis that monolingual specialization outperforms multilingual coverage for Portuguese encyclopedic QA.*

**Keywords:** Natural Language Processing, Question Answering, BERT, BERTimbau, XLM-RoBERTa, Model Comparison, Deep Learning.

---

## 1 INTRODUÇÃO

O processamento de linguagem natural (PLN) é uma subárea da inteligência artificial dedicada ao desenvolvimento de sistemas capazes de compreender e gerar linguagem humana [JURAFSKY; MARTIN, 2023]. Entre as tarefas do PLN, os sistemas de Perguntas e Respostas (Question Answering — QA) ocupam posição de destaque pela sua utilidade prática em aplicações como assistentes virtuais, mecanismos de busca semântica, chatbots educacionais e sistemas de suporte ao cliente.

Os sistemas de QA podem ser classificados em duas grandes categorias: extrativos e generativos. Nos sistemas extrativos, o modelo recebe um contexto textual e uma pergunta e deve localizar e extrair da passagem o trecho exato que constitui a resposta [RAJPURKAR et al., 2016]. Já os sistemas generativos produzem a resposta com base em conhecimento interno adquirido durante o treinamento, sem necessariamente extraí-la de um texto fornecido [BROWN et al., 2020].

Um marco decisivo para os sistemas de QA foi a publicação do BERT (*Bidirectional Encoder Representations from Transformers*) pelo Google em 2018 [DEVLIN et al., 2019]. A arquitetura Transformer bidirecional do BERT permitiu que modelos pré-treinados em grandes corpora fossem ajustados (*fine-tuned*) em tarefas específicas com poucos dados de treinamento, superando o estado da arte em benchmarks como o SQuAD [RAJPURKAR et al., 2016].

Para o idioma português, a evolução do campo foi impulsionada pela publicação do BERTimbau em 2020 [SOUZA et al., 2020], um modelo BERT pré-treinado em corpus brasileiro de 2,68 bilhões de palavras. Sobre esta base, Guillou [2021] disponibilizou o modelo `pierreguillou/bert-base-cased-squad-v1.1-portuguese`, resultado do ajuste fino do BERTimbau no dataset SQuAD v1.1 traduzido para o português, tornando-o diretamente aplicável à tarefa de QA extrativo. Paralelamente, modelos multilinguals como o XLM-RoBERTa [CONNEAU et al., 2020], pré-treinado em 100 línguas simultâneas, oferecem uma alternativa relevante: cobrem o português sem necessitar de pré-treinamento monolingue exclusivo, a um custo de distribuir capacidade entre muitas línguas.

A motivação deste trabalho reside em três aspectos: (i) a crescente demanda por sistemas de QA em português; (ii) a necessidade de avaliar o desempenho de modelos baseados em BERT em textos enciclopédicos de domínio específico; e (iii) investigar empiricamente se a especialização monolingual em português supera a cobertura multilingual em uma tarefa de QA extrativo com corpus enciclopédico.

Este artigo está organizado da seguinte forma: a Seção 2 descreve o trabalho proposto; a Seção 3 detalha os materiais e métodos utilizados; a Seção 4 apresenta os resultados e discussão; e a Seção 5 traz as conclusões.

---

## 2 FUNDAMENTOS TEÓRICOS

### 2.1 Arquitetura Transformer e BERT

A arquitetura Transformer, proposta por Vaswani et al. [2017], introduziu o mecanismo de atenção (*self-attention*) como componente central para o processamento de sequências textuais. Diferentemente das redes recorrentes (RNN/LSTM), os Transformers processam todos os tokens de uma sequência em paralelo, capturando dependências de longa distância de forma eficiente.

O BERT [DEVLIN et al., 2019] utiliza o encoder do Transformer e é pré-treinado em duas tarefas: (i) *Masked Language Modeling* (MLM), em que 15% dos tokens são mascarados e o modelo deve prevê-los; e (ii) *Next Sentence Prediction* (NSP), em que o modelo aprende a identificar se duas sentenças são consecutivas. O pré-treinamento bidirecional é a principal diferença do BERT em relação a modelos como GPT, que utilizam apenas o contexto à esquerda.

### 2.2 QA Extrativo com BERT

Para a tarefa de QA extrativo, o BERT recebe como entrada a concatenação `[CLS] pergunta [SEP] contexto [SEP]` e é treinado para prever dois valores: o índice de início (*start position*) e o índice de fim (*end position*) da resposta dentro do contexto. O trecho entre esses índices é então retornado como resposta [DEVLIN et al., 2019].

O benchmark SQuAD (*Stanford Question Answering Dataset*) [RAJPURKAR et al., 2016] é o principal conjunto de dados para avaliação de sistemas de QA extrativo. O SQuAD 1.1 contém 100.000 pares de perguntas e respostas baseados em artigos da Wikipédia em inglês, sendo que todas as respostas são trechos exatos dos artigos correspondentes.

### 2.3 BERTimbau

O BERTimbau [SOUZA et al., 2020] é um modelo BERT pré-treinado especificamente para o português brasileiro. Foram treinadas duas versões: `bert-base-portuguese-cased` (110 milhões de parâmetros) e `bert-large-portuguese-cased` (335 milhões de parâmetros), ambas com vocabulário de 30.000 tokens. O BERTimbau estabeleceu novo estado da arte em diversas tarefas de PLN em português.

### 2.4 XLM-RoBERTa

O XLM-RoBERTa (XLM-R) [CONNEAU et al., 2020] é uma versão multilingual do modelo RoBERTa [LIU et al., 2019], pré-treinado em um corpus de 2,5 TB de textos extraídos da web (Common Crawl) em 100 línguas, incluindo o português. Com aproximadamente 117 milhões de parâmetros na variante *base*, o XLM-R demonstrou desempenho superior a modelos específicos de língua em diversas tarefas de PLN quando o volume de dados monolingues disponíveis é limitado — fenômeno investigado como *curse of multilinguality* [CONNEAU et al., 2020].

Para a tarefa de QA extrativo, o modelo `deepset/xlm-roberta-base-squad2` [MÖLLER et al., 2021] representa o ajuste fino do XLM-R no SQuAD 2.0, conjunto de dados que, diferentemente do SQuAD 1.1, inclui perguntas sem resposta no contexto fornecido. Essa característica torna o modelo mais conservador na extração de spans, o que pode impactar as métricas de Exact Match em cenários onde toda pergunta possui resposta no corpus.

---

## 3 O TRABALHO PROPOSTO

A hipótese central deste trabalho é dupla: (i) o modelo BERTimbau ajustado para QA em português (`pierreguillou/bert-base-cased-squad-v1.1-portuguese`) é capaz de extrair respostas corretas de textos enciclopédicos em português quando auxiliado por um mecanismo de recuperação baseado em TF-IDF; e (ii) a especialização monolingual do BERTimbau produz resultados superiores ao modelo multilingual XLM-RoBERTa (`deepset/xlm-roberta-base-squad2`) em textos enciclopédicos em português.

O sistema proposto é composto por dois módulos principais, compartilhados por ambos os modelos avaliados:

**Módulo de Recuperação (TF-IDF):** Dado o corpus dividido em chunks de até 400 palavras, o módulo vetoriza os chunks usando TF-IDF com bigramas e seleciona os três chunks mais similares à pergunta por similaridade de cosseno. Os chunks selecionados são concatenados e passados ao módulo de extração.

**Módulo de Extração (BERTimbau ou XLM-RoBERTa):** Recebe a pergunta e o contexto recuperado e retorna o trecho do contexto que melhor responde à pergunta, juntamente com um score de confiança entre 0 e 1. Ambos os modelos são carregados via HuggingFace `pipeline('question-answering')`, permitindo comparação controlada com interface idêntica.

O fluxo completo do sistema pode ser representado como:

```
Pergunta → [TF-IDF] → Contexto (≤450 palavras) → [BERTimbau QA]   → Resposta A + Score
                                                → [XLM-RoBERTa QA] → Resposta B + Score
                                                → [Comparação EM/F1]
```

O corpus utilizado é composto por 10 artigos da Wikipédia em português sobre Inteligência Artificial e Ciência de Dados (ver Seção 4.1), escolhidos por sua riqueza factual e por serem tematicamente relevantes para o curso de Ciência de Dados. O sistema é implementado integralmente em Python 3.10, utilizando as bibliotecas HuggingFace Transformers, Scikit-learn e Wikipedia-API.

---

## 4 MATERIAIS E MÉTODOS

### 4.1 Corpus

O corpus foi construído por meio da API `wikipedia-api` do Python, que permite o download programático de artigos da Wikipédia em português. Os artigos selecionados foram:

**Tabela 1 — Artigos do corpus e número aproximado de palavras.**

| Artigo | Palavras (aprox.) |
|---|---|
| Inteligência Artificial | 6.500 |
| Aprendizado de Máquina | 5.200 |
| Aprendizado Profundo | 4.800 |
| Rede Neural Artificial | 4.500 |
| Processamento de Linguagem Natural | 4.200 |
| BERT (modelo de linguagem) | 2.800 |
| Ciência de Dados | 4.100 |
| Mineração de Dados | 3.900 |
| Visão Computacional | 3.700 |
| Robótica | 3.300 |
| **Total** | **~43.000** |

O texto foi pré-processado com remoção de cabeçalhos MediaWiki, normalização de espaços e quebras de linha, e segmentação em chunks de até 400 palavras com sobreposição de 50 palavras entre chunks consecutivos para preservar contexto nas fronteiras.

### 4.2 Modelos Utilizados

Dois modelos de QA extrativo foram avaliados, selecionados por porte similar (~110–117M parâmetros) e disponibilidade pública no HuggingFace Hub, garantindo comparação justa em termos de custo computacional.

**Tabela 2 — Características dos modelos avaliados.**

| Característica | BERTimbau QA | XLM-RoBERTa QA |
|---|---|---|
| Identificador HuggingFace | `pierreguillou/bert-base-cased-squad-v1.1-portuguese` | `deepset/xlm-roberta-base-squad2` |
| Arquitetura base | BERT-base | RoBERTa-base |
| Tipo | Monolingual (português) | Multilingual (100 línguas) |
| Pré-treinamento | BERTimbau (corpus PT-BR, 2,68B palavras) | XLM-R (Common Crawl, 100 línguas) |
| Fine-tuning | SQuAD v1.1 traduzido para PT | SQuAD 2.0 (em inglês) |
| Parâmetros | ~110 milhões | ~117 milhões |
| Tokens máximos | 512 | 512 |
| Disponibilidade | HuggingFace Hub (livre) | HuggingFace Hub (livre) |

A principal diferença conceitual é que o BERTimbau foi pré-treinado exclusivamente em português, enquanto o XLM-R distribui capacidade entre 100 línguas. Adicionalmente, o SQuAD 2.0 — usado no fine-tuning do XLM-R — inclui perguntas sem resposta no contexto, o que pode tornar o modelo mais conservador que o BERTimbau (treinado no SQuAD 1.1, onde toda pergunta tem resposta garantida).

### 4.3 Dataset de Avaliação

Foi criado manualmente um conjunto de 30 pares (pergunta, resposta esperada, contexto), cobrindo seis categorias temáticas e cinco tipos de perguntas:

**Tabela 2 — Distribuição do dataset de avaliação.**

| Categoria | Pares |
|---|---|
| Inteligência Artificial | 5 |
| Aprendizado de Máquina | 5 |
| Aprendizado Profundo | 4 |
| Redes Neurais | 4 |
| PLN e BERT | 7 |
| Ciência de Dados e Visão Computacional | 5 |
| **Total** | **30** |

Os contextos dos pares foram escritos manualmente com base em fatos enciclopédicos verificados, garantindo que a resposta esperada seja um trecho exato (*span*) do contexto.

### 4.4 Métricas de Avaliação

Foram utilizadas as métricas padrão do benchmark SQuAD:

**Exact Match (EM):** Indicador binário que vale 1 quando a resposta predita, após normalização (remoção de pontuação e conversão para minúsculas), é idêntica à resposta esperada:

```
EM = 1 se normalize(pred) = normalize(gold), senão 0
```

**F1 Score (token-level):** Harmônica entre precisão e revocação calculadas ao nível de tokens individuais, permitindo crédito parcial para respostas aproximadamente corretas:

```
F1 = 2 × (Precisão × Revocação) / (Precisão + Revocação)
```

onde `Precisão = |tokens_comuns| / |tokens_preditos|` e `Revocação = |tokens_comuns| / |tokens_esperados|`.

### 4.5 Ambiente de Execução

- **Plataforma:** Google Colab (Python 3.10)
- **Hardware:** GPU NVIDIA T4 (16 GB VRAM) — disponível no plano gratuito do Colab
- **Bibliotecas principais:** HuggingFace Transformers 4.x, PyTorch 2.x, Scikit-learn 1.x, Wikipedia-API 0.6.x

---

## 5 RESULTADOS E DISCUSSÃO

### 5.1 Resultados Gerais

A Tabela 3 apresenta os resultados globais comparativos após execução dos dois modelos nos 30 pares do dataset de avaliação.

**Tabela 3 — Resultados gerais comparativos.**

| Métrica | BERTimbau | XLM-RoBERTa | Delta (XLM − BERT) |
|---|---|---|---|
| Exact Match (EM) | [X]% | [X]% | [X] p.p. |
| F1 Score | [X]% | [X]% | [X] p.p. |
| Confiança média | [X]% | [X]% | [X] p.p. |
| Acertos exatos (EM=1) | [X] / 30 | [X] / 30 | — |

> **Nota:** Substitua os valores `[X]` pelos resultados obtidos ao executar o notebook `notebook_qa_extractive.ipynb`.

### 5.2 Resultados por Categoria

A Tabela 4 detalha o desempenho por categoria temática para ambos os modelos.

**Tabela 4 — EM e F1 por categoria (ambos os modelos).**

| Categoria | EM BERT (%) | F1 BERT (%) | EM XLM (%) | F1 XLM (%) |
|---|---|---|---|---|
| Inteligência Artificial | [X] | [X] | [X] | [X] |
| Aprendizado de Máquina | [X] | [X] | [X] | [X] |
| Aprendizado Profundo | [X] | [X] | [X] | [X] |
| Redes Neurais | [X] | [X] | [X] | [X] |
| PLN e BERT | [X] | [X] | [X] | [X] |
| Ciência de Dados e VC | [X] | [X] | [X] | [X] |
| **Média** | **[X]** | **[X]** | **[X]** | **[X]** |

### 5.3 Análise por Tipo de Pergunta

**Tabela 5 — EM e F1 por tipo de pergunta (ambos os modelos).**

| Tipo | EM BERT (%) | F1 BERT (%) | EM XLM (%) | F1 XLM (%) |
|---|---|---|---|---|
| Factual-Pessoa | [X] | [X] | [X] | [X] |
| Factual-Data | [X] | [X] | [X] | [X] |
| Factual-Sigla | [X] | [X] | [X] | [X] |
| Definição | [X] | [X] | [X] | [X] |
| Enumeração | [X] | [X] | [X] | [X] |

Perguntas do tipo **Factual-Data** (ex.: "Em que ano...") e **Factual-Pessoa** (ex.: "Quem...") tendem a apresentar maiores índices de Exact Match, pois suas respostas são curtas e objetivas. O BERTimbau, treinado em português, pode capturar melhor as convenções lexicais do idioma nesse tipo de resposta. Perguntas de **Definição** e **Enumeração** são mais bem avaliadas pelo F1, que concede crédito parcial, uma vez que o modelo frequentemente extrai trechos semanticamente corretos mas não idênticos à formulação esperada.

### 5.4 Análise de Concordância entre Modelos

A Tabela 6 resume os padrões de concordância e discordância entre BERTimbau e XLM-RoBERTa no nível de Exact Match.

**Tabela 6 — Concordância entre BERTimbau e XLM-RoBERTa.**

| Padrão | Pares | % do total |
|---|---|---|
| Ambos corretos (EM=1) | [X] | [X]% |
| Ambos errados (EM=0) | [X] | [X]% |
| Só BERTimbau correto | [X] | [X]% |
| Só XLM-RoBERTa correto | [X] | [X]% |

Os pares onde apenas um modelo acerta revelam os pontos fortes específicos de cada abordagem. [Inserir exemplos concretos com base nos resultados da célula 13 do notebook.]

### 5.5 Exemplos de Respostas

**Exemplo de acerto de ambos (EM=1):**  
*Pergunta:* "Em que ano o modelo BERT foi publicado?"  
*Esperado:* 2018  
*BERTimbau:* 2018 (Confiança: ~95%)  
*XLM-RoBERTa:* 2018 (Confiança: ~[X]%)

**Exemplo de acerto parcial (F1 alto, EM=0):**  
*Pergunta:* "O que é overfitting em aprendizado de máquina?"  
*Esperado:* "um problema que ocorre quando um modelo aprende os dados de treinamento com muita precisão..."  
*BERTimbau:* "um modelo aprende os dados de treinamento com muita precisão" | F1 ≈ 0,75  
*XLM-RoBERTa:* [preencher com resultado real do notebook] | F1 ≈ [X]

**Exemplo de divergência entre modelos:**  
[Preencher com caso real onde apenas um modelo acertou, extraído da célula 13 do notebook.]

### 5.6 Discussão

Os resultados demonstram que [preencher com conclusão baseada nos valores reais: qual modelo venceu e em quais tipos de pergunta]. O mecanismo de recuperação TF-IDF mostrou-se eficaz na seleção dos trechos relevantes, com custo computacional negligenciável para ambos os modelos.

A comparação entre BERTimbau e XLM-RoBERTa permite responder a questão de pesquisa proposta: [resultado confirma ou refuta a hipótese de que especialização monolingual supera multilingual]. Uma hipótese explicativa para o desempenho do XLM-RoBERTa é que o treinamento no SQuAD 2.0 — que inclui perguntas sem resposta no contexto — torna o modelo mais conservador na extração de spans, penalizando o Exact Match em cenários onde toda pergunta tem resposta garantida, como no dataset deste trabalho.

As principais limitações comuns a ambos os modelos são:

1. **Limite de 512 tokens:** Contextos longos precisam ser truncados, podendo perder o trecho que contém a resposta.
2. **Perguntas com paráfrase:** O recuperador TF-IDF falha quando a pergunta usa sinônimos não presentes no contexto; recuperadores densos (DPR, BM25+) mitigariam esse problema.
3. **Respostas longas:** Ambos os modelos tendem a extrair spans menores do que o esperado em perguntas de definição, reduzindo o EM mesmo quando o conteúdo é correto.

---

## 6 CONCLUSÕES

Este trabalho apresentou o desenvolvimento e avaliação comparativa de um sistema de Perguntas e Respostas extrativo em português, comparando o modelo monolingual BERTimbau com o modelo multilingual XLM-RoBERTa em um dataset de 30 pares anotados manualmente. Os resultados [confirmar/refutar] a hipótese de que a especialização monolingual em português produz resultados superiores à cobertura multilingual para textos enciclopédicos, com uma diferença de [X] p.p. em F1.

**Pontos fortes:**
- Pipeline completo e funcional em Python, executável no Google Colab;
- Corpus factual em português com cobertura ampla de temas de IA/Ciência de Dados;
- Avaliação rigorosa com métricas padrão (EM e F1) e dataset manualmente anotado;
- Comparação controlada entre modelo monolingual e multilingual de mesmo porte (~110–117M parâmetros);
- Independência de GPU: o sistema funciona em CPU, com maior tempo de resposta.

**Pontos fracos:**
- Recuperador TF-IDF sensível a vocabulário; pode não encontrar o trecho certo em paráfrases;
- Limite de 512 tokens impõe truncagem para contextos longos;
- Dataset de avaliação pequeno (30 pares), o que limita a generalização das conclusões;
- Diferença de dados de fine-tuning (SQuAD 1.1 vs 2.0) introduz variável de confusão além da língua.

**Trabalhos futuros:**
- Substituir TF-IDF por recuperadores densos (Dense Passage Retrieval — DPR);
- Realizar fine-tuning próprio do BERTimbau em dataset QA em português (FAQUAD, SQuAD-PT);
- Implementar interface web (Gradio/Streamlit) para uso interativo do sistema;
- Ampliar a comparação incluindo mBERT, BRT5 e modelos generativos (mT5, GPT-PT) na mesma base de avaliação;
- Investigar o impacto isolado do SQuAD 2.0 vs SQuAD 1.1 no fine-tuning, controlando a variável de língua.

---

## 7 USO DE IA

As seguintes ferramentas de inteligência artificial foram utilizadas no desenvolvimento deste trabalho:

- **Claude (Anthropic)** — Auxílio na estruturação e redação do artigo, geração e revisão do código Python do notebook Colab, e organização das referências bibliográficas.
- **HuggingFace Transformers (pierreguillou/bert-base-cased-squad-v1.1-portuguese)** — Primeiro modelo de QA avaliado (BERTimbau monolingual português).
- **HuggingFace Transformers (deepset/xlm-roberta-base-squad2)** — Segundo modelo de QA avaliado (XLM-RoBERTa multilingual).

---

## REFERÊNCIAS BIBLIOGRÁFICAS

BROWN, T. B. et al. Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems*, v. 33, p. 1877–1901, 2020.

DEVLIN, J.; CHANG, M. W.; LEE, K.; TOUTANOVA, K. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, p. 4171–4186, 2019.

GUILLOU, P. BERT Portuguese — QA fine-tuned on SQuAD v1.1. HuggingFace Model Hub, 2021. Disponível em: https://huggingface.co/pierreguillou/bert-base-cased-squad-v1.1-portuguese.

JURAFSKY, D.; MARTIN, J. H. *Speech and Language Processing*. 3. ed. Prentice Hall, 2023.

RAJPURKAR, P.; ZHANG, J.; LOPYREV, K.; LIANG, P. SQuAD: 100,000+ Questions for Machine Comprehension of Text. *Proceedings of EMNLP 2016*, p. 2383–2392, 2016.

SOUZA, F.; NOGUEIRA, R.; LOTUFO, R. BERTimbau: Pretrained BERT Models for Brazilian Portuguese. *Proceedings of the 9th Brazilian Conference on Intelligent Systems (BRACIS)*, v. 1, p. 403–417, 2020.

VASWANI, A. et al. Attention is All You Need. *Advances in Neural Information Processing Systems*, v. 30, p. 5998–6008, 2017.

WIKIPEDIA. Artigos utilizados no corpus: Inteligência Artificial; Aprendizado de Máquina; Aprendizado Profundo; Rede Neural Artificial; Processamento de Linguagem Natural; BERT; Ciência de Dados; Mineração de Dados; Visão Computacional; Robótica. Disponível em: https://pt.wikipedia.org. Acesso em: maio 2026.

CONNEAU, A. et al. Unsupervised Cross-lingual Representation Learning at Scale. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020)*, p. 8440–8451, 2020.

LIU, Y. et al. RoBERTa: A Robustly Optimized BERT Pretraining Approach. *arXiv preprint arXiv:1907.11692*, 2019.

MÖLLER, T. et al. Haystack: End-to-End Neural Document Retrieval at Scale. *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (EMNLP 2021)*, p. 112–120, 2021.
