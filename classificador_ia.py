import csv
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

ARQUIVO_ENTRADA = 'denuncias_confidenciais.txt'
ARQUIVO_SAIDA = 'relatorio_classificado.csv'

def classificar_via_regras(texto):
    """BACKUP: Palavras-chave simples."""
    texto = texto.lower()
    if any(x in texto for x in ['desvio', 'roubo', 'assédio', 'fraude', 'crime', 'licitação', 'suborno', 'racista', 'coagindo', 'copiando']):
        return "COMPLIANCE", "ALTO"
    elif any(x in texto for x in ['cadeira', 'ar condicionado', 'quebrada', 'luz', 'mofo', 'pingando', 'impressora', 'toner', 'estacionamento']):
        return "INFRAESTRUTURA", "BAIXO"
    else:
        return "CLIMA", "MÉDIO"

def classificar_via_ia(texto):
    """
    Usa Few-Shot Prompting para ensinar o modelo Gemma.
    """
    prompt_sistema = """
    Você é um classificador de denúncias corporativas.
    Analise a queixa e retorne APENAS: Categoria | Risco.
    
    Use estas opções:
    - Categorias: COMPLIANCE, INFRAESTRUTURA, CLIMA
    - Riscos: ALTO, MÉDIO, BAIXO

    EXEMPLOS DE COMO RESPONDER:
    Entrada: "O diretor está roubando o caixa."
    Saída: COMPLIANCE | ALTO

    Entrada: "O ar condicionado quebrou."
    Saída: INFRAESTRUTURA | BAIXO

    Entrada: "Não gosto do café."
    Saída: CLIMA | BAIXO

    AGORA É SUA VEZ. NÃO explique, apenas classifique.
    """
    
    try:
        response = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Entrada: \"{texto}\"\nSaída:"}
            ],
            temperature=0.1,
            max_tokens=10
        )
        
        resposta = response.choices[0].message.content.strip()
        
        resposta = resposta.replace(".", "").replace('"', '').replace("Saída: ", "")

        if "|" in resposta:
            partes = resposta.split('|')
            return partes[0].strip(), partes[1].strip()
        else:
            raise ValueError(f"Formato inválido: {resposta}")

    except Exception as e:
        return classificar_via_regras(texto)

def processar():
    print("--- Classificação Otimizada (Few-Shot) ---")
    try:
        with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f_in:
            leitor = csv.reader(f_in, delimiter=';')
            cabecalho = next(leitor)
            
            dados_finais = []
            contagem_ia = 0
            contagem_backup = 0
            
            for linha in leitor:
                id_ticket, data, depto, relato = linha
                
                print(f"Ticket {id_ticket}...", end=" ")
                
                categoria, risco = classificar_via_ia(relato)
                
                print(f"-> {categoria} | {risco}")
                dados_finais.append([id_ticket, depto, categoria, risco, relato])

        with open(ARQUIVO_SAIDA, 'w', newline='', encoding='utf-8') as f_out:
            escritor = csv.writer(f_out, delimiter=';')
            escritor.writerow(['ID', 'DEPARTAMENTO', 'CATEGORIA', 'RISCO', 'RELATO'])
            escritor.writerows(dados_finais)
            
        print(f"\n✅ Relatório salvo em: {ARQUIVO_SAIDA}")

    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")

if __name__ == "__main__":
    processar()