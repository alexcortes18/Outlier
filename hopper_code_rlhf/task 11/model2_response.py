from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def parse_xml(file_path):
    """Analiza el archivo XML y retorna un objeto BeautifulSoup."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'xml')
        return soup
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
    except Exception as e:
        print(f"Error al analizar el archivo XML: {e}")
    return None


def extract_homograph_info(homograph_tag):
    """Extrae la información relevante de un tag <homograph>."""
    info = {
        'lemma': homograph_tag.find('lemma').text.strip(),
        'pronunciation': homograph_tag.find('pronunciation').text.strip(),
        'pos': [tag.text.strip() for tag in homograph_tag.find_all('pos')],
        'senses': []
    }

    for sense_tag in homograph_tag.find_all('sense'):
        sense = {
            'id': sense_tag.get('id'),
            'definition': sense_tag.find('definition').text.strip(),
            'examples': [example.text.strip() for example in sense_tag.find_all('example')]
        }
        info['senses'].append(sense)

    return info


def extract_metadata_homographs(soup):
    """Extrae la metadatos de todos los homógrafos del archivo XML."""
    homographs = {}
    for lemma_tag in soup.find_all('lemma'):
        lemma_id = lemma_tag.get('id')
        
        # Inicializar la lista de homógrafos para este lemma si no existe
        if lemma_id not in homographs:
            homographs[lemma_id] = []
        
        homograph_tags = lemma_tag.find_all('homograph')
        
        # Extraer la información de cada homógrafo y agregarla a la lista
        for homograph_tag in homograph_tags:
            homograph_info = extract_homograph_info(homograph_tag)
            homographs[lemma_id].append(homograph_info)

    return homographs


def main():
    file_path = 'med.cd.az.xml'
    soup = parse_xml(file_path)

    if soup:
        homograph_data = extract_metadata_homographs(soup)
        
        # Ejemplo de cómo imprimir los datos
        for lemma_id, homographs in homograph_data.items():
            print(f"Lemma ID: {lemma_id}")
            for homograph in homographs:
                print(f"  Lemma: {homograph['lemma']}")
                print(f"  Pronunciación: {homograph['pronunciation']}")
                print(f"  Partes del discurso: {', '.join(homograph['pos'])}")
                for i, sense in enumerate(homograph['senses'], 1):
                    print(f"    Sentido {i}:")
                    print(f"      Definición: {sense['definition']}")
                    for example in sense['examples']:
                        print(f"      Ejemplo: {example}")
                    print()
            print()


if __name__ == "__main__":
    main()