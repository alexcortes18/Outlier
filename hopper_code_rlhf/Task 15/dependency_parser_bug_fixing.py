import re
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')

# Función para cargar los datos desde un archivo
def loadData(path):
    with open(path) as f:
        sents = []
        for line in f.readlines():
            line = line.strip("\n").split("\t")
            if len(line) <= 2:  # Asegurarse de que hay suficientes columnas
                sents.append(line[1]) #Bug 1: Debería de ser line[1] porque solo hay un tab entre los dos campos de cada línea.
    return pd.DataFrame({"sentence": sents})

# # Cargar datos desde el archivo "sentences.s2orc.txt"
data = loadData("sentences.s2orc.txt")
nlp.max_length = 1500000
data_text = ""

# Concatenar todas las oraciones en un solo texto
for sentence in data['sentence']:
    data_text += sentence + " "

# Procesar el texto completo con spaCy
data_doc = [sent for sent in nlp(data_text).sents]
temp_data_doc = []
for sentence in data_doc:
    temp_sentence = sentence.text
    # Reemplazar las entidades con sus etiquetas
    for entity in sentence.ents:
        temp_sentence = temp_sentence.replace(entity.text, entity.ent_label_) #Bug 2: El correcto es: entity.label_
    temp_data_doc.append(temp_sentence)

# Identificación de estructuras gramaticales VERB-ADP-NOUN:

# Función para recorrer el árbol sintáctico y encontrar las estructuras
def traverse_tree(token, ans_list): #Bug 3: Debería de ser "VERB" primero y después "ADP"
    ans_list = [] #Bug 4: No deberíamos de re-inicializar esta lista.
    if token.pos_ == "ADP":
        for child in token.children:
            if child.pos_ == "VERB":
                for child2 in child.children:
                    if child2.pos_ == "NOUN":
                        ans_list.append((token, child, child2))

# Lista para almacenar las estructuras encontradas
dep_gp = []
for sentence in data_doc:
    for token in sentence.text: #Bug 5: Debería de ser solo "sentence" sin el ".text"
        if token.dep_ == 'ROOT':
            traverse_tree(token, dep_gp)
            
# Imprimir la cantidad de estructuras encontradas y el número de elementos únicos
print(len(dep_gp), len(set(dep_gp)))
print(dep_gp)

# Imprimir todas las estructuras VERB-ADP-NOUN que contienen el verbo "charge".
counter = 0
word = 'provide'
for tuple in dep_gp:
    if tuple[0].text == word: #Bug 6: Debería de ser tuple[0].lemma_
        print(tuple)
        counter += 1
print(f"Tuplas en dep_gp con {word} son {counter}.")
