import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
ARQUIVO_ENTRADA = 'relatorio_classificado.csv'

def gerar_dashboard():
    print("--- Gerando Indicadores Visuais ---")
    
    try:
        df = pd.read_csv(ARQUIVO_ENTRADA, delimiter=';', encoding='utf-8')
        
        print(f"Dados carregados: {len(df)} registros.")
        
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=df, x='CATEGORIA', hue='CATEGORIA', palette='viridis', legend=False)
        plt.title('Volume de Denúncias por Categoria', fontsize=16)
        plt.xlabel('Categoria', fontsize=12)
        plt.ylabel('Quantidade de Tickets', fontsize=12)
        
        plt.savefig('grafico_categorias.png')
        print("📊 Gráfico 1 salvo: grafico_categorias.png")
        plt.close()

        plt.figure(figsize=(8, 8))
        contagem_risco = df['RISCO'].value_counts()
        
        cores_risco = {'ALTO': '#ff6666', 'MÉDIO': '#ffcc99', 'BAIXO': '#99ff99'}
        cores_usadas = [cores_risco.get(x, '#cccccc') for x in contagem_risco.index]

        plt.pie(contagem_risco, labels=contagem_risco.index, autopct='%1.1f%%', startangle=140, colors=cores_usadas)
        plt.title('Nível de Criticidade das Denúncias', fontsize=16)
        
        plt.savefig('grafico_riscos.png')
        print("🍕 Gráfico 2 salvo: grafico_riscos.png")
        plt.close()

        print("\n✅ Dashboard gerado com sucesso! Verifique as imagens na pasta.")

    except FileNotFoundError:
        print(f"❌ Erro: O arquivo {ARQUIVO_ENTRADA} não existe. Rode o classificador primeiro.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    gerar_dashboard()