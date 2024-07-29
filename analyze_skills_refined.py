import spacy
from collections import Counter
import matplotlib.pyplot as plt

# Carregar modelo de NLP do spaCy
nlp = spacy.load("en_core_web_sm")

# Exemplo de currículo (substitua isso pelo texto real do seu currículo)
curriculo = """
Experienced Product Manager with a degree in Business Administration and certifications in SFPC, SFC, CEA, and CPA10. Over 12 years of experience at the largest bank in Latin America, managing client portfolios for both individuals and businesses. Developed skills in project management, Scrum, SQL, and digital marketing. Achieved significant KPIs including an NPS of 8.5, a product churn rate of 2%, and a client retention rate of 95%. Successfully increased product and service contracts through electronic channels by 50% and monthly revenue by 20%.
"""

# Lista de habilidades conhecidas (baseada nas informações que você forneceu)
habilidades_conhecidas = [
    "Project Management", "Scrum", "SQL", "Digital Marketing", 
    "Business Administration", "SFPC", "SFC", "CEA", "CPA10", 
    "Client Portfolio Management", "KPI Achievement", "NPS", "Churn Rate", "Client Retention"
]

# Função para determinar senioridade
def determinar_senioridade(anos_experiencia):
    if anos_experiencia < 3:
        return "Júnior"
    elif 3 <= anos_experiencia <= 7:
        return "Pleno"
    else:
        return "Sênior"

# Analisar anos de experiência
anos_experiencia = 0
for ent in nlp(curriculo).ents:
    if ent.label_ == "DATE":
        if "year" in ent.text or "years" in ent.text:
            anos_experiencia = int(ent.text.split()[0])

nivel_senioridade = determinar_senioridade(anos_experiencia)

# Contar a frequência das habilidades no currículo
contagem_habilidades = Counter()

for habilidade in habilidades_conhecidas:
    if habilidade.lower() in curriculo.lower():
        contagem_habilidades[habilidade] += 1

# Exibir as habilidades e suas pontuações iniciais
print("Habilidades e Pontuações Iniciais:")
for habilidade, contagem in contagem_habilidades.items():
    print(f"Habilidade: {habilidade}, Pontuação: {contagem}")

# Atribuir pontuações adicionais com base no contexto
contextos_positivos = ["achieved", "improved", "success", "increased", "significant", "successfully", "enhanced", "boosted", "optimized", "led"]

for sent in nlp(curriculo).sents:
    for habilidade in habilidades_conhecidas:
        if habilidade.lower() in sent.text.lower():
            if any(word in sent.text.lower() for word in contextos_positivos):
                contagem_habilidades[habilidade] += 2  # Adicionar pontuação extra para contextos positivos

# Exibir as habilidades e suas pontuações ajustadas
print("\nHabilidades e Pontuações Ajustadas:")
for habilidade, contagem in contagem_habilidades.items():
    print(f"Habilidade: {habilidade}, Pontuação Ajustada: {contagem}")

# Visualização dos resultados
habilidades = list(contagem_habilidades.keys())
pontuacoes = list(contagem_habilidades.values())

plt.figure(figsize=(12, 8))
plt.barh(habilidades, pontuacoes, color='skyblue')
plt.xlabel('Pontuação')
plt.ylabel('Habilidade')
plt.title(f'Pontuação das Habilidades com Base no Currículo ({nivel_senioridade})')
plt.grid(axis='x')
plt.show()

print(f"\nNível de Senioridade: {nivel_senioridade}")
