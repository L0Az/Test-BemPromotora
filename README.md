# Test-BemPromotora

Como os arquivos são pesados, coloquei em um Zip no Drive https://drive.google.com/file/d/15MGc9PlqVYb_ciHADBxj7VXuYUTskkE8/view?usp=sharing

Também é possível observar o projeto no link https://test-bempromotora.diogosansonove.website/

# OBS: O projeto irá demorar para rodar na primeira vez, pois estará inserindo os arquivos csv em um arquivo .DB

# Projeto montado com Python na versão 3.10

Para instalar as bibliotecas é recomendada a criação de um venv

```
python -m venv venv
```

Após a criação é preciso acessar

# Windows
```
venv\Scripts\activate

ou

.\venv\Scripts\activate
```

# Mac/Linux
```
source venv/bin/activate
```

Separei um arquivo para ser rodado e instalar todas as bibliotecas

```
pip install -r requirements.txt
```

Após a instalação saia do venv

```
deactivate
```

# Inicie o Projeto com o comando

```
flask run
```

O projeto será aberto em na url http://127.0.0.1:5000/.

# Métodos

# O que foi feito?

Adicionei dados de 6 anos (2018 a 2023) comparando dados e demonstrando a evolução dos mesmos.
(OBS: Foram ignoradas as organizações "sigilosas")

### Cidades mais visitadas

Uma simples contagem de quantas vezes a cidade aparece em rows.

### Custos por organização

Um Inner Join entre as tabelas viagem e pagamento, é possível observar uma diminuição nos gastos do Fundo Nacional de Segurança Pública durante o passar dos anos, trazendo um equilíbrio maior para as organizações.

### Viagens mais caras por mês

Uma comparação simples utilizando o campo de "Período - Data de início" e a soma de "Valor Diárias, Valor passagens, Valor outros gastos".
Em 2018 haviam mais viagens no fim e começo do ano, durante o passar de anos é possível ver uma troca para meio e fim de ano serem escolhas mais populares.

### Cidades com maior número de diárias

Uma soma simples de quantas diárias a cidade tem na tabela "trecho".
As diárias mantiveram seus picos de viagens durante o fim do ano, mas é possível observar que ao passar dos anos as capitais são as mais escolhidas.

### Organizações com maior custo de passagens

Um Inner Join com as tabelas pagamento e viagem, comparando somente o preço que as organizações que mais gastaram com passagens no ano.
