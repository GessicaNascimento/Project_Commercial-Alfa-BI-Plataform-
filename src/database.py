import os
from configparser import ConfigParser

def load_db_config(filename='database.ini', section='postgresql'):
    # Encontra o diretório onde o próprio arquivo database.py está guardado (src/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Sobe um nível e entra na pasta config de forma absoluta
    path_to_ini = os.path.join(base_dir, '..', 'config', filename)
    
    # Inicializa o parser
    parser = ConfigParser()
    
    if not os.path.exists(path_to_ini):
        raise FileNotFoundError(f"Erro de Configuração: O arquivo {path_to_ini} não foi encontrado.")
        
    parser.read(path_to_ini)
    
    # (Mantenha o restante do seu código original que lê a seção abaixo daqui)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
        
    return db