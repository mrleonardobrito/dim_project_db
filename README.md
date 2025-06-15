# 🚀 Projeto Dimensional de um Data Warehouse - Global Retail

## 🧠 Descrição do Projeto

Este projeto consiste na modelagem e implementação de um **Data Warehouse** para uma rede varejista fictícia chamada **Global Retail**. O objetivo é permitir análises detalhadas e agregadas sobre vendas, fornecendo insights estratégicos que apoiem a tomada de decisão.

## 🎯 Objetivo

Criar um modelo dimensional eficiente que permita:

- Analisar valor total das vendas e quantidade de produtos vendidos.
- Realizar análises por período (diário, mensal, trimestral e anual).
- Calcular margens de lucro por **produto**, **categoria** e **cliente**.
- Facilitar consultas rápidas e intuitivas através de um modelo otimizado.

---

## 🏗️ Modelo Dimensional

### 🔸 Tipo de Esquema

➝ **Esquema Estrela (Star Schema)**

**Justificativa:**

- Alta performance para consultas analíticas.
- Estrutura simples e intuitiva.
- Redução da quantidade de joins em consultas.
- Melhor experiência para analistas e usuários de BI.

---

## 🗺️ Estrutura do Modelo

### 🔥 Tabela Fato

- **Fato_Vendas:**  
  Contém as métricas de vendas, como quantidade, valor da venda, custo e margem de lucro.

### 🌟 Tabelas Dimensão

- **Dim_Produto:** Produto e categoria.
- **Dim_Cliente:** Dados do cliente (nome, idade, gênero, localidade).
- **Dim_Loja:** Informações da loja (nome, cidade, estado).
- **Dim_Tempo:** Datas para análise temporal (ano, mês, dia, trimestre).

---

## 💾 Dados Gerados

- Utilização de **Python + Faker** para gerar dados sintéticos realistas.
- Base simulada com:
  - 100 produtos
  - 200 clientes
  - 10 lojas
  - 60 datas
  - 5.000 registros de vendas na tabela fato

---

## 🔍 Consultas Realizadas

- **Total de vendas por categoria de produto.**
- **Total de vendas por loja.**
- **Total de vendas por cliente (top 5).**
- As consultas são executadas com medição do tempo, demonstrando a eficiência do modelo dimensional.

---

## ⏱️ Desempenho - Tempos de Execução

| Query                           | Tempo (s) aproximado |
| ------------------------------- | -------------------- |
| Vendas por Categoria de Produto | ~0.004               |
| Vendas por Loja                 | ~0.0039              |
| Vendas por Cliente (Top 5)      | ~0.0052              |

_Os tempos podem variar conforme a máquina, volume de dados e cache do banco._

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- SQLAlchemy
- Faker
- PostgreSQL
- Docker + Docker Compose

---

## 🚀 Como Executar o Projeto

### 🔧 Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3 instalado.

### 🔥 Passo a passo

1. **Clone este repositório:**

```bash
git clone https://github.com/seu-usuario/datawarehouse-global-retail.git
cd datawarehouse-global-retail
```
