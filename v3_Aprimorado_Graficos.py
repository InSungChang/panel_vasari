import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# --- Configuração da Página Streamlit ---
st.set_page_config(
    page_title="Dashboard Meta Ads - Análise Estratégica Aprimorada",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título Principal do Dashboard ---
st.title("🚀 Dashboard Meta Ads - Análise Estratégica Avançada e Diagnóstica")
st.markdown("Faça o upload da sua planilha do Meta Ads para obter recomendações estratégicas para otimização de campanhas de Facebook e Instagram Ads.")

# --- Definição de Colunas (Permanecem as mesmas do v3.txt original) ---
COLUNAS = {
    'conta': 'Nome da conta',
    'campanha': 'Nome da campanha',
    'conjunto': 'Nome do conjunto de anúncios',
    'anuncio': 'Nome do anúncio',
    'plataforma': 'Plataforma',
    'posicionamento': 'Posicionamento',
    'dia': 'Dia',
    'objetivo': 'Objetivo',
    'alcance': 'Alcance',
    'impressoes': 'Impressões',
    'cliques_todos': 'Cliques (todos)',
    'cpc_todos': 'CPC (todos)',
    'investimento': 'Valor usado (BRL)',
    'frequencia': 'Frequência',
    'cliques_link': 'Cliques no link',
    'cpc_link': 'CPC (custo por clique no link)',
    'ctr_todos': 'CTR (todos)',
    'cpm': 'CPM (custo por 1.000 impressões)',
    'ctr_link': 'CTR (taxa de cliques no link)',
    'conversas': 'Conversas por mensagem iniciadas',
    'custo_conversa': 'Custo por conversa por mensagem iniciada'
}

# --- Banco de Insights Aprimorados (NOVO) ---
INSIGHTS_APRIMORADOS = {
    "⛔ PAUSAR (Alto Gasto, Zero Leads)": "Anúncio gastou significativamente sem gerar resultados. Pausar imediatamente para evitar desperdício de orçamento. Criativo/segmentação inadequados.",
    "⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)": "Anúncio com baixo investimento e sem conversões. Aguardar mais dados ou testar pequenas otimizações antes de pausar/descartar. Ainda está na fase de aprendizado.",
    "📈 DUPLICAR (Performance Excelente)": "Anúncio com CPL(Custo por Lead) excepcional e ótimo CTR(Taxa de Cliques no Link). Duplicar para escalar, expandir públicos e maximizar resultados, monitorando de perto o CPL(Custo por Lead) e a frequência.",
    "🎨 NOVO CRIATIVO (Fadiga Detectada)": "Frequência alta com CPL(Custo por Lead) aceitável/ruim. O público está saturado. Requer novos ângulos criativos para reengajar e manter a oferta relevante.",
    "🔧 OTIMIZAR (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo)": "CPL(Custo por Lead) razoável, mas CTR(Taxa de Cliques no Link) baixo. O criativo ou a copy (texto do anúncio) não estão atraindo. Ajustar copy, CTA (Chamada para Ação), imagem/vídeo para aumentar o engajamento e a qualificação dos cliques.",
    "🔧 OTIMIZAR (Custo de Exibição Alto/CPM(Custo por Mil Impressões))": "CPL(Custo por Lead) razoável, mas CPM(Custo por Mil Impressões) alto. O custo para exibir o anúncio está elevado. Testar novos públicos, refinar segmentação ou ajustar lances para reduzir o custo por impressão.",
    "🔧 OTIMIZAR (Oferta/Funil Pós-Clique)": "CPL(Custo por Lead) razoável, com bom CTR(Taxa de Cliques no Link) e CPM(Custo por Mil Impressões). O problema pode estar na qualificação do lead, na oferta ou na experiência pós-clique (ex: landing page, atendimento). Revisar a jornada do usuário e a promessa do anúncio.",
    "🔧 OTIMIZAR (Ajustes Finas/Monitoramento)": "Anúncio com bom desempenho geral, mas não excelente o suficiente para duplicar. Buscar pequenas melhorias contínuas, testar variações sutis ou apenas monitorar sua estabilidade.",
    "🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)": "Anúncio gerando leads, mas com CPL(Custo por Lead) muito, muito alto, e não é um caso de fadiga isolada. O criativo/oferta parece fundamentalmente inadequado. Requer uma nova abordagem criativa e estratégica desde o início.",
    "🔄 RECRIAR (Métricas Fracas/Sem Direção)": "Anúncio com performance geral fraca, sem uma causa óbvia de otimização clara (não é só fadiga, nem só um CPL(Custo por Lead) alto isolado). Considerar desativar e iniciar novos testes criativos e de público.",
    "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)": "Anúncio que não se encaixou nas categorias específicas. Requer uma análise mais aprofundada por um especialista para identificar as causas da performance e definir a próxima ação. Pode ser um erro de segmentação, oferta ou produto."
}

# --- Sidebar para Configurações dos Parâmetros da Lógica (APRIMORADO) ---
st.sidebar.header("⚙️ Configurações de Análise")
st.sidebar.markdown("Ajuste os parâmetros para refinar as recomendações.")

cpl_meta = st.sidebar.number_input("🎯 CPL Meta (R$) (Custo por Lead/Conversa Desejado)", min_value=1.0, value=25.0, step=1.0,
                                    help="O valor médio que você deseja gastar para adquirir um lead ou iniciar uma conversa.")
ctr_meta = st.sidebar.number_input("📊 CTR Link Meta (%) (Taxa de Cliques no Link Desejada)", min_value=0.1, value=1.0, step=0.1, format="%.1f",
                                   help="A porcentagem de pessoas que clicaram no seu link após verem o anúncio. Usada para avaliar a relevância do criativo.")
cpm_meta = st.sidebar.number_input("💸 CPM Meta (R$) (Custo por Mil Impressões Desejado)", min_value=0.1, value=25.0, step=0.5,
                                   help="O custo para exibir seu anúncio mil vezes. Usado para avaliar o custo de exibição e saturação do público.")
freq_limite = st.sidebar.number_input("⚡ Frequência Máxima", min_value=1.0, value=2.0, step=0.1, format="%.1f",
                                      help="Número médio de vezes que uma pessoa viu o anúncio. Acima deste limite, pode indicar fadiga do criativo, levando à queda de performance.")
investimento_min = st.sidebar.number_input("💰 Investimento Mín. para Pausar (R$)", min_value=1.0, value=5.0, step=1.0,
                                         help="Valor gasto mínimo para que um anúncio sem conversas seja recomendado para 'Pausar'. Abaixo deste valor, ele é 'Mantido em Análise' para coletar mais dados.")
valor_lead = st.sidebar.number_input("💎 Valor Estimado por Lead (R$)", min_value=10.0, value=100.0, step=10.0,
                                      help="O valor médio que cada lead representa em receita ou lucro para o seu negócio. Usado para calcular o Retorno sobre o Investimento (ROI).")

# Novos parâmetros para refinar a lógica de "Otimizar" e "Recriar"
cpl_mult_duplicar = st.sidebar.number_input("Multiplicador CPL(Custo por Lead) Duplicar (vs. Meta)", min_value=0.1, value=0.7, step=0.1, format="%.1f",
                                            help="Define o limite de CPL(Custo por Lead) para 'Duplicar'. Anúncios com CPL(Custo por Lead) menor ou igual a (CPL Meta * este Multiplicador) serão considerados para duplicação.")
cpl_mult_recriar = st.sidebar.number_input("Multiplicador CPL(Custo por Lead) Recriar (vs. Meta)", min_value=1.5, value=2.5, step=0.1, format="%.1f",
                                           help="Define o limite de CPL(Custo por Lead) para 'Recriar'. Anúncios com CPL(Custo por Lead) maior que (CPL Meta * este Multiplicador) serão considerados para recriação total.")
ctr_mult_relevancia = st.sidebar.number_input("Multiplicador CTR(Taxa de Cliques no Link) Relevância (vs. Meta)", min_value=0.1, value=0.7, step=0.1, format="%.1f",
                                              help="Define o limiar para identificar baixa relevância criativa. CTR(Taxa de Cliques no Link) menor que (CTR Meta * este Multiplicador) indica que o criativo precisa de otimização.")
taxa_conversao_meta_pct = st.sidebar.number_input("Taxa de Conversão Meta (%) (Cliques -> Leads)", min_value=0.1, value=5.0, step=0.1, format="%.1f",
                                                  help="A porcentagem desejada de cliques no link que resultam em uma conversa/lead. Usada para diagnosticar problemas no funil pós-clique.")


# --- Função de Classificação Aprimorada (APRIMORADO) ---
def recomendar_acao(row):
    # Garante que os valores sejam numéricos; NaN se houver erro ou ausência.
    cpl_calc = row.get('cpl_calculado')
    ctr_link = row.get(COLUNAS['ctr_link'])
    cpm = row.get(COLUNAS['cpm'])
    conversas = row.get(COLUNAS['conversas'])
    investimento = row.get(COLUNAS['investimento'])
    frequencia = row.get(COLUNAS['frequencia'])
    cliques_link = row.get(COLUNAS['cliques_link'])

    # Tratamento de NaNs (importante para comparações numéricas)
    cpl_calc = cpl_calc if pd.notna(cpl_calc) and cpl_calc != np.inf else float('inf')
    ctr_link = ctr_link if pd.notna(ctr_link) else 0.0
    cpm = cpm if pd.notna(cpm) else float('inf')
    frequencia = frequencia if pd.notna(frequencia) else 0.0
    conversas = conversas if pd.notna(conversas) else 0.0
    investimento = investimento if pd.notna(investimento) else 0.0
    cliques_link = cliques_link if pd.notna(cliques_link) else 0.0

    # Calcula taxa de conversão (do clique para o lead)
    # Evita divisão por zero ou infinito se não houver cliques no link
    taxa_conversao_clique_lead = (conversas / cliques_link * 100) if cliques_link > 0 else 0.0

    acao = ''

    # 1. Lógica para PAUSAR / MANTER EM ANÁLISE (Zero Conversas)
    if conversas == 0:
        if investimento >= investimento_min:
            acao = "⛔ PAUSAR (Alto Gasto, Zero Leads)"
        else:
            acao = "⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)"
        return acao

    # --- Anúncios com Leads (Análise de Performance Detalhada) ---

    # 2. Lógica para DUPLICAR (Excelente Performance)
    # Combina CPL(Custo por Lead) muito baixo com CTR(Taxa de Cliques no Link) muito bom
    if cpl_calc <= cpl_meta * cpl_mult_duplicar and ctr_link >= ctr_meta * 1.2:
        acao = "📈 DUPLICAR (Performance Excelente)"
        return acao

    # 3. Lógica para RECRIAR (CPL(Custo por Lead) Inviável - o criativo/oferta está fundamentalmente errado)
    # Esta é uma falha grave, mesmo com leads, o custo é inviável
    if cpl_calc > cpl_meta * cpl_mult_recriar:
        acao = "🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)"
        return acao

    # 4. Lógica para NOVO CRIATIVO (Fadiga)
    # Anúncio fadigado, mas CPL(Custo por Lead) ainda gerenciável (não inviável)
    if frequencia >= freq_limite:
        acao = "🎨 NOVO CRIATIVO (Fadiga Detectada)"
        return acao

    # 5. Lógica para OTIMIZAR (Diagnósticos detalhados)
    # Para anúncios que geram leads, não são excelentes, não são inviáveis e não estão fadigados
    if cpl_calc > cpl_meta * cpl_mult_duplicar and cpl_calc <= cpl_meta:
        # 5.1 Otimizar: Relevância do Criativo (CTR(Taxa de Cliques no Link) Baixo)
        if ctr_link < ctr_meta * ctr_mult_relevancia:
            acao = "🔧 OTIMIZAR (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo)"
        # 5.2 Otimizar: Custo de Exibição (CPM(Custo por Mil Impressões) Alto)
        elif cpm > cpm_meta * 1.2: # CPM 20% acima da meta
            acao = "🔧 OTIMIZAR (Custo de Exibição Alto/CPM(Custo por Mil Impressões))"
        # 5.3 Otimizar: Oferta/Funil Pós-Clique (Taxa de Conversão Baixa, mas CTR(Taxa de Cliques no Link)/CPM(Custo por Mil Impressões) ok)
        elif taxa_conversao_clique_lead < taxa_conversao_meta_pct:
            acao = "🔧 OTIMIZAR (Oferta/Funil Pós-Clique)"
        # 5.4 Otimizar: Ajustes Finas (Bom desempenho, sem grandes problemas evidentes)
        else:
            acao = "🔧 OTIMIZAR (Ajustes Finas/Monitoramento)"
        return acao

    # 6. Fallback - Para qualquer outro cenário que gerou leads, mas não se encaixou nas regras claras.
    # Ex: CPL(Custo por Lead) um pouco acima da meta, mas não o suficiente para ser 'Recriar Inviável', e sem fadiga.
    acao = "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)"
    return acao


# --- Upload de arquivo Excel ---
file = st.file_uploader("📂 Faça upload da sua planilha do Meta Ads (.xlsx)", type="xlsx", help="Certifique-se de que a planilha contenha as colunas necessárias para a análise.")

df = None

if file:
    if not file.name.endswith('.xlsx'):
        st.error("❌ Erro: Por favor, faça upload de um arquivo no formato **.xlsx**.")
    else:
        with st.spinner("🚀 Processando e validando sua planilha..."):
            try:
                df_raw = pd.read_excel(file)

                if df_raw.empty:
                    st.error("🚫 Erro: O arquivo Excel carregado está vazio ou não contém dados válidos. Por favor, verifique sua planilha.")
                    df = None
                else:
                    # Mapeamento de colunas (mantido do v3 original, certifique-se que seus nomes batam)
                    # Exemplo: 'Valor usado (BRL)' -> COLUNAS['investimento']
                    df_processed = df_raw.rename(columns={
                        'Nome da conta': COLUNAS['conta'],
                        'Nome da campanha': COLUNAS['campanha'],
                        'Nome do conjunto de anúncios': COLUNAS['conjunto'],
                        'Nome do anúncio': COLUNAS['anuncio'],
                        'Plataforma': COLUNAS['plataforma'],
                        'Posicionamento': COLUNAS['posicionamento'],
                        'Dia': COLUNAS['dia'],
                        'Objetivo': COLUNAS['objetivo'],
                        'Alcance': COLUNAS['alcance'],
                        'Impressões': COLUNAS['impressoes'],
                        'Cliques (todos)': COLUNAS['cliques_todos'],
                        'CPC (todos)': COLUNAS['cpc_todos'],
                        'Valor usado (BRL)': COLUNAS['investimento'],
                        'Frequência': COLUNAS['frequencia'],
                        'Cliques no link': COLUNAS['cliques_link'],
                        'CPC (custo por clique no link)': COLUNAS['cpc_link'],
                        'CTR (todos)': COLUNAS['ctr_todos'],
                        'CPM (custo por 1.000 impressões)': COLUNAS['cpm'],
                        'CTR (taxa de cliques no link)': COLUNAS['ctr_link'],
                        'Conversas por mensagem iniciadas': COLUNAS['conversas'],
                        'Custo por conversa por mensagem iniciada': COLUNAS['custo_conversa']
                    })

                    # Validar se as colunas essenciais para o dashboard existem no DF
                    colunas_essenciais_para_logica = [
                        COLUNAS['investimento'], COLUNAS['conversas'], COLUNAS['campanha'],
                        COLUNAS['anuncio'], COLUNAS['ctr_link'], COLUNAS['cpm'],
                        COLUNAS['frequencia'], COLUNAS['cliques_link']
                    ]
                    missing_cols = [col for col in colunas_essenciais_para_logica if col not in df_processed.columns]

                    if missing_cols:
                        st.error(f"⚠️ Erro: As seguintes colunas essenciais estão faltando na sua planilha: **{', '.join(missing_cols)}**.\n\nPor favor, exporte seu relatório do Meta Ads com essas colunas.")
                        st.info("💡 **Dica:** Ao exportar do Meta Ads, verifique as opções de 'Colunas' ou 'Quebrar por' para incluir todas as métricas e dimensões necessárias.")
                        df = None
                    else:
                        df = df_processed.copy()

                        # Limpeza e preparação dos dados (mantido do v3 original, com pequenas adaptações)
                        numeric_columns_to_process = [
                            COLUNAS['investimento'], COLUNAS['conversas'], COLUNAS['alcance'],
                            COLUNAS['impressoes'], COLUNAS['frequencia'], COLUNAS['ctr_link'],
                            COLUNAS['cpm'], COLUNAS['cliques_link']
                        ]
                        for col in numeric_columns_to_process:
                            if col in df.columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

                        # NOVAS COLUNAS DE ANÁLISE (mantido do v3 original, com pequenas adaptações)
                        st.header("🔬 Criando Análises Avançadas...")
                        with st.spinner("Processando análises estratégicas..."):
                            # 1. CPL(Custo por Lead) Calculado
                            df['cpl_calculado'] = np.where(
                                df[COLUNAS['conversas']] > 0,
                                df[COLUNAS['investimento']] / df[COLUNAS['conversas']],
                                np.inf
                            )

                            # 2. Taxa de Conversão (Cliques no Link -> Conversas)
                            df['taxa_conversao'] = np.where(
                                df[COLUNAS['cliques_link']] > 0,
                                df[COLUNAS['conversas']] / df[COLUNAS['cliques_link']] * 100,
                                0
                            )

                            # Aplica a função de recomendação aprimorada
                            df['recomendacao_acao'] = df.apply(recomendar_acao, axis=1)

                            # Demais análises do v3.txt (mantidas e ajustadas para as novas recomendações)
                            # 3. Classificação de Performance (Pode ser ajustado para refletir a nova lógica)
                            def classificar_performance(row):
                                acao = row['recomendacao_acao']
                                if acao.startswith("⛔ PAUSAR"): return "🚨 PÉSSIMO"
                                if acao.startswith("⏳ MANTER"): return "⏳ INCIPIENTE"
                                if acao.startswith("📈 DUPLICAR"): return "🏆 EXCELENTE"
                                if acao.startswith("🎨 NOVO CRIATIVO"): return "📉 FADIGA"
                                if acao.startswith("🔧 OTIMIZAR"): return "⚠️ REQUER OTIMIZAÇÃO"
                                if acao.startswith("🔄 RECRIAR"): return "🔥 RUIM"
                                if acao.startswith("💡 REAVALIAR"): return "❓ REAVALIAR"
                                return "❓ DESCONHECIDO" # Fallback

                            df['classificacao_performance'] = df.apply(classificar_performance, axis=1)

                            # 4. Eficiência de Custo
                            df['eficiencia_custo'] = np.where(
                                df[COLUNAS['conversas']] > 0,
                                np.where(df['cpl_calculado'] <= cpl_meta * 0.7, 'Alto',
                                np.where(df['cpl_calculado'] <= cpl_meta, 'Médio', 'Baixo')),
                                'Sem Conversão'
                            )

                            # 5. Potencial de Escala
                            df['potencial_escala'] = np.where(
                                (df['cpl_calculado'] <= cpl_meta) & (df[COLUNAS['conversas']] >= 1),
                                '🚀 Alto Potencial',
                                np.where(df[COLUNAS['conversas']] > 0, '🔧 Otimizar Primeiro', '⛔ Não Escalar')
                            )

                            # 6. Status de Fadiga (Agora mais um indicador do que uma ação primária)
                            df['status_fadiga'] = np.where(
                                df[COLUNAS['frequencia']] >= freq_limite,
                                '😴 Fadiga Detectada',
                                '✅ Saudável'
                            )

                            # 7. Prioridade de Ação (Ajustado para novas categorias)
                            prioridade_map = {
                                '⛔ PAUSAR (Alto Gasto, Zero Leads)': 'CRÍTICA',
                                '⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)': 'BAIXA',
                                '📈 DUPLICAR (Performance Excelente)': 'ALTA',
                                '🎨 NOVO CRIATIVO (Fadiga Detectada)': 'MÉDIA',
                                '🔧 OTIMIZAR (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo)': 'MÉDIA',
                                '🔧 OTIMIZAR (Custo de Exibição Alto/CPM(Custo por Mil Impressões))': 'MÉDIA',
                                '🔧 OTIMIZAR (Oferta/Funil Pós-Clique)': 'MÉDIA',
                                '🔧 OTIMIZAR (Ajustes Finas/Monitoramento)': 'BAIXA', # Ajustado para Baixa
                                '🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)': 'CRÍTICA',
                                '🔄 RECRIAR (Métricas Fracas/Sem Direção)': 'ALTA', # Ajustado para Alta
                                '💡 REAVALIAR ESTRATÉGIA (Outros Cenários)': 'MÉDIA' # Mantido Média
                            }
                            df['prioridade'] = df['recomendacao_acao'].map(prioridade_map)


                            # 8. ROI Estimado
                            df['roi_estimado'] = np.where(
                                df[COLUNAS['investimento']] > 0,
                                ((df[COLUNAS['conversas']] * valor_lead) - df[COLUNAS['investimento']]) / df[COLUNAS['investimento']] * 100,
                                0
                            )

                            # 9. Score de Qualidade (0-100) - Mantido do v3.txt, mas com os novos parâmetros
                            def calcular_score_qualidade(row):
                                score = 0
                                # CTR(Taxa de Cliques no Link) (30 pontos)
                                ctr_actual = row.get(COLUNAS['ctr_link'], 0)
                                if ctr_actual >= ctr_meta * 1.5: score += 30
                                elif ctr_actual >= ctr_meta: score += 20
                                elif ctr_actual >= ctr_meta * 0.5: score += 10
                                # CPL(Custo por Lead) (40 pontos)
                                if row[COLUNAS['conversas']] > 0:
                                    if row['cpl_calculado'] <= cpl_meta * 0.7: score += 40
                                    elif row['cpl_calculado'] <= cpl_meta: score += 30
                                    elif row['cpl_calculado'] <= cpl_meta * 1.5: score += 15
                                # Frequência (20 pontos)
                                freq_actual = row.get(COLUNAS['frequencia'], 0)
                                if freq_actual <= freq_limite * 0.7: score += 20
                                elif freq_actual <= freq_limite: score += 15
                                elif freq_actual <= freq_limite * 1.3: score += 5
                                # Conversões (10 pontos)
                                if row[COLUNAS['conversas']] >= 3: score += 10
                                elif row[COLUNAS['conversas']] >= 1: score += 7
                                return min(score, 100) # Garante que o score não ultrapasse 100

                            df['score_qualidade'] = df.apply(calcular_score_qualidade, axis=1)

                            # 10. Categoria de Anúncio - Mantido (Específico do Nicho)
                            def categorizar_anuncio(nome_anuncio):
                                nome = str(nome_anuncio).upper()
                                if 'IMPLANTE' in nome: return '🦷 Implantes'
                                elif 'LENTE' in nome or 'FACETA' in nome: return '✨ Facetas/Lentes'
                                elif 'CLINICA' in nome: return '🏥 Institucional'
                                else: return '📋 Outros'
                            df['categoria_anuncio'] = df[COLUNAS['anuncio']].apply(categorizar_anuncio)

                            # 11. Análise de Posicionamento - Mantido
                            def analisar_posicionamento(posicionamento):
                                pos = str(posicionamento).lower()
                                if 'feed' in pos: return '📱 Feed'
                                elif 'stories' in pos or 'story' in pos: return '📖 Stories'
                                elif 'reels' in pos: return '🎥 Reels'
                                elif 'video' in pos: return '📺 Vídeo'
                                else: return '🔄 Outros'
                            df['categoria_posicionamento'] = df[COLUNAS['posicionamento']].apply(analisar_posicionamento)

                            # 12. Eficiência por Impressão (leads por 1000 impressões)
                            df['eficiencia_impressao'] = np.where(
                                df[COLUNAS['impressoes']] > 0,
                                df[COLUNAS['conversas']] / df[COLUNAS['impressoes']] * 1000,
                                0
                            )

                        st.success("✅ Análises criadas com sucesso!")

            except Exception as e:
                st.error(f"💔 Ocorreu um erro inesperado ao ler o arquivo. Por favor, verifique se é um arquivo Excel válido e não está corrompido. Detalhes do erro: `{e}`")
                df = None
else:
    st.info("⬆️ Faça o upload de uma planilha .xlsx para começar a visualizar seu dashboard.")

# --- O restante do seu código do dashboard só será executado se 'df' não for None ---
if df is not None:
    # DASHBOARD PRINCIPAL
    st.header("📊 Dashboard de Performance")

    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    total_investido = df[COLUNAS['investimento']].sum()
    total_leads = df[COLUNAS['conversas']].sum()
    cpl_medio = total_investido / total_leads if total_leads > 0 else 0

    col1.metric("💰 Investimento Total", f"R$ {total_investido:,.2f}")
    col2.metric("🎯 Total de Leads", f"{int(total_leads)}")
    col3.metric("📈 CPL(Custo por Lead) Médio", f"R$ {cpl_medio:,.2f}")
    col4.metric("👁️ Impressões", f"{df[COLUNAS['impressoes']].sum():,.0f}")
    col5.metric("⚡ CTR(Taxa de Cliques no Link) Médio", f"{df[COLUNAS['ctr_link']].mean():.2f}%")

    # Distribuição de ações recomendadas (NOVO E MELHORADO)
    st.subheader("🎯 Distribuição de Recomendações")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Tipos de Ações Recomendadas")
        acao_counts = df['recomendacao_acao'].value_counts()

        # Define um mapa de cores mais simples baseado no tipo principal de ação
        simplified_colors_map = {
            "⛔ PAUSAR": '#DC3545',     # Vermelho para ações críticas de pausa
            "⏳ MANTER": '#FFC107',     # Amarelo/Laranja para manter em análise
            "📈 DUPLICAR": '#28A745',   # Verde para ações de escala
            "🎨 NOVO CRIATIVO": '#17A2B8', # Ciano para novos criativos
            "🔧 OTIMIZAR": '#6C757D',   # Cinza para otimizações
            "🔄 RECRIAR": '#6F42C1',    # Roxo para recriar
            "💡 REAVALIAR": '#A9A9A9'   # Cinza mais claro para reavaliar
        }

        plot_colors = []
        for action_label in acao_counts.index:
            found_color = False
            for key, color in simplified_colors_map.items():
                if action_label.startswith(key):
                    plot_colors.append(color)
                    found_color = True
                    break
            if not found_color:
                plot_colors.append('#CCCCCC') # Fallback color

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(acao_counts.index, acao_counts.values, color=plot_colors)
        ax.set_xlabel('Ação')
        ax.set_ylabel('Quantidade de Anúncios')
        ax.set_title('') # Título já está no st.subheader
        plt.xticks(rotation=45, ha='right') # Ajusta rotação e alinhamento para nomes longos
        plt.tight_layout() # Ajusta o layout para evitar sobreposição
        st.pyplot(fig)


    with col2:
        st.markdown("##### Nível de Prioridade das Ações")
        prioridade_counts = df['prioridade'].value_counts()
        # Definir ordem das prioridades para o gráfico
        prioridade_order = ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA']
        # Reindexar para garantir a ordem e incluir prioridades que podem ter 0 anúncios
        prioridade_counts = prioridade_counts.reindex(prioridade_order, fill_value=0)

        fig_priority, ax_priority = plt.subplots(figsize=(8, 6)) # Aumenta o tamanho
        # Cores para as prioridades (distintas do gráfico de ações)
        priority_colors = {
            'CRÍTICA': '#DC3545', # Vermelho forte
            'ALTA': '#FD7E14',    # Laranja
            'MÉDIA': '#FFC107',   # Amarelo
            'BAIXA': '#28A745'    # Verde
        }
        bar_colors = [priority_colors.get(p, '#6C757D') for p in prioridade_counts.index]

        # Inverte a ordem para que 'CRÍTICA' fique no topo se for horizontal
        # Garante que a ordem visual das barras corresponda à 'prioridade_order'
        prioridade_counts_sorted = prioridade_counts[prioridade_order[::-1]] # Inverte a ordem para plotar

        ax_priority.barh(prioridade_counts_sorted.index, prioridade_counts_sorted.values, color=bar_colors[::-1]) # Inverte cores também
        ax_priority.set_xlabel('Quantidade de Anúncios')
        ax_priority.set_ylabel('Prioridade')
        ax_priority.set_title('') # Título já está no st.subheader
        # Adicionar valores nas barras
        for index, value in enumerate(prioridade_counts_sorted.values):
            ax_priority.text(value, index, str(value), va='center') # Adiciona o número dentro/ao lado da barra

        plt.tight_layout()
        st.pyplot(fig_priority)

    # Análise por categoria de anúncio
    st.subheader("📊 Performance por Categoria de Anúncio")
    categoria_stats = df.groupby('categoria_anuncio').agg(
        investimento=(COLUNAS['investimento'], 'sum'),
        conversas=(COLUNAS['conversas'], 'sum'),
        score_qualidade=('score_qualidade', 'mean'),
        impressoes=(COLUNAS['impressoes'], 'sum')
    ).reset_index()
    categoria_stats['cpl_categoria'] = np.where(
        categoria_stats['conversas'] > 0,
        categoria_stats['investimento'] / categoria_stats['conversas'],
        np.inf
    )

    st.dataframe(categoria_stats.style.format({
        'investimento': 'R$ {:.2f}',
        'cpl_categoria': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'score_qualidade': '{:.1f}',
        'impressoes': '{:,.0f}'
    }))

    # Análise por posicionamento
    st.subheader("📱 Performance por Posicionamento")
    posicionamento_stats = df.groupby('categoria_posicionamento').agg(
        investimento=(COLUNAS['investimento'], 'sum'),
        conversas=(COLUNAS['conversas'], 'sum'),
        ctr_link=(COLUNAS['ctr_link'], 'mean'),
        eficiencia_impressao=('eficiencia_impressao', 'mean')
    ).reset_index()
    posicionamento_stats['cpl_posicionamento'] = np.where(
        posicionamento_stats['conversas'] > 0,
        posicionamento_stats['investimento'] / posicionamento_stats['conversas'],
        np.inf
    )

    st.dataframe(posicionamento_stats.style.format({
        'investimento': 'R$ {:.2f}',
        'cpl_posicionamento': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'ctr_link': '{:.2f}%',
        'eficiencia_impressao': '{:.3f}'
    }))

    # Top anúncios por categoria
    st.subheader("🏆 Top 5 Performers por Categoria")

    for categoria in df['categoria_anuncio'].unique():
        if pd.notna(categoria):
            st.write(f"### {categoria}")
            df_categoria = df[df['categoria_anuncio'] == categoria]
            # Filtrar por anúncios que geraram conversas e não foram marcados para Pausar por alto gasto e zero leads
            df_top = df_categoria[df_categoria[COLUNAS['conversas']] > 0].nsmallest(5, 'cpl_calculado')

            if not df_top.empty:
                cols_display = [
                    COLUNAS['anuncio'],
                    COLUNAS['investimento'],
                    COLUNAS['conversas'],
                    'cpl_calculado',
                    'score_qualidade',
                    'recomendacao_acao',
                    'prioridade' # Adicionado prioridade para visualização
                ]
                st.dataframe(df_top[cols_display].style.format({
                    COLUNAS['investimento']: 'R$ {:.2f}',
                    'cpl_calculado': 'R$ {:.2f}',
                    'score_qualidade': '{:.0f}'
                }))
            else:
                st.info(f"Nenhum anúncio com conversão encontrado para {categoria}")

    # Análise temporal
    if COLUNAS['dia'] in df.columns:
        st.subheader("📅 Análise de Tendência por Dia")
        df[COLUNAS['dia']] = pd.to_datetime(df[COLUNAS['dia']], errors='coerce')
        df_temporal = df.groupby(COLUNAS['dia']).agg(
            investimento=(COLUNAS['investimento'], 'sum'),
            conversas=(COLUNAS['conversas'], 'sum')
        ).reset_index()

        df_temporal['cpl_diario'] = np.where(
            df_temporal['conversas'] > 0,
            df_temporal['investimento'] / df_temporal['conversas'],
            np.nan
        )

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Investimento e leads por dia
        ax1.plot(df_temporal[COLUNAS['dia']], df_temporal['investimento'], label='Investimento', color='blue')
        ax1_twin = ax1.twinx()
        ax1_twin.plot(df_temporal[COLUNAS['dia']], df_temporal['conversas'],
                     label='Leads', color='green', linestyle='--')
        ax1.set_ylabel('Investimento (R$)', color='blue')
        ax1_twin.set_ylabel('Leads', color='green')
        ax1.set_title('Investimento e Leads por Dia')
        ax1.tick_params(axis='x', rotation=45) # Rotaciona labels do eixo X
        ax1.legend(loc="upper left")
        ax1_twin.legend(loc="upper right")

        # CPL(Custo por Lead) por dia
        ax2.plot(df_temporal[COLUNAS['dia']], df_temporal['cpl_diario'], color='red', marker='o')
        ax2.set_ylabel('CPL(Custo por Lead) (R$)')
        ax2.set_title('CPL(Custo por Lead) por Dia')
        ax2.axhline(y=cpl_meta, color='orange', linestyle='--', label=f'Meta CPL(Custo por Lead) (R$ {cpl_meta})')
        ax2.legend()
        ax2.grid(True)
        ax2.tick_params(axis='x', rotation=45) # Rotaciona labels do eixo X

        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.warning("⚠️ Coluna 'Dia' não encontrada. Exporte seu relatório do Meta Ads com a opção 'Quebrar por Dia' para ativar esta análise de tendência.")

    # Tabela completa com filtros
    st.subheader("📋 Análise Detalhada com Filtros")

    # Filtros
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        campanhas = ['Todas'] + list(df[COLUNAS['campanha']].unique())
        campanha_selecionada = st.selectbox("Campanha", campanhas)

    with col2:
        acoes = ['Todas'] + list(df['recomendacao_acao'].unique())
        acao_selecionada = st.selectbox("Ação Recomendada", acoes)

    with col3:
        categorias = ['Todas'] + list(df['categoria_anuncio'].unique())
        categoria_selecionada = st.selectbox("Categoria", categorias)

    with col4:
        prioridades = ['Todas'] + list(df['prioridade'].unique())
        prioridade_selecionada = st.selectbox("Prioridade", prioridades)

    # Aplicar filtros
    df_filtered = df.copy()
    if campanha_selecionada != 'Todas': df_filtered = df_filtered[df_filtered[COLUNAS['campanha']] == campanha_selecionada]
    if acao_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['recomendacao_acao'] == acao_selecionada]
    if categoria_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['categoria_anuncio'] == categoria_selecionada]
    if prioridade_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['prioridade'] == prioridade_selecionada]

    # Colunas para exibição
    colunas_exibicao = [
        COLUNAS['campanha'], COLUNAS['anuncio'], 'categoria_anuncio',
        'categoria_posicionamento', COLUNAS['investimento'], COLUNAS['conversas'],
        'cpl_calculado', 'classificacao_performance', 'recomendacao_acao',
        'prioridade', 'score_qualidade', 'roi_estimado', 'status_fadiga',
        'taxa_conversao', COLUNAS['ctr_link'], COLUNAS['cpm'], COLUNAS['frequencia'], COLUNAS['cliques_link']
    ]

    st.dataframe(
        df_filtered[colunas_exibicao].style.format({
            COLUNAS['investimento']: 'R$ {:.2f}',
            'cpl_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
            'score_qualidade': '{:.0f}',
            'roi_estimado': '{:.1f}%',
            'taxa_conversao': '{:.2f}%',
            COLUNAS['ctr_link']: '{:.2f}%',
            COLUNAS['cpm']: 'R$ {:.2f}',
            COLUNAS['frequencia']: '{:.2f}',
            COLUNAS['cliques_link']: '{:,.0f}'
        }),
        use_container_width=True
    )

    # Download da planilha analisada
    st.subheader("📥 Download da Análise")

    @st.cache_data
    def convert_df_to_excel(dataframe):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Análise_Completa')
        return output.getvalue()

    excel_data = convert_df_to_excel(df_filtered)
    st.download_button(
        label="📊 Baixar Planilha com Análises",
        data=excel_data,
        file_name=f"analise_meta_ads_aprimorada_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Resumo executivo
    st.header("📋 Resumo Executivo")

    # Calcula as contagens para o resumo
    pausar_urgente = len(df[df['recomendacao_acao'] == '⛔ PAUSAR (Alto Gasto, Zero Leads)'])
    manter_em_analise = len(df[df['recomendacao_acao'] == '⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)'])
    duplicar = len(df[df['recomendacao_acao'] == '📈 DUPLICAR (Performance Excelente)'])
    novo_criativo = len(df[df['recomendacao_acao'] == '🎨 NOVO CRIATIVO (Fadiga Detectada)'])
    recriar_cpl_inviavel = len(df[df['recomendacao_acao'] == '🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)'])
    recriar_metricas_fracas = len(df[df['recomendacao_acao'] == '🔄 RECRIAR (Métricas Fracas/Sem Direção)'])
    otimizar_relevancia = len(df[df['recomendacao_acao'] == '🔧 OTIMIZAR (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo)'])
    otimizar_custo_exibicao = len(df[df['recomendacao_acao'] == '🔧 OTIMIZAR (Custo de Exibição Alto/CPM(Custo por Mil Impressões))'])
    otimizar_oferta_funil = len(df[df['recomendacao_acao'] == '🔧 OTIMIZAR (Oferta/Funil Pós-Clique)'])
    otimizar_ajustes_finais = len(df[df['recomendacao_acao'] == '🔧 OTIMIZAR (Ajustes Finas/Monitoramento)'])
    reavaliar_estrategia = len(df[df['recomendacao_acao'] == '💡 REAVALIAR ESTRATÉGIA (Outros Cenários)'])

    # Cálculo da economia potencial (apenas anúncios para PAUSAR com gasto >= investimento_min)
    economia_potencial = df[df['recomendacao_acao'] == '⛔ PAUSAR (Alto Gasto, Zero Leads)'][COLUNAS['investimento']].sum()

    st.markdown(f"""
    ### 🎯 **Ações Prioritárias Detalhadas:**
    
    **🚨 CRÍTICA - Pausar e Recriar:**
    *   **⛔ Pausar (Alto Gasto, Zero Leads): {pausar_urgente} anúncios** 
        > {INSIGHTS_APRIMORADOS['⛔ PAUSAR (Alto Gasto, Zero Leads)']}
    *   **🔄 Recriar (CPL(Custo por Lead) Inviável/Criativo Inadequado): {recriar_cpl_inviavel} anúncios**
        > {INSIGHTS_APRIMORADOS['🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)']}
    
    **📈 ALTA - Escalar e Renovar Estratégia:**
    *   **📈 Duplicar (Performance Excelente): {duplicar} anúncios**
        > {INSIGHTS_APRIMORADOS['📈 DUPLICAR (Performance Excelente)']}
    *   **🔄 Recriar (Métricas Fracas/Sem Direção): {recriar_metricas_fracas} anúncios**
        > {INSIGHTS_APRIMORADOS['🔄 RECRIAR (Métricas Fracas/Sem Direção)']}

    **🔧 MÉDIA - Otimizar e Diagnosticar:**
    *   **🎨 Novo Criativo (Fadiga Detectada): {novo_criativo} anúncios**
        > {INSIGHTS_APRIMORADOS['🎨 NOVO CRIATIVO (Fadiga Detectada)']}
    *   **🔧 Otimizar (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo): {otimizar_relevancia} anúncios**
        > {INSIGHTS_APRIMORADOS['🔧 OTIMIZAR (Relevância Criativo/CTR(Taxa de Cliques no Link) Baixo)']}
    *   **🔧 Otimizar (Custo de Exibição Alto/CPM(Custo por Mil Impressões)): {otimizar_custo_exibicao} anúncios**
        > {INSIGHTS_APRIMORADOS['🔧 OTIMIZAR (Custo de Exibição Alto/CPM(Custo por Mil Impressões))']}
    *   **🔧 Otimizar (Oferta/Funil Pós-Clique): {otimizar_oferta_funil} anúncios**
        > {INSIGHTS_APRIMORADOS['🔧 OTIMIZAR (Oferta/Funil Pós-Clique)']}
    *   **💡 Reavaliar Estratégia (Outros Cenários): {reavaliar_estrategia} anúncios**
        > {INSIGHTS_APRIMORADOS['💡 REAVALIAR ESTRATÉGIA (Outros Cenários)']}

    **⏳ BAIXA - Monitorar:**
    *   **⏳ Manter em Análise (Baixo Gasto, Zero Leads): {manter_em_analise} anúncios**
        > {INSIGHTS_APRIMORADOS['⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)']}
    *   **🔧 Otimizar (Ajustes Finas/Monitoramento): {otimizar_ajustes_finais} anúncios**
        > {INSIGHTS_APRIMORADOS['🔧 OTIMIZAR (Ajustes Finas/Monitoramento)']}

    ---

    ### 💡 **Principais Insights Globais:**
    
    1.  **CPL (Custo por Lead/Conversa) Médio Atual:** R$ {cpl_medio:.2f} (Meta: R$ {cpl_meta:.2f}) - {('Atingido' if cpl_medio <= cpl_meta else 'Acima da Meta')}
    2.  **Taxa de Conversão (Cliques -> Leads):** {df['taxa_conversao'].mean():.2f}% - Média geral da eficiência do funil pós-clique.
    3.  **Economia Potencial (Pausando Ineficientes):** R$ {economia_potencial:.2f} - Valor que pode ser realocado imediatamente para anúncios de melhor performance.
    4.  **ROI (Retorno sobre o Investimento) Médio (Estimado):** {df['roi_estimado'].mean():.1f}% - Retorno potencial geral da conta com base no valor de um lead.
    5.  **Score Médio de Qualidade:** {df['score_qualidade'].mean():.1f}/100 - Avaliação sintética da saúde geral dos anúncios.

    ---

    ### 🚀 **Próximos Passos Recomendados:**
    
    1.  **Ação Imediata:** Pausar anúncios classificados como "⛔ PAUSAR (Alto Gasto, Zero Leads)".
    2.  **Acelerar Crescimento:** Duplicar e escalar anúncios classificados como "📈 DUPLICAR (Performance Excelente)".
    3.  **Renovação Constante:** Criar novos criativos para anúncios com "🎨 NOVO CRIATIVO (Fadiga Detectada)" ou "🔄 RECRIAR (CPL(Custo por Lead) Inviável/Criativo Inadequado)".
    4.  **Análise e Ajustes Pontuais:** Focar em otimizar anúncios classificados como "🔧 OTIMIZAR (...)" com base nos diagnósticos detalhados.
    5.  **Revisão Estratégica:** Avaliar profundamente os anúncios em "🔄 RECRIAR (Métricas Fracas/Sem Direção)" e "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)" para entender falhas e planejar novos testes.
    6.  **Realocação de Orçamento:** Transferir o orçamento economizado para anúncios de alta performance e novos testes.
    """)
