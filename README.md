
# 📊 Extração de Dados com Sidrapy em Python

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python) ![Sidrapy](https://img.shields.io/badge/Sidrapy-Data_Extraction-orange?style=for-the-badge)

## 📋 Descrição do Projeto

Este projeto utiliza a biblioteca **Sidrapy** para extrair dados diretamente da plataforma **Sidra** do IBGE com Python, facilitando o processo de coleta e manipulação de dados para análises mais rápidas e eficazes. Com ele, você poderá acessar dados estatísticos diretamente da API do IBGE e integrá-los ao **Pandas** para análises de dados.

---

## 📦 Requisitos de Instalação

Para rodar o projeto, você precisará ter **Python 3.x** instalado. Instale as bibliotecas necessárias com:

```bash
pip install sidrapy pandas
```

---

## 🛠️ Uso

Antes de iniciar, identifique o código da tabela e variáveis que deseja extrair na [plataforma Sidra](https://sidra.ibge.gov.br/).

### Exemplo de extração de tabela

```python
import pandas as pd
import sidrapy

base = get_table(table_code="1086", 
                 territorial_level="3",
                 ibge_territorial_code="all",
                 variable="283",
                 period="all")


print(df.head())
```

### Parâmetros Principais

- **table_code**: Código da tabela no Sidra (e.g., “1086” para leite).
- **territorial_level**: Nível territorial (1 para Brasil, 3 para Estados).
- **ibge_territorial_code**: Código do IBGE para estados (e.g., “all" para selecionar todos).
- **variable**: Código da variável (e.g., “283” para quantidade de leite cru).
- **period**: Período (use “all” para todos os períodos ou um específico, como “202402” para 2º trimestre de 2024).

---

## 📈 Análise e Manipulação com Pandas

Com os dados extraídos no DataFrame, você pode realizar várias operações de análise e visualização.
Caso precise de um tutorial, acesse meu Medium, escrevi uma matéria lá.
- [Documentação Sidrapy](https://medium.com/@falkzera/extra%C3%A7%C3%A3o-de-dados-do-sidra-com-python-40fd7d3a0ff5)


---

## 🚀 Acesse o DashBoard, atualizado em tempo real

- [DashBoard](https://pesquisa-trimestral-leite.streamlit.app/)

---

## 📚 Recursos Adicionais

- [Documentação Sidrapy](https://github.com/username/sidrapy)
- [API SIDRA do IBGE](https://apisidra.ibge.gov.br/)

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para reportar problemas ou sugerir melhorias, por favor, abra uma _issue_ ou envie um _pull request_.

---

## 📝 Licença

Este projeto é distribuído sob a licença MIT.
