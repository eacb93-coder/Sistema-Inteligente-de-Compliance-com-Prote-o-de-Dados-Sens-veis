import csv
import random
from faker import Faker

fake = Faker('pt_BR')
NOME_ARQUIVO = 'denuncias_confidenciais.txt'
QTD_REGISTROS = 50

TEMPLATES_RELATOS = [
    # ALTO RISCO (Compliance / Ética)
    "o diretor financeiro pediu para alterar a data da nota fiscal",
    "ouvi comentários preconceituosos do gestor na reunião",
    "estão contratando fornecedores sem licitação, parece esquema",
    "vi um funcionário copiando o banco de dados de clientes",
    "o supervisor está obrigando a equipe a trabalhar sem bater ponto",
    "sofri assédio moral na frente de todos, gritaram comigo",
    "suspeita de suborno na negociação com a empresa de limpeza",
    
    # MÉDIO/BAIXO RISCO (Infra / Operacional)
    "o ar condicionado do 3º andar está pingando nas mesas",
    "faltam cadeiras ergonômicas, estou com dor nas costas",
    "a impressora do setor fiscal está sem toner há dias",
    "o carpete da sala de reuniões está com cheiro de mofo",
    "a porta de emergência está bloqueada por caixas",
    "os monitores novos ainda não foram instalados",
    
    # IRRELEVANTE (Clima / Opinião)
    "não gosto da marca de café que estão comprando",
    "deveriam liberar bermuda nas sextas-feiras",
    "a música ambiente do refeitório é muito alta",
    "o estacionamento deveria ser coberto para todos",
    "acho que a parede da recepção ficaria melhor azul"
]

# 2. Contexto Inicial (Abertura formal)
CONTEXTO_INICIAL = [
    "Gostaria de relatar que",
    "Infelizmente presenciei uma situação onde",
    "Venho por meio deste canal informar que",
    "Quero fazer uma denúncia anônima pois",
    "Notei algo errado:",
    "Durante o expediente de ontem,",
    "Estou preocupado porque"
]

# 3. Desfecho (Fechamento)
DESFECHOS = [
    "Isso é inadmissível na nossa cultura.",
    "Aguardo providências urgentes.",
    "Isso está atrapalhando meu desempenho.",
    "Alguém precisa fazer alguma coisa.",
    "Espero que a diretoria resolva.",
    "Fico no aguardo de uma solução.",
    "Isso vai contra as regras da empresa."
]

DEPARTAMENTOS = ['Financeiro', 'RH', 'Vendas', 'Operações', 'TI', 'Jurídico', 'Marketing']

def gerar_dataset_sintetico():
    print(f"--- Gerando {QTD_REGISTROS} denúncias em PT-BR (Sem Latim) ---")
    dados = []
    
    for i in range(QTD_REGISTROS):
        id_ticket = fake.uuid4()[:8]
        data_relato = fake.date_between(start_date='-6m', end_date='today')
        departamento = random.choice(DEPARTAMENTOS)
        
        inicio = random.choice(CONTEXTO_INICIAL)
        meio = random.choice(TEMPLATES_RELATOS)
        fim = random.choice(DESFECHOS)
        
        relato_final = f"{inicio} {meio}. {fim}"

        dados.append([id_ticket, data_relato, departamento, relato_final])

    with open(NOME_ARQUIVO, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(['ID_TICKET', 'DATA', 'DEPARTAMENTO', 'RELATO_ANONIMO'])
        escritor.writerows(dados)
        
    print(f"✅ Sucesso! Arquivo '{NOME_ARQUIVO}' renovado.")
    print(f"Exemplo gerado: {dados[0][3]}")

if __name__ == "__main__":
    gerar_dataset_sintetico()