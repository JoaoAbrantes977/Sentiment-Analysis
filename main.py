import keyboard as keyboard
import matplotlib.pyplot as plt
import spacy
from textblob import TextBlob
import snscrape.modules.twitter as snstwitter
from wordcloud import WordCloud, STOPWORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

"""
# DOWNLOADS
# pip install keyboard
# nltk.download('movie_reviews')
# nltk.download('averaged_perceptron_tagger')
# python -m spacy download en_core_web_sm
"""

# =============================================================================
# Criado por : João Abrantes Nº 47621
# =============================================================================

"""
################ Scrape de tweets ################
"""

print("################ A carregar tweets... ################")

query = "trump"
tweets = []
limit = 300
for tweet in snstwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append(tweet.content)

for i in tweets:
    print(i)
    print("\n")

"""
################ Guardar Tweets num ficheiro .txt ################
"""

print("################ Guardar Tweets num ficheiro .txt ################" + "\n")
# Guarda os tweets da lista "tweets" para dentro de um ficheiro .txt
# +w para criar um ficheiro com aquele nome caso não exista, encoding="utf-8" para não dar o erro de codificação
f = open("texto.txt", "+w", encoding='utf-8')

for i in tweets:
    f.write(i + "\n")
print("Ficheiro Criado")

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ Calculo da analise de sentimento de cada tweet individual com VADER ################
"""

print("################ Calculo da analise de sentimento de cada tweet individual com VADER ################")

negativos = []
positivos = []

s = SentimentIntensityAnalyzer()

for comment in tweets:
    score = s.polarity_scores(comment)  # calcula o sentimento do tweet, compound é o calculo do sentimento
    if score['compound'] >= 0:
        positivos.append(comment)
    else:
        negativos.append(comment)

print(f"Comentários positivos: {len(positivos)}")
print(f"Comentários negativos: {len(negativos)}")
print("\n")

# vai buscar 10 comentarios positivos ao array
n = 1
print(f"10 comentários  positivos:")
for i in range(10):
    print(f'{n:03d} --> {positivos[i]}')
    n += 1

# vai buscar 10 comentarios negativos ao array
n = 1
print("\n")
print(f"10 comentários  negativos:")
for x in range(10):
    print(f'{n:03d} --> {negativos[x]}')
    n += 1

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ PROCURAR ENTIDADES NO TEXTO COM spaCy ################ 
"""

print("################ PROCURAR ENTIDADES NO TEXTO COM spaCy ################ ")
nlp = spacy.load('en_core_web_sm')

with open('texto.txt', 'r', encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)

# Conta a frequência de cada entidade
entity_counts = {}
for ent in doc.ents:
    if ent.label_ in ('PERSON', 'ORG'):  # Apenas entidades Pessoa ou Organizações
        if ent.text in entity_counts:
            entity_counts[ent.text] += 1
        else:
            entity_counts[ent.text] = 1

# Função lambda para selecionar as entidades por frequência e obter as 10 mais comuns
sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
most_common = sorted_entities[:10]

print("Entidades mais comuns e as suas frenquências ")
print(most_common)

# Retirar apenas 5 entidades da lista das entidades e exclui os numeros
myStringEntidades = []

for i in range(10):
    myStringEntidades.append(most_common[i][0])
print("Lista das Entidades: ")
print(myStringEntidades)
print("\n")

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ ANALISE DE SENTIMENTOS POR CADA ENTIDADE COM spaCy e TextBlob ################ 
"""

print("################ ANALISE DE SENTIMENTOS POR CADA ENTIDADE COM spaCy e TextBlob ################ ")
# Carrega o modelo da lingua em Inglês
nlp = spacy.load('en_core_web_sm')

# Array para guardar os valores correspondentes a cada Entidade
valorEntidades = []

with open('texto.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Processamento do texto
doc = nlp(text)

# loop pela lista de nomes
for entidade in myStringEntidades:
    # Inicialização da string vazia
    myString = ""

    # Loop por cada linha do texto
    for line in text.split('\n'):
        # verifica se a entidade se encontra na respetiva linha
        if entidade in line:
            # se a entidade se encontra na linha então a linha é inserida na string de linhas
            myString += line + '\n'

    # Analise de sentimentos na string
    sentiment = TextBlob(myString).sentiment.polarity
    valorEntidades.append(sentiment)

print("Valor sentimental polarizado das Entidades: ")
print(valorEntidades)
print("\n")

# loop para percorrer por cada entidade verificar se o seu sentimento é positivo, negativo ou neutro
for i in range(len(myStringEntidades)):
    if valorEntidades[i] >= 0.05:
        print(" O Sentimento geral relativamente à entidade " + myStringEntidades[i] + " é positiva")
    elif -0.05 < valorEntidades[i] < 0.05:
        print(" O Sentimento geral relativamente à entidade " + myStringEntidades[i] + " é neutro")
    else:
        print(" O Sentimento geral relativamente à entidade " + myStringEntidades[i] + " é negativo")

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ Mostra 10 comentários positivos e negativos de cada entidade ################ 
"""

