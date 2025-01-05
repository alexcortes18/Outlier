from bs4 import BeautifulSoup
from collections import defaultdict
import json

def parse_xml(file_path):
    """
    Analiza un archivo XML y devuelve un objeto BeautifulSoup.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

def extract_homograph_info(soup):
    """
    Extrae información de homógrafos del objeto BeautifulSoup.
    """
    homograph_dict = defaultdict(lambda: {'metadata': {}, 'parts_of_speech': set()})
    
    # Iterar sobre cada elemento 'homograph' en el XML
    for homograph in soup.find_all('homograph'):
        word = homograph.get('word')
        if not word:
            continue  # Saltar si no hay palabra
        
        # Extraer metadatos
        for metadata in homograph.find_all('metadata'):
            key = metadata.get('key')
            value = metadata.get('value')
            if key and value:
                homograph_dict[word]['metadata'][key] = value
        
        # Extraer partes de discurso
        for part_of_speech in homograph.find_all('part_of_speech'):
            pos = part_of_speech.get('tag')
            if pos:
                homograph_dict[word]['parts_of_speech'].add(pos)
    
    return homograph_dict

def main():
    file_path = 'med.cd.az.xml'  # Ruta al archivo XML
    soup = parse_xml(file_path)
    homograph_info = extract_homograph_info(soup)
    
    # Imprimir la información de los homógrafos
    for word, info in homograph_info.items():
        print(f"Palabra: {word}")
        print("Metadatos:")
        for key, value in info['metadata'].items():
            print(f"  {key}: {value}")
        print("Partes de discurso:")
        for pos in info['parts_of_speech']:
            print(f"  {pos}")
        print("-" * 40)

if __name__ == '__main__':
    main()