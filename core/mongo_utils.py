from pymongo import MongoClient
from django.utils import timezone

# Tua string de conexão do Atlas com a palavra-passe preenchida
MONGO_URI = "mongodb+srv://anagonzalis_db_user:4xKdrqcrdw3LUTiF@cluster0.fvovu4a.mongodb.net/?retryWrites=true&w=majority"

def get_mongo_db():
    client = MongoClient(MONGO_URI)
    return client['geosolutions_db']

def registrar_log_auditoria(projeto_id, usuario, acao, detalhes=None):
    try:
        db = get_mongo_db()
        log_doc = {
            "projeto_id": projeto_id,
            "usuario": usuario,
            "acao": acao,
            "detalhes": detalhes or {},
            "data_hora": timezone.now().isoformat()
        }
        db.logs_auditoria.insert_one(log_doc)
        print(f"[MongoDB Log] Log gravado com sucesso para o projeto {projeto_id}")
    except Exception as e:
        print(f"[MongoDB Error] Falha ao gravar log: {e}")