print("################ Mostra 10 comentários positivos e negativos de cada entidade ################")
# Carrega o modelo da lingua em Inglês
nlp = spacy.load('en_core_web_sm')

# Abre o ficheiro .txt
with open('texto.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Processamento do texto
doc = nlp(text)


# Função para mostrar frase de positivas e negativas de cada entidade
def calcularSentimento(comments, entidade1):
    positivos = []
    negativos = []

    # Por cada comentario no array comentarios, calcula o valor sentimental da frase se for positiva vai para dentro
    # do array de positivos, caso seja negativa vai para o array de comentarios negativos
    for i in comments:
        sentiment = TextBlob(i).sentiment.polarity

        if sentiment >= 0.05:
            positivos.append(i)
        elif sentiment <= -0.05:
            negativos.append(i)

    # Imprime para a consola se existirem, 10 comentarios positivos e 10 negativos de cada entidade
    print("*****************************")
    print("Comentarios positivos da entidade: " + entidade1 + "\n")

    for i in positivos[:10]:
        print(f'--> {i}')

    print("\n")

    print("Comentarios negativos da entidade: " + entidade1)

    for i in negativos[:10]:
        print(f' --> {i}')


# loop pela lista de nomes
for entidade in myStringEntidades:
    # Inicialização do array vazio para guardar todos os comentarios de uma entidade
    frases = []

    # Loop por cada linha do texto
    for line in text.split('\n'):
        # verifica se a entidade se encontra na respetiva linha
        if entidade in line:
            # se a entidade se encontra na linha então a linha é inserida no array de frases da entidade
            frases.append(line)
    # Chamada da função para imprimir os comentarios positivos e negativos da função
    calcularSentimento(frases, entidade)

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################  CÓDIGO DO GRÁFICO DE BARRAS ################  
"""

print("################  CÓDIGO DO GRÁFICO DE BARRAS ################")
# Gera o gráfico de barras com os nomes das entidades no eixo x e os valores no eixo y

valorReduzido = []
for valor in valorEntidades:
    num = round(valor, 4)
    valorReduzido.append(num)

x = myStringEntidades
y = valorReduzido

fig, ax = plt.subplots(figsize=(12, 8))
for index in range(len(x)):
    ax.text(x[index], y[index], y[index], size=7)
plt.title(" Valor Sentimental por Entidade")
plt.xlabel("Nome das Entidades")
plt.ylabel("Valor Sentimental")
plt.bar(x, y)
plt.show()

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ PROCURAR VERBOS NO TEXTO COM spaCy ################ 
"""

print("################ Frequência de verbos no texto ################ ")

# Carrega o modelo da lingua em Inglês
nlp = spacy.load('en_core_web_sm')

with open('texto.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Processamento do texto
doc = nlp(text)

# Conta a frequência de cada verbo
verb_counts = {}
for token in doc:
    if token.pos_ == 'VERB':
        if token.lemma_ in verb_counts:
            verb_counts[token.lemma_] += 1
        else:
            verb_counts[token.lemma_] = 1

# # Função lambda para selecionar os verbos por frequência e obter os 10 mais comuns
sorted_verbs = sorted(verb_counts.items(), key=lambda x: x[1], reverse=True)
most_common = sorted_verbs[:15]

print("Verbos mais comuns: ")
print(most_common)

# Retirar apenas os verbos da lista dos verbos mais comuns e exclui os numeros, para passar para a wordcloud
myString = ""

for i in range(len(most_common)):
    print(most_common[i][0])
    myString = myString + " " + most_common[i][0]
print(myString)

# Espera pelo clique do utilizador para ir para a proxima parte do codigo
print("Enter para avançar" + "\n")
keyboard.wait('enter')
print('a carregar...' + "\n")

"""
################ WORD CLOUD ################ 
"""

# Ignorar classe de palavras
stopwords = set(STOPWORDS)
stopwords.update(["’", "'s"])

# Word cloud com os verbos mais frequentes
worldcloud = WordCloud(width=800, height=600, stopwords=STOPWORDS, max_font_size=100, max_words=20, collocations=False,
                       background_color="white").generate(myString)
plt.figure(figsize=(40, 30))
plt.imshow(worldcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
