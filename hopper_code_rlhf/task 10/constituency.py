import pandas as pd
import gzip
import json
import stanza
import nltk
import time

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF('../../All_datasets/Amazon Data/Cell_Phones_and_Accessories_5.json.gz')
new_df = df[['reviewText','summary','overall']][0:10000]

nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')
start_time = time.time()

review = new_df["reviewText"][24]
print(f'La oración es: {review}')

phrases = []
review_doc = nlp(review)

def few_phrases(tree):
    num_nps, num_vps = 0, 0
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            num_nps += 1
        elif subtree.label() == "VP":
            num_vps += 1
    return num_nps, num_vps


for sentence in review_doc.sentences:
    tree = nltk.ParentedTree.fromstring(str(sentence.constituency))
    if tree.pretty_print() is not None:
        print(f'El árbol general es: {tree.pretty_print()} y el tipo es {type(tree.pretty_print())}')

    if  tree.label() == 'ROOT':
            num_nps, num_vps = few_phrases(tree)
            print(num_nps, num_vps)
            if num_nps <=1 or num_vps <=1:
                phrases.append(" ".join(tree.leaves()))

    for i, subtree in enumerate(tree.subtrees()):

        if subtree.label() == 'ROOT' or subtree.parent().label() == 'ROOT' or subtree.parent().parent().label() == 'ROOT':
            # print((subtree.label()))
            continue

        if subtree.label() == 'NP' and subtree.right_sibling() is not None and subtree.right_sibling().label() == 'VP':
            subtree_text = " ".join(subtree.leaves())+ " " + " ".join(subtree.right_sibling().leaves())
            print(f'El texto de la subfrase #{i} es: {subtree_text}')
            phrases.append(subtree_text)

print("------------------------------")
print("La revisión completa es:")
print(review)
print("Las frases finales son:")
print(phrases)
print(f'La longitud de la oración completa es: {len(review.split())}')
print(f'La longitud de las frases es: {sum(len(phrase.split()) for phrase in phrases)}')

end_time = time.time()
total_time = end_time - start_time

print(f"Tiempo de ejecución: {total_time:.4f} segundos")
