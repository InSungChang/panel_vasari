import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# --- Configuração da Página Streamlit ---
st.set_page_config(
    page_title="Dashboard Meta Ads - Análise Estratégica Aprimorada e Orientada por Objetivo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título Principal do Dashboard ---
st.title("🚀 Dashboard Meta Ads - Análise Estratégica Avançada e Diagnóstica por Objetivo")
st.markdown("Faça o upload da sua planilha do Meta Ads para obter recomendações estratégicas para otimização de campanhas de Facebook e Instagram Ads.")

# --- Definição de Colunas (Expandido para incluir novas métricas) ---
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
    'custo_conversa': 'Custo por conversa por mensagem iniciada',
    # Novas colunas adicionadas para análise por objetivo
    'reproducoes_video_3s': 'Reproduções do vídeo por no mínimo 3 segundos',
    'custo_reproducao_video_3s': 'Custo por reprodução de vídeo por no mínimo 3 segundos',
    'visualizacoes_pagina_destino': 'Visualizações da página de destino',
    'resultados': 'Resultados',
    'custo_resultado': 'Custo por resultado'
}

# --- Banco de Insights Aprimorados (EXPANDIDO) ---
INSIGHTS_APRIMORADOS = {
    # Cenários de "Pausar" e "Manter em Análise"
    "⛔ PAUSAR (Alto Gasto, Zero Leads)": "Anúncio de conversão gastou significativamente sem gerar leads. Pausar imediatamente para evitar desperdício de orçamento. Criativo/segmentação inadequados ou erro fundamental.",
    "⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)": "Anúncio de conversão com baixo investimento e sem leads. Ainda na fase de aprendizado. Aguardar mais dados ou testar pequenas otimizações antes de pausar.",
    "⛔ PAUSAR (Alto Gasto, Sem Cliques no Link - Tráfego)": "Anúncio de tráfego gastou significativamente sem gerar cliques no link. Pausar para evitar desperdício. Criativo ou público-alvo podem estar inadequados.",
    "⏳ MANTER EM ANÁLISE (Baixo Gasto, Sem Cliques no Link - Tráfego)": "Anúncio de tráfego com baixo investimento e sem cliques no link. Monitorar, pode estar em fase de aprendizado.",
    "⛔ PAUSAR (Alto Gasto, Baixo Alcance/Impressões - Awareness)": "Anúncio de awareness/vídeo gastou significativamente sem entregar alcance ou impressões relevantes. Orçamento ineficiente para o objetivo.",
    "⏳ MANTER EM ANÁLISE (Baixo Gasto, Baixo Alcance/Impressões - Awareness)": "Anúncio de awareness/vídeo com baixo investimento e entrega limitada. Monitorar, pode precisar de mais tempo ou otimização de lance.",

    # Cenários de "Duplicar"
    "📈 DUPLICAR (Performance Excelente - Conversão/Leads)": "Anúncio de conversão com CPL excepcional e ótimo CTR. Duplicar para escalar, expandir públicos e maximizar resultados, monitorando de perto CPL e frequência.",
    "📈 DUPLICAR (CPL Excelente, CTR Link Baixo/N/A - Conversão/Leads)": "Anúncio de conversão com CPL excepcional, mas com CTR Link baixo ou não aplicável. Isso pode ocorrer em campanhas 'Click-to-Message' ou conversões diretas que não dependem de um clique em link tradicional. Duplicar e escalar com foco no CPL e volume de leads.",
    "📈 DUPLICAR (Performance Excelente - Tráfego)": "Anúncio de tráfego com CPC excelente e alto CTR no link. Duplicar para escalar o volume de visitas qualificado para a página de destino.",
    "📈 DUPLICAR (Performance Excelente - Awareness/Vídeo)": "Anúncio de awareness/vídeo com CPM muito baixo e boa frequência. Duplicar para escalar alcance ou visualizações de forma eficiente.",

    # Cenários de "Recriar"
    "🔄 RECRIAR (CPL Inviável/Criativo Inadequado - Conversão)": "Anúncio de conversão gerando leads, mas com CPL muito, muito alto. O criativo/oferta parece fundamentalmente inadequado. Requer uma nova abordagem estratégica desde o início.",
    "🔄 RECRIAR (Métricas Fracas/Sem Direção - Conversão)": "Anúncio de conversão com performance geral fraca, sem uma causa óbvia de otimização clara. Considerar desativar e iniciar novos testes criativos e de público.",
    "🔄 RECRIAR (CPC Inviável/Criativo Inadequado - Tráfego)": "Anúncio de tráfego gerando cliques, mas com CPC muito alto. O criativo/oferta pode não ser relevante para o público ou a concorrência é alta. Requer nova abordagem.",
    "🔄 RECRIAR (Métricas Fracas/Sem Direção - Tráfego)": "Anúncio de tráfego com performance geral fraca, não gerando cliques a custo razoável. Recriar com novos criativos e segmentações.",
    "🔄 RECRIAR (CPM Inviável/Criativo Inadequado - Awareness)": "Anúncio de awareness/vídeo com CPM muito alto, indicando alto custo para entregar impressões. O público ou o posicionamento podem ser caros ou o criativo não é atrativo para o algoritmo. Recriar.",
    "🔄 RECRIAR (Métricas Fracas/Sem Direção - Awareness)": "Anúncio de awareness/vídeo com baixo alcance/impressões para o gasto. Recriar com novos criativos e segmentações para melhorar a entrega.",

    # Cenários de "Otimizar"
    "🎨 NOVO CRIATIVO (Fadiga Detectada)": "Anúncio com frequência alta com métricas aceitáveis/ruins. O público está saturado. Requer novos ângulos criativos para reengajar e manter a oferta relevante.",
    "🔧 OTIMIZAR (Relevância Criativo/CTR Baixo - Conversão/Tráfego)": "CPL/CPC razoável, mas CTR baixo. O criativo ou a copy não estão atraindo. Ajustar copy, CTA, imagem/vídeo para aumentar engajamento e qualificação dos cliques.",
    "🔧 OTIMIZAR (Custo de Exibição Alto/CPM - Geral)": "CPL/CPC razoável, mas CPM alto. O custo para exibir o anúncio está elevado. Testar novos públicos, refinar segmentação ou ajustar lances para reduzir o custo por impressão.",
    "🔧 OTIMIZAR (Oferta/Funil Pós-Clique - Conversão)": "CPL razoável, com bom CTR e CPM. O problema pode estar na qualificação do lead, na oferta ou na experiência pós-clique (ex: landing page, atendimento). Revisar a jornada do usuário e a promessa do anúncio.",
    "🔧 OTIMIZAR (Ajustes Finas/Monitoramento - Geral)": "Anúncio com bom desempenho geral, mas não excelente o suficiente para duplicar. Buscar pequenas melhorias contínuas, testar variações sutis ou apenas monitorar sua estabilidade.",
    "🔧 OTIMIZAR (Qualidade do Vídeo/Custo - Awareness)": "CPM razoável, mas custo por visualização de vídeo muito alto. O criativo de vídeo não está prendendo a atenção. Otimizar a qualidade, duração ou gancho inicial do vídeo.",
    "🔧 OTIMIZAR (Problema na Landing Page - Tráfego)": "Anúncio de tráfego que gera cliques no link, mas as visualizações da página de destino ou a taxa de conversão pós-clique estão baixas. Indica problema na landing page, funil ou qualificação do clique.",

    # Cenário "Reavaliar Estratégia"
    "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)": "Anúncio que não se encaixou nas categorias específicas. Requer uma análise mais aprofundada por um especialista para identificar as causas da performance e definir a próxima ação. Pode ser um erro de segmentação, oferta ou produto."
}

# --- Sidebar para Configurações dos Parâmetros da Lógica (APRIMORADO POR OBJETIVO) ---
st.sidebar.header("⚙️ Configurações de Análise")
st.sidebar.markdown("Ajuste os parâmetros para refinar as recomendações com base no objetivo da campanha.")

# --- Parâmetros para Conversão/Leads ---
st.sidebar.subheader("📈 Conversão/Geração de Leads")
cpl_meta = st.sidebar.number_input("🎯 CPL Meta (R$) (Custo por Lead/Conversa Desejado)", min_value=1.0, value=25.0, step=1.0,
                                    help="O valor médio que você deseja gastar para adquirir um lead ou iniciar uma conversa para objetivos de conversão.")
cpl_mult_duplicar = st.sidebar.number_input("Multiplicador CPL Duplicar (vs. Meta)", min_value=0.1, value=0.7, step=0.1, format="%.1f",
                                            help="Define o limite de CPL para 'Duplicar'. Anúncios com CPL menor ou igual a (CPL Meta * este Multiplicador) serão considerados para duplicação.")
cpl_mult_recriar = st.sidebar.number_input("Multiplicador CPL Recriar (vs. Meta)", min_value=1.5, value=2.5, step=0.1, format="%.1f",
                                           help="Define o limite de CPL para 'Recriar'. Anúncios com CPL maior que (CPL Meta * este Multiplicador) serão considerados para recriação total.")
ctr_meta = st.sidebar.number_input("📊 CTR Link Meta (%) (Conversão/Leads)", min_value=0.1, value=1.0, step=0.1, format="%.1f",
                                   help="A porcentagem de pessoas que clicaram no seu link após verem o anúncio. Usada para avaliar a relevância do criativo para este objetivo.")
taxa_conversao_meta_pct = st.sidebar.number_input("Taxa de Conversão Meta (%) (Cliques -> Leads)", min_value=0.1, value=5.0, step=0.1, format="%.1f",
                                                  help="A porcentagem desejada de cliques no link que resultam em uma conversa/lead. Usada para diagnosticar problemas no funil pós-clique.")
investimento_min_leads = st.sidebar.number_input("💰 Investimento Mín. para Pausar (R$ - Leads)", min_value=1.0, value=5.0, step=1.0,
                                         help="Valor gasto mínimo para que um anúncio de conversão sem resultados seja recomendado para 'Pausar'.")


# --- Parâmetros para Tráfego ---
st.sidebar.subheader("🌐 Tráfego")
cpc_meta_trafego = st.sidebar.number_input("💲 CPC Meta (R$) (Custo por Clique no Link Desejado)", min_value=0.01, value=2.0, step=0.1, format="%.2f",
                                      help="O custo por clique no link desejado para objetivos de tráfego.")
ctr_meta_trafego = st.sidebar.number_input("📊 CTR Link Meta (%) (Tráfego)", min_value=0.1, value=1.5, step=0.1, format="%.1f",
                                    help="A porcentagem de cliques no link desejada para objetivos de tráfego.")
investimento_min_trafego = st.sidebar.number_input("💰 Investimento Mín. para Pausar (R$ - Tráfego)", min_value=1.0, value=3.0, step=1.0,
                                         help="Valor gasto mínimo para que um anúncio de tráfego sem resultados seja recomendado para 'Pausar'.")


# --- Parâmetros para Awareness/Vídeo ---
st.sidebar.subheader("👁️ Awareness/Visualização de Vídeo")
cpm_meta_awareness = st.sidebar.number_input("💸 CPM Meta (R$) (Custo por Mil Impressões Desejado)", min_value=0.1, value=20.0, step=0.5,
                                   help="O custo para exibir seu anúncio mil vezes desejado para objetivos de awareness/vídeo.")
cpv_3s_meta = st.sidebar.number_input("🎥 CPV 3s Meta (R$) (Custo por Visualização de Vídeo 3s)", min_value=0.01, value=0.05, step=0.01, format="%.2f",
                                   help="O custo por visualização de 3 segundos desejado para objetivos de vídeo.")
freq_limite = st.sidebar.number_input("⚡ Frequência Máxima (Geral)", min_value=1.0, value=2.0, step=0.1, format="%.1f",
                                      help="Número médio de vezes que uma pessoa viu o anúncio. Acima deste limite, pode indicar fadiga do criativo.")
investimento_min_awareness = st.sidebar.number_input("💰 Investimento Mín. para Pausar (R$ - Awareness)", min_value=1.0, value=2.0, step=1.0,
                                         help="Valor gasto mínimo para que um anúncio de awareness/vídeo sem alcance significativo seja recomendado para 'Pausar'.")

# --- Parâmetros Gerais ---
st.sidebar.subheader("⚙️ Parâmetros Gerais")
valor_lead = st.sidebar.number_input("💎 Valor Estimado por Lead (R$)", min_value=10.0, value=100.0, step=10.0,
                                      help="O valor médio que cada lead representa em receita ou lucro para o seu negócio. Usado para calcular o Retorno sobre o Investimento (ROI).")

# --- Função de Classificação Aprimorada por Objetivo ---
def recomendar_acao(row):
    # Garante que os valores sejam numéricos; NaN se houver erro ou ausência.
    investimento = pd.to_numeric(row.get(COLUNAS['investimento']), errors='coerce') if pd.notna(row.get(COLUNAS['investimento'])) else 0.0
    frequencia = pd.to_numeric(row.get(COLUNAS['frequencia']), errors='coerce') if pd.notna(row.get(COLUNAS['frequencia'])) else 0.0
    objetivo = str(row.get(COLUNAS['objetivo'])).upper() if pd.notna(row.get(COLUNAS['objetivo'])) else 'OUTRO'

    acao = ''

    # --- Métricas Comuns ---
    cpm = pd.to_numeric(row.get(COLUNAS['cpm']), errors='coerce') if pd.notna(row.get(COLUNAS['cpm'])) else np.inf
    ctr_link = pd.to_numeric(row.get(COLUNAS['ctr_link']), errors='coerce') if pd.notna(row.get(COLUNAS['ctr_link'])) else 0.0

    # --- Lógica Baseada no Objetivo ---

    # 1. OBJETIVOS DE CONVERSÃO / GERAÇÃO DE LEADS (OUTCOME_ENGAGEMENT, OUTCOME_LEAD_GENERATION, OUTCOME_CONVERSIONS)
    if 'ENGAGEMENT' in objetivo or 'LEAD_GENERATION' in objetivo or 'CONVERSIONS' in objetivo:
        conversas = pd.to_numeric(row.get(COLUNAS['conversas']), errors='coerce') if pd.notna(row.get(COLUNAS['conversas'])) else 0.0
        cliques_link = pd.to_numeric(row.get(COLUNAS['cliques_link']), errors='coerce') if pd.notna(row.get(COLUNAS['cliques_link'])) else 0.0

        cpl_calc = investimento / conversas if conversas > 0 else np.inf
        taxa_conversao_clique_lead = (conversas / cliques_link * 100) if cliques_link > 0 else 0.0

        # Cenários sem leads
        if conversas == 0:
            if investimento >= investimento_min_leads:
                acao = "⛔ PAUSAR (Alto Gasto, Zero Leads)"
            else:
                acao = "⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)"
            return acao

        # Cenários com leads (análise de performance)
        if cpl_calc <= cpl_meta * cpl_mult_duplicar: # Se o CPL já é excelente (melhor que a meta de duplicação)
            if ctr_link >= ctr_meta * 0.9: # E o CTR Link também é bom
                acao = "📈 DUPLICAR (Performance Excelente - Conversão/Leads)"
            else: # O CPL é excelente, mas o CTR Link é baixo/ausente.
                acao = "📈 DUPLICAR (CPL Excelente, CTR Link Baixo/N/A - Conversão/Leads)"
            return acao
        elif cpl_calc > cpl_meta * cpl_mult_recriar:
            acao = "🔄 RECRIAR (CPL Inviável/Criativo Inadequado - Conversão)"
        elif frequencia >= freq_limite:
            acao = "🎨 NOVO CRIATIVO (Fadiga Detectada)"
        elif cpl_calc > cpl_meta * cpl_mult_duplicar and cpl_calc <= cpl_meta:
            # Se o CPL é bom (mas não excelente o suficiente para duplicar sem ressalvas)
            # E o CTR Link é baixo, ainda é uma otimização relevante
            if ctr_link < ctr_meta * 0.7: # CTR baixo indica problema de relevância do criativo para este objetivo
                acao = "🔧 OTIMIZAR (Relevância Criativo/CTR Baixo - Conversão/Tráfego)"
            elif cpm > cpm_meta_awareness * 1.2: # CPM alto para qualquer objetivo geralmente é ineficiente
                acao = "🔧 OTIMIZAR (Custo de Exibição Alto/CPM - Geral)"
            elif taxa_conversao_clique_lead < taxa_conversao_meta_pct:
                acao = "🔧 OTIMIZAR (Oferta/Funil Pós-Clique - Conversão)"
            else:
                acao = "🔧 OTIMIZAR (Ajustes Finas/Monitoramento - Geral)"
        else:
            acao = "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)" # Fallback para conversão

    # 2. OBJETIVOS DE TRÁFEGO (OUTCOME_TRAFFIC)
    elif 'TRAFFIC' in objetivo or 'LINK_CLICKS' in objetivo:
        cliques_link = pd.to_numeric(row.get(COLUNAS['cliques_link']), errors='coerce') if pd.notna(row.get(COLUNAS['cliques_link'])) else 0.0
        visualizacoes_pagina_destino = pd.to_numeric(row.get(COLUNAS['visualizacoes_pagina_destino']), errors='coerce') if pd.notna(row.get(COLUNAS['visualizacoes_pagina_destino'])) else 0.0
        
        cpc_link = investimento / cliques_link if cliques_link > 0 else np.inf

        # Cenários sem cliques no link
        if cliques_link == 0:
            if investimento >= investimento_min_trafego:
                acao = "⛔ PAUSAR (Alto Gasto, Sem Cliques no Link - Tráfego)"
            else:
                acao = "⏳ MANTER EM ANÁLISE (Baixo Gasto, Sem Cliques no Link - Tráfego)"
            return acao

        # Cenários com cliques
        if cpc_link <= cpc_meta_trafego * 0.7 and ctr_link >= ctr_meta_trafego * 1.2:
            acao = "📈 DUPLICAR (Performance Excelente - Tráfego)"
        elif cpc_link > cpc_meta_trafego * 1.5:
            acao = "🔄 RECRIAR (CPC Inviável/Criativo Inadequado - Tráfego)"
        elif frequencia >= freq_limite:
            acao = "🎨 NOVO CRIATIVO (Fadiga Detectada)"
        elif cpc_link > cpc_meta_trafego * 0.7 and cpc_link <= cpc_meta_trafego:
            if ctr_link < ctr_meta_trafego * 0.7:
                acao = "🔧 OTIMIZAR (Relevância Criativo/CTR Baixo - Conversão/Tráfego)"
            elif cpm > cpm_meta_awareness * 1.2:
                acao = "🔧 OTIMIZAR (Custo de Exibição Alto/CPM - Geral)"
            elif visualizacoes_pagina_destino == 0 and cliques_link > 0: # Clicou mas não chegou na página
                acao = "🔧 OTIMIZAR (Problema na Landing Page - Tráfego)"
            else:
                acao = "🔧 OTIMIZAR (Ajustes Finas/Monitoramento - Geral)"
        else:
            acao = "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)" # Fallback para tráfego

    # 3. OBJETIVOS DE AWARENESS / VIZUALIZAÇÃO DE VÍDEO (OUTCOME_AWARENESS, OUTCOME_VIDEO_VIEWS)
    elif 'AWARENESS' in objetivo or 'VIDEO_VIEWS' in objetivo:
        impressoes = pd.to_numeric(row.get(COLUNAS['impressoes']), errors='coerce') if pd.notna(row.get(COLUNAS['impressoes'])) else 0.0
        reproducoes_video_3s = pd.to_numeric(row.get(COLUNAS['reproducoes_video_3s']), errors='coerce') if pd.notna(row.get(COLUNAS['reproducoes_video_3s'])) else 0.0
        
        # Custo por reprodução de vídeo 3s
        cpv_3s = investimento / reproducoes_video_3s if reproducoes_video_3s > 0 else np.inf

        # Cenários de baixo alcance/impressões para o gasto
        if impressoes < 100 or (investimento >= investimento_min_awareness and impressoes == 0): # Se gastou e não imprimiu
            acao = "⛔ PAUSAR (Alto Gasto, Baixo Alcance/Impressões - Awareness)"
            return acao

        # Cenários de performance
        if cpm <= cpm_meta_awareness * 0.7 and frequencia <= freq_limite:
            acao = "📈 DUPLICAR (Performance Excelente - Awareness/Vídeo)"
        elif cpm > cpm_meta_awareness * 1.5:
            acao = "🔄 RECRIAR (CPM Inviável/Criativo Inadequado - Awareness)"
        elif frequencia >= freq_limite:
            acao = "🎨 NOVO CRIATIVO (Fadiga Detectada)"
        elif cpm > cpm_meta_awareness * 0.7 and cpm <= cpm_meta_awareness:
            if cpv_3s > cpv_3s_meta * 1.2: 
                acao = "🔧 OTIMIZAR (Qualidade do Vídeo/Custo - Awareness)"
            else:
                acao = "🔧 OTIMIZAR (Ajustes Finas/Monitoramento - Geral)"
        else:
            acao = "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)" # Fallback para awareness

    # 4. OUTROS OBJETIVOS / OBJETIVO DESCONHECIDO (fallback)
    else:
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

                # Mapeamento de colunas da planilha original para os nomes internos do COLUNAS
                # Adicionei os mappings para as novas colunas aqui
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
                    'Custo por conversa por mensagem iniciada': COLUNAS['custo_conversa'],
                    'Reproduções do vídeo por no mínimo 3 segundos': COLUNAS['reproducoes_video_3s'],
                    'Custo por reprodução de vídeo por no mínimo 3 segundos': COLUNAS['custo_reproducao_video_3s'],
                    'Visualizações da página de destino': COLUNAS['visualizacoes_pagina_destino'],
                    'Resultados': COLUNAS['resultados'], # Mapear se a planilha tiver essa coluna
                    'Custo por resultado': COLUNAS['custo_resultado'] # Mapear se a planilha tiver essa coluna
                })

                # Validar se as colunas essenciais para o dashboard existem no DF
                # A lista de colunas essenciais pode variar dependendo dos objetivos.
                # Para simplificar, vou manter as mais comuns, mas o código se adapta.
                colunas_essenciais_para_logica = [
                    COLUNAS['investimento'], COLUNAS['objetivo'], COLUNAS['campanha'],
                    COLUNAS['anuncio'], COLUNAS['frequencia'], COLUNAS['impressoes'],
                    COLUNAS['cliques_link'], COLUNAS['conversas'], COLUNAS['cpm'],
                    COLUNAS['ctr_link'], COLUNAS['reproducoes_video_3s'],
                    COLUNAS['visualizacoes_pagina_destino']
                ]

                # Verificar a presença de pelo menos uma das colunas chave para não dar erro
                # Se não tiver a coluna, ela será tratada como NaN/0 na função recomendar_acao
                missing_cols_input = [col_alias for col_key, col_alias in COLUNAS.items() if col_alias not in df_processed.columns]
                if len(missing_cols_input) > 0:
                    st.warning(f"⚠️ Algumas colunas esperadas não foram encontradas na sua planilha: **{', '.join(missing_cols_input)}**. A análise continuará, mas algumas métricas podem ser impactadas.")


                df = df_processed.copy()

                # Limpeza e preparação dos dados: converter para numérico e preencher NaNs
                numeric_columns_to_process = [
                    COLUNAS['investimento'], COLUNAS['conversas'], COLUNAS['alcance'],
                    COLUNAS['impressoes'], COLUNAS['frequencia'], COLUNAS['ctr_link'],
                    COLUNAS['cpm'], COLUNAS['cliques_link'], COLUNAS['cpc_link'], COLUNAS['cpc_todos'],
                    COLUNAS['reproducoes_video_3s'], COLUNAS['custo_reproducao_video_3s'],
                    COLUNAS['visualizacoes_pagina_destino'], COLUNAS['resultados'], COLUNAS['custo_resultado']
                ]
                for col in numeric_columns_to_process:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # Trata NaN e strings vazias como 0


                st.header("🔬 Criando Análises Avançadas...")
                with st.spinner("Processando análises estratégicas..."):
                    # 1. CPL Calculado (mantido, mas agora usado apenas para objetivos de conversão)
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

                    # 3. CPC Link Calculado (para objetivos de Tráfego)
                    df['cpc_link_calculado'] = np.where(
                        df[COLUNAS['cliques_link']] > 0,
                        df[COLUNAS['investimento']] / df[COLUNAS['cliques_link']],
                        np.inf
                    )

                    # 4. CPV 3s Calculado (Custo por Reprodução de Vídeo por no mínimo 3 segundos)
                    df['cpv_3s_calculado'] = np.where(
                        df[COLUNAS['reproducoes_video_3s']] > 0,
                        df[COLUNAS['investimento']] / df[COLUNAS['reproducoes_video_3s']],
                        np.inf
                    )

                    # Classifica a família de objetivos para melhor organização
                    def classificar_objetivo_familia(objetivo):
                        obj = str(objetivo).upper()
                        if 'ENGAGEMENT' in obj or 'LEAD_GENERATION' in obj or 'CONVERSIONS' in obj or 'PURCHASE' in obj:
                            return 'Conversão/Leads'
                        elif 'TRAFFIC' in obj or 'LINK_CLICKS' in obj or 'LANDING_PAGE_VIEWS' in obj:
                            return 'Tráfego'
                        elif 'AWARENESS' in obj or 'REACH' in obj or 'BRAND_AWARENESS' in obj or 'VIDEO_VIEWS' in obj:
                            return 'Awareness/Vídeo'
                        else:
                            return 'Outros'
                    df['classificacao_objetivo'] = df[COLUNAS['objetivo']].apply(classificar_objetivo_familia)


                    # Aplica a função de recomendação aprimorada e orientada por objetivo
                    df['recomendacao_acao'] = df.apply(recomendar_acao, axis=1)

                    # 5. Classificação de Performance (Ajustada para refletir a nova lógica)
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
                    
                    # 6. Status de Fadiga (Agora mais um indicador do que uma ação primária)
                    # Certifique-se que a coluna 'Frequência' existe e está numérica antes de usar
                    if COLUNAS['frequencia'] in df.columns:
                        df['status_fadiga'] = np.where(
                            df[COLUNAS['frequencia']] >= freq_limite,
                            '😴 Fadiga Detectada',
                            '✅ Saudável'
                        )
                    else:
                        df['status_fadiga'] = 'N/A' # Coluna 'Frequência' ausente

                    # 7. Prioridade de Ação (Ajustado para novas categorias)
                    prioridade_map = {
                        '⛔ PAUSAR (Alto Gasto, Zero Leads)': 'CRÍTICA',
                        '⏳ MANTER EM ANÁLISE (Baixo Gasto, Zero Leads)': 'BAIXA',
                        '📈 DUPLICAR (Performance Excelente - Conversão/Leads)': 'ALTA',
                        '📈 DUPLICAR (CPL Excelente, CTR Link Baixo/N/A - Conversão/Leads)': 'ALTA', # NOVA RECOMENDAÇÃO
                        '🎨 NOVO CRIATIVO (Fadiga Detectada)': 'MÉDIA',
                        '🔧 OTIMIZAR (Relevância Criativo/CTR Baixo - Conversão/Tráfego)': 'MÉDIA',
                        '🔧 OTIMIZAR (Custo de Exibição Alto/CPM - Geral)': 'MÉDIA',
                        '🔧 OTIMIZAR (Oferta/Funil Pós-Clique - Conversão)': 'MÉDIA',
                        '🔧 OTIMIZAR (Ajustes Finas/Monitoramento - Geral)': 'BAIXA',
                        '🔄 RECRIAR (CPL Inviável/Criativo Inadequado - Conversão)': 'CRÍTICA',
                        '🔄 RECRIAR (Métricas Fracas/Sem Direção - Conversão)': 'ALTA',
                        '💡 REAVALIAR ESTRATÉGIA (Outros Cenários)': 'MÉDIA',
                        # Novas prioridades
                        "⛔ PAUSAR (Alto Gasto, Sem Cliques no Link - Tráfego)": 'CRÍTICA',
                        "⏳ MANTER EM ANÁLISE (Baixo Gasto, Sem Cliques no Link - Tráfego)": 'BAIXA',
                        "⛔ PAUSAR (Alto Gasto, Baixo Alcance/Impressões - Awareness)": 'CRÍTICA',
                        "⏳ MANTER EM ANÁLISE (Baixo Gasto, Baixo Alcance/Impressões - Awareness)": 'BAIXA',
                        "📈 DUPLICAR (Performance Excelente - Tráfego)": 'ALTA',
                        "📈 DUPLICAR (Performance Excelente - Awareness/Vídeo)": 'ALTA',
                        "🔄 RECRIAR (CPC Inviável/Criativo Inadequado - Tráfego)": 'CRÍTICA',
                        "🔄 RECRIAR (Métricas Fracas/Sem Direção - Tráfego)": 'ALTA',
                        "🔄 RECRIAR (CPM Inviável/Criativo Inadequado - Awareness)": 'CRÍTICA',
                        "🔄 RECRIAR (Métricas Fracas/Sem Direção - Awareness)": 'ALTA',
                        "🔧 OTIMIZAR (Qualidade do Vídeo/Custo - Awareness)": 'MÉDIA',
                        "🔧 OTIMIZAR (Problema na Landing Page - Tráfego)": 'MÉDIA',
                    }
                    df['prioridade'] = df['recomendacao_acao'].map(prioridade_map).fillna('❓ DESCONHECIDA') # Fallback para novas ações

                    # 8. ROI Estimado (Mantido, relevante para qualquer investimento que gera valor por lead/conversa)
                    df['roi_estimado'] = np.where(
                        df[COLUNAS['investimento']] > 0,
                        ((df[COLUNAS['conversas']] * valor_lead) - df[COLUNAS['investimento']]) / df[COLUNAS['investimento']] * 100,
                        0
                    )

                    # 9. Score de Qualidade (Ajustado para considerar os novos KPIs)
                    def calcular_score_qualidade(row):
                        score = 0
                        objetivo_familia = row['classificacao_objetivo']
                        
                        # Atribuir freq_actual no início da função
                        freq_actual = pd.to_numeric(row.get(COLUNAS['frequencia']), errors='coerce') if pd.notna(row.get(COLUNAS['frequencia'])) else 0.0

                        # Pontuação baseada no objetivo principal
                        if objetivo_familia == 'Conversão/Leads':
                            # CPL (40 pontos) - prioridade máxima para a métrica de resultado
                            if row[COLUNAS['conversas']] > 0:
                                if row['cpl_calculado'] <= cpl_meta * 0.7: score += 40
                                elif row['cpl_calculado'] <= cpl_meta: score += 30
                                elif row['cpl_calculado'] <= cpl_meta * 1.5: score += 15
                            else: # Se não há leads, o CPL é infinito, penaliza
                                score += 0
                            
                            # CTR Link (25 pontos) - relevante para o criativo
                            if row[COLUNAS['ctr_link']] >= ctr_meta * 1.5: score += 25
                            elif row[COLUNAS['ctr_link']] >= ctr_meta: score += 15
                            elif row[COLUNAS['ctr_link']] >= ctr_meta * 0.5: score += 5

                            # Conversões (15 pontos) - volume de conversão
                            if row[COLUNAS['conversas']] >= 3: score += 15
                            elif row[COLUNAS['conversas']] >= 1: score += 10

                        elif objetivo_familia == 'Tráfego':
                            # CPC Link (40 pontos)
                            if row['cpc_link_calculado'] <= cpc_meta_trafego * 0.7: score += 40
                            elif row['cpc_link_calculado'] <= cpc_meta_trafego: score += 30
                            elif row['cpc_link_calculado'] <= cpc_meta_trafego * 1.5: score += 15
                            # CTR Link (30 pontos)
                            if row[COLUNAS['ctr_link']] >= ctr_meta_trafego * 1.5: score += 30
                            elif row[COLUNAS['ctr_link']] >= ctr_meta_trafego: score += 20
                            elif row[COLUNAS['ctr_link']] >= ctr_meta_trafego * 0.5: score += 10
                            # Visualizações de Página de Destino (15 pontos)
                            if row[COLUNAS['visualizacoes_pagina_destino']] >= 3: score += 15
                            elif row[COLUNAS['visualizacoes_pagina_destino']] >= 1: score += 10

                        elif objetivo_familia == 'Awareness/Vídeo':
                            # CPM (40 pontos)
                            if row[COLUNAS['cpm']] <= cpm_meta_awareness * 0.7: score += 40
                            elif row[COLUNAS['cpm']] <= cpm_meta_awareness: score += 30
                            elif row[COLUNAS['cpm']] <= cpm_meta_awareness * 1.5: score += 15
                            # CPV 3s (30 pontos) - se disponível e relevante
                            if row[COLUNAS['reproducoes_video_3s']] > 0:
                                if row['cpv_3s_calculado'] <= cpv_3s_meta * 0.7: score += 30
                                elif row['cpv_3s_calculado'] <= cpv_3s_meta: score += 20
                                elif row['cpv_3s_calculado'] <= cpv_3s_meta * 1.5: score += 10
                            # Alcance / Impressões (15 pontos)
                            if row[COLUNAS['impressoes']] >= 1000: score += 15 # Valor arbitrário para "bom volume"
                            elif row[COLUNAS['impressoes']] >= 300: score += 10

                        # Frequência (Restantes pontos - geral para todos os objetivos, distribuído entre os 100 pontos)
                        # Garante que a frequência não some mais que os pontos totais restantes
                        remaining_points = max(0, 100 - score) 
                        if remaining_points > 0:
                            if freq_actual <= freq_limite * 0.7: score += remaining_points # Excelente
                            elif freq_actual <= freq_limite: score += (remaining_points * 0.75) # Bom
                            elif freq_actual <= freq_limite * 1.3: score += (remaining_points * 0.25) # Atenção

                        return min(int(score), 100) # Garante que o score não ultrapasse 100

                    df['score_qualidade'] = df.apply(calcular_score_qualidade, axis=1)

                    # 10. Categoria de Anúncio - Mantido
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

    # Métricas principais (adaptadas para exibir métricas relevantes para todos os objetivos)
    col1, col2, col3, col4, col5 = st.columns(5)
    total_investido = df[COLUNAS['investimento']].sum()
    total_leads = df[COLUNAS['conversas']].sum()
    total_cliques_link = df[COLUNAS['cliques_link']].sum()
    total_impressoes = df[COLUNAS['impressoes']].sum()
    total_reproducoes_video_3s = df[COLUNAS['reproducoes_video_3s']].sum()

    cpl_medio_geral = total_investido / total_leads if total_leads > 0 else 0
    cpc_link_medio_geral = total_investido / total_cliques_link if total_cliques_link > 0 else 0
    cpm_medio_geral = total_investido / total_impressoes * 1000 if total_impressoes > 0 else 0
    cpv_3s_medio_geral = total_investido / total_reproducoes_video_3s if total_reproducoes_video_3s > 0 else 0

    col1.metric("💰 Investimento Total", f"R$ {total_investido:,.2f}")
    col2.metric("🎯 Total de Leads", f"{int(total_leads)}")
    col3.metric("🔗 Total de Cliques no Link", f"{int(total_cliques_link)}")
    col4.metric("👁️ Impressões Totais", f"{int(total_impressoes):,.0f}")
    col5.metric("▶️ Reprod. Vídeo (3s) Totais", f"{int(total_reproducoes_video_3s):,.0f}")

    col_metrics_extra1, col_metrics_extra2, col_metrics_extra3, col_metrics_extra4, col_metrics_extra5 = st.columns(5)
    col_metrics_extra1.metric("📈 CPL Médio (Geral)", f"R$ {cpl_medio_geral:,.2f}")
    col_metrics_extra2.metric("💲 CPC Link Médio (Geral)", f"R$ {cpc_link_medio_geral:,.2f}")
    col_metrics_extra3.metric("💸 CPM Médio (Geral)", f"R$ {cpm_medio_geral:,.2f}")
    col_metrics_extra4.metric("🎥 CPV 3s Médio (Geral)", f"R$ {cpv_3s_medio_geral:,.2f}")
    col_metrics_extra5.metric("⚡ CTR Link Médio (Geral)", f"{df[COLUNAS['ctr_link']].mean():.2f}%")


    # Distribuição de ações recomendadas (MANTIDO)
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
        prioridade_order = ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA', '❓ DESCONHECIDA']
        # Reindexar para garantir a ordem e incluir prioridades que podem ter 0 anúncios
        prioridade_counts = prioridade_counts.reindex(prioridade_order, fill_value=0)

        fig_priority, ax_priority = plt.subplots(figsize=(8, 6)) # Aumenta o tamanho
        # Cores para as prioridades (distintas do gráfico de ações)
        priority_colors = {
            'CRÍTICA': '#DC3545', # Vermelho forte
            'ALTA': '#FD7E14',    # Laranja
            'MÉDIA': '#FFC107',   # Amarelo
            'BAIXA': '#28A745',   # Verde
            '❓ DESCONHECIDA': '#A9A9A9'
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

    # Análise por categoria de objetivo
    st.subheader("📊 Performance por Tipo de Objetivo")
    objetivo_stats = df.groupby('classificacao_objetivo').agg(
        investimento=(COLUNAS['investimento'], 'sum'),
        conversas=(COLUNAS['conversas'], 'sum'),
        cliques_link=(COLUNAS['cliques_link'], 'sum'),
        impressoes=(COLUNAS['impressoes'], 'sum'),
        score_qualidade=('score_qualidade', 'mean')
    ).reset_index()

    objetivo_stats['cpl_categoria_objetivo'] = np.where(
        objetivo_stats['conversas'] > 0,
        objetivo_stats['investimento'] / objetivo_stats['conversas'],
        np.inf
    )
    objetivo_stats['cpc_link_categoria_objetivo'] = np.where(
        objetivo_stats['cliques_link'] > 0,
        objetivo_stats['investimento'] / objetivo_stats['cliques_link'],
        np.inf
    )
    objetivo_stats['cpm_categoria_objetivo'] = np.where(
        objetivo_stats['impressoes'] > 0,
        objetivo_stats['investimento'] / objetivo_stats['impressoes'] * 1000,
        np.inf
    )

    st.dataframe(objetivo_stats.style.format({
        'investimento': 'R$ {:.2f}',
        'cpl_categoria_objetivo': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpc_link_categoria_objetivo': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpm_categoria_objetivo': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'score_qualidade': '{:.1f}',
        'impressoes': '{:,.0f}',
        'conversas': '{:,.0f}',
        'cliques_link': '{:,.0f}'
    }))

    # --- Performance por Categoria de Anúncio ---
    st.subheader("📊 Performance por Categoria de Anúncio")
    st.markdown("Veja o desempenho consolidado dos seus anúncios por categoria.")

    categoria_anuncio_stats = df.groupby('categoria_anuncio').agg(
        investimento=(COLUNAS['investimento'], 'sum'),
        conversas=(COLUNAS['conversas'], 'sum'),
        cliques_link=(COLUNAS['cliques_link'], 'sum'),
        impressoes=(COLUNAS['impressoes'], 'sum'),
        reproducoes_video_3s=(COLUNAS['reproducoes_video_3s'], 'sum'),
        visualizacoes_pagina_destino=(COLUNAS['visualizacoes_pagina_destino'], 'sum'),
        score_qualidade=('score_qualidade', 'mean'),
        frequencia_media=(COLUNAS['frequencia'], 'mean'),
        ctr_link_medio=(COLUNAS['ctr_link'], 'mean'),
        roi_estimado_medio=('roi_estimado', 'mean')
    ).reset_index()

    # Cálculos de custos médios por categoria de anúncio
    categoria_anuncio_stats['cpl_medio'] = np.where(
        categoria_anuncio_stats['conversas'] > 0,
        categoria_anuncio_stats['investimento'] / categoria_anuncio_stats['conversas'],
        np.inf
    )
    categoria_anuncio_stats['cpc_link_medio'] = np.where(
        categoria_anuncio_stats['cliques_link'] > 0,
        categoria_anuncio_stats['investimento'] / categoria_anuncio_stats['cliques_link'],
        np.inf
    )
    categoria_anuncio_stats['cpm_medio'] = np.where(
        categoria_anuncio_stats['impressoes'] > 0,
        categoria_anuncio_stats['investimento'] / categoria_anuncio_stats['impressoes'] * 1000,
        np.inf
    )
    categoria_anuncio_stats['cpv_3s_medio'] = np.where(
        categoria_anuncio_stats['reproducoes_video_3s'] > 0,
        categoria_anuncio_stats['investimento'] / categoria_anuncio_stats['reproducoes_video_3s'],
        np.inf
    )

    st.dataframe(categoria_anuncio_stats.style.format({
        'investimento': 'R$ {:.2f}',
        'conversas': '{:,.0f}',
        'cliques_link': '{:,.0f}',
        'impressoes': '{:,.0f}',
        'reproducoes_video_3s': '{:,.0f}',
        'visualizacoes_pagina_destino': '{:,.0f}',
        'cpl_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpc_link_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpm_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpv_3s_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'score_qualidade': '{:.1f}',
        'frequencia_media': '{:.2f}',
        'ctr_link_medio': '{:.2f}%',
        'roi_estimado_medio': '{:.1f}%'
    }))

    # --- Performance por Posicionamento ---
    st.subheader("📱 Performance por Posicionamento")
    st.markdown("Analise o desempenho das suas campanhas por posicionamento.")

    posicionamento_stats = df.groupby('categoria_posicionamento').agg(
        investimento=(COLUNAS['investimento'], 'sum'),
        conversas=(COLUNAS['conversas'], 'sum'),
        cliques_link=(COLUNAS['cliques_link'], 'sum'),
        impressoes=(COLUNAS['impressoes'], 'sum'),
        reproducoes_video_3s=(COLUNAS['reproducoes_video_3s'], 'sum'),
        visualizacoes_pagina_destino=(COLUNAS['visualizacoes_pagina_destino'], 'sum'),
        score_qualidade=('score_qualidade', 'mean'),
        frequencia_media=(COLUNAS['frequencia'], 'mean'),
        ctr_link_medio=(COLUNAS['ctr_link'], 'mean'),
        roi_estimado_medio=('roi_estimado', 'mean')
    ).reset_index()

    # Cálculos de custos médios por posicionamento
    posicionamento_stats['cpl_medio'] = np.where(
        posicionamento_stats['conversas'] > 0,
        posicionamento_stats['investimento'] / posicionamento_stats['conversas'],
        np.inf
    )
    posicionamento_stats['cpc_link_medio'] = np.where(
        posicionamento_stats['cliques_link'] > 0,
        posicionamento_stats['investimento'] / posicionamento_stats['cliques_link'],
        np.inf
    )
    posicionamento_stats['cpm_medio'] = np.where(
        posicionamento_stats['impressoes'] > 0,
        posicionamento_stats['investimento'] / posicionamento_stats['impressoes'] * 1000,
        np.inf
    )
    posicionamento_stats['cpv_3s_medio'] = np.where(
        posicionamento_stats['reproducoes_video_3s'] > 0,
        posicionamento_stats['investimento'] / posicionamento_stats['reproducoes_video_3s'],
        np.inf
    )

    st.dataframe(posicionamento_stats.style.format({
        'investimento': 'R$ {:.2f}',
        'conversas': '{:,.0f}',
        'cliques_link': '{:,.0f}',
        'impressoes': '{:,.0f}',
        'reproducoes_video_3s': '{:,.0f}',
        'visualizacoes_pagina_destino': '{:,.0f}',
        'cpl_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpc_link_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpm_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'cpv_3s_medio': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
        'score_qualidade': '{:.1f}',
        'frequencia_media': '{:.2f}',
        'ctr_link_medio': '{:.2f}%',
        'roi_estimado_medio': '{:.1f}%'
    }))

    # Análise por categoria de anúncio (MANTIDO)
    st.subheader("🏆 Top 5 Performers por Categoria de Anúncio")

    for categoria in df['categoria_anuncio'].unique():
        if pd.notna(categoria):
            st.write(f"### {categoria}")
            df_categoria = df[df['categoria_anuncio'] == categoria]
            # Filtrar por anúncios que geraram resultados e ordenar pela métrica mais relevante ao objetivo
            
            # Escolher a métrica para ordenar com base na maioria dos objetivos ou uma métrica geral
            # Para fins de demonstração, manterei score_qualidade como padrão para ordem decrescente
            df_top = df_categoria.sort_values(by='score_qualidade', ascending=False).head(5)

            if not df_top.empty:
                cols_display = [
                    COLUNAS['anuncio'],
                    COLUNAS['investimento'],
                    COLUNAS['conversas'],
                    COLUNAS['cliques_link'],
                    COLUNAS['impressoes'],
                    'cpl_calculado',
                    'cpc_link_calculado',
                    'cpv_3s_calculado',
                    'score_qualidade',
                    'recomendacao_acao',
                    'prioridade'
                ]
                st.dataframe(df_top[cols_display].style.format({
                    COLUNAS['investimento']: 'R$ {:.2f}',
                    'cpl_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
                    'cpc_link_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
                    'cpv_3s_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
                    'score_qualidade': '{:.0f}',
                    COLUNAS['conversas']: '{:,.0f}',
                    COLUNAS['cliques_link']: '{:,.0f}',
                    COLUNAS['impressoes']: '{:,.0f}'
                }))
            else:
                st.info(f"Nenhum anúncio com desempenho relevante encontrado para {categoria}")

    # Análise temporal (MANTIDO)
    if COLUNAS['dia'] in df.columns:
        st.subheader("📅 Análise de Tendência por Dia")
        df[COLUNAS['dia']] = pd.to_datetime(df[COLUNAS['dia']], errors='coerce')
        df_temporal = df.groupby(COLUNAS['dia']).agg(
            investimento=(COLUNAS['investimento'], 'sum'),
            conversas=(COLUNAS['conversas'], 'sum'),
            cliques_link=(COLUNAS['cliques_link'], 'sum')
        ).reset_index()

        df_temporal['cpl_diario'] = np.where(
            df_temporal['conversas'] > 0,
            df_temporal['investimento'] / df_temporal['conversas'],
            np.nan
        )
        df_temporal['cpc_link_diario'] = np.where(
            df_temporal['cliques_link'] > 0,
            df_temporal['investimento'] / df_temporal['cliques_link'],
            np.nan
        )


        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15)) # 3 gráficos

        # Investimento e leads por dia
        ax1.plot(df_temporal[COLUNAS['dia']], df_temporal['investimento'], label='Investimento', color='blue')
        ax1_twin = ax1.twinx()
        ax1_twin.plot(df_temporal[COLUNAS['dia']], df_temporal['conversas'],
                     label='Leads', color='green', linestyle='--')
        ax1.set_ylabel('Investimento (R$)', color='blue')
        ax1_twin.set_ylabel('Leads', color='green')
        ax1.set_title('Investimento e Leads por Dia')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend(loc="upper left")
        ax1_twin.legend(loc="upper right")

        # CPL por dia
        ax2.plot(df_temporal[COLUNAS['dia']], df_temporal['cpl_diario'], color='red', marker='o')
        ax2.set_ylabel('CPL (R$)')
        ax2.set_title('CPL por Dia')
        ax2.axhline(y=cpl_meta, color='orange', linestyle='--', label=f'Meta CPL (R$ {cpl_meta})')
        ax2.legend()
        ax2.grid(True)
        ax2.tick_params(axis='x', rotation=45)

        # CPC Link por dia
        ax3.plot(df_temporal[COLUNAS['dia']], df_temporal['cpc_link_diario'], color='purple', marker='x')
        ax3.set_ylabel('CPC Link (R$)')
        ax3.set_title('CPC Link por Dia')
        ax3.axhline(y=cpc_meta_trafego, color='brown', linestyle=':', label=f'Meta CPC Tráfego (R$ {cpc_meta_trafego})')
        ax3.legend()
        ax3.grid(True)
        ax3.tick_params(axis='x', rotation=45)


        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.warning("⚠️ Coluna 'Dia' não encontrada. Exporte seu relatório do Meta Ads com a opção 'Quebrar por Dia' para ativar esta análise de tendência.")

    # Tabela completa com filtros
    st.subheader("📋 Análise Detalhada com Filtros")

    # Filtros
    col1, col2, col3, col4, col5 = st.columns(5) # Adicionado um filtro
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
    with col5: # Novo filtro
        objetivos_familias = ['Todas'] + list(df['classificacao_objetivo'].unique())
        objetivo_familia_selecionada = st.selectbox("Família de Objetivo", objetivos_familias)

    # Aplicar filtros
    df_filtered = df.copy()
    if campanha_selecionada != 'Todas': df_filtered = df_filtered[df_filtered[COLUNAS['campanha']] == campanha_selecionada]
    if acao_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['recomendacao_acao'] == acao_selecionada]
    if categoria_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['categoria_anuncio'] == categoria_selecionada]
    if prioridade_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['prioridade'] == prioridade_selecionada]
    if objetivo_familia_selecionada != 'Todas': df_filtered = df_filtered[df_filtered['classificacao_objetivo'] == objetivo_familia_selecionada]


    # Colunas para exibição (EXPANDIDO)
    colunas_exibicao = [
        COLUNAS['campanha'], COLUNAS['anuncio'], COLUNAS['objetivo'], 'classificacao_objetivo', 'categoria_anuncio',
        'categoria_posicionamento', COLUNAS['investimento'], COLUNAS['conversas'], COLUNAS['cliques_link'],
        COLUNAS['impressoes'], COLUNAS['alcance'], COLUNAS['frequencia'],
        COLUNAS['reproducoes_video_3s'], COLUNAS['visualizacoes_pagina_destino'],
        'cpl_calculado', 'cpc_link_calculado', 'cpv_3s_calculado', COLUNAS['cpm'], COLUNAS['ctr_link'],
        'taxa_conversao', 'classificacao_performance', 'recomendacao_acao',
        'prioridade', 'score_qualidade', 'roi_estimado', 'status_fadiga'
    ]
    
    # Filtra apenas as colunas que existem no DataFrame para evitar KeyError
    colunas_exibicao_final = [col for col in colunas_exibicao if col in df_filtered.columns]

    st.dataframe(
        df_filtered[colunas_exibicao_final].style.format({
            COLUNAS['investimento']: 'R$ {:.2f}',
            'cpl_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
            'cpc_link_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
            'cpv_3s_calculado': lambda x: 'R$ {:.2f}'.format(x) if x != np.inf else 'N/A',
            COLUNAS['cpm']: 'R$ {:.2f}',
            COLUNAS['conversas']: '{:,.0f}',
            COLUNAS['cliques_link']: '{:,.0f}',
            COLUNAS['impressoes']: '{:,.0f}',
            COLUNAS['alcance']: '{:,.0f}',
            COLUNAS['reproducoes_video_3s']: '{:,.0f}',
            COLUNAS['visualizacoes_pagina_destino']: '{:,.0f}',
            'score_qualidade': '{:.0f}',
            'roi_estimado': '{:.1f}%',
            'taxa_conversao': '{:.2f}%',
            COLUNAS['ctr_link']: '{:.2f}%',
            COLUNAS['frequencia']: '{:.2f}',
            'status_fadiga': '{}' # Adicionado formato para nova coluna, se existir
        }),
        use_container_width=True
    )

    # Download da planilha analisada (MANTIDO)
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
        file_name=f"analise_meta_ads_orientada_objetivo_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Resumo executivo (EXPANDIDO)
    st.header("📋 Resumo Executivo")

    # Contagens por ação
    acao_counts_resumo = df['recomendacao_acao'].value_counts()
    
    # Cálculo da economia potencial
    economia_potencial = df[df['recomendacao_acao'].str.contains('⛔ PAUSAR')][COLUNAS['investimento']].sum()

    st.markdown(f"""
    ### 🎯 **Ações Prioritárias Detalhadas (por Categoria):**
    """)
    
    # Gerar a seção de prioridades dinamicamente com base nas contagens
    priority_order = ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA', '❓ DESCONHECIDA']
    for priority in priority_order:
        # Filtrar as ações que pertencem a esta prioridade e que realmente apareceram nos dados
        actions_in_priority = [action for action, count in acao_counts_resumo.items() if prioridade_map.get(action) == priority and count > 0]
        
        if actions_in_priority:
            st.markdown(f"**{'🚨' if priority == 'CRÍTICA' else '📈' if priority == 'ALTA' else '🔧' if priority == 'MÉDIA' else '⏳' if priority == 'BAIXA' else '❓'} {priority}**")
            for action_label in actions_in_priority:
                count = acao_counts_resumo[action_label]
                st.markdown(f"*   **{action_label}: {count} anúncios**")
                st.markdown(f"> {INSIGHTS_APRIMORADOS.get(action_label, 'Descrição não disponível.')}")
            st.markdown("---")

    st.markdown(f"""
    ### 💡 **Principais Insights Globais:**
    
    1.  **CPL (Custo por Lead/Conversa) Médio Atual:** R$ {cpl_medio_geral:.2f} (Meta Conversão: R$ {cpl_meta:.2f}) - {('Atingido' if cpl_medio_geral <= cpl_meta else 'Acima da Meta')}
    2.  **CPC Link (Custo por Clique no Link) Médio Atual:** R$ {cpc_link_medio_geral:.2f} (Meta Tráfego: R$ {cpc_meta_trafego:.2f}) - {('Atingido' if cpc_link_medio_geral <= cpc_meta_trafego else 'Acima da Meta')}
    3.  **CPM (Custo por Mil Impressões) Médio Atual:** R$ {cpm_medio_geral:.2f} (Meta Awareness: R$ {cpm_meta_awareness:.2f}) - {('Atingido' if cpm_medio_geral <= cpm_meta_awareness else 'Acima da Meta')}
    4.  **Taxa de Conversão (Cliques -> Leads):** {df['taxa_conversao'].mean():.2f}% - Média geral da eficiência do funil pós-clique para leads.
    5.  **Economia Potencial (Pausando Ineficientes):** R$ {economia_potencial:.2f} - Valor que pode ser realocado imediatamente para anúncios de melhor performance.
    6.  **ROI (Retorno sobre o Investimento) Médio (Estimado):** {df['roi_estimado'].mean():.1f}% - Retorno potencial geral da conta com base no valor de um lead.
    7.  **Score Médio de Qualidade:** {df['score_qualidade'].mean():.1f}/100 - Avaliação sintética da saúde geral dos anúncios, ponderada por objetivo.

    ---

    ### 🚀 **Próximos Passos Recomendados:**
    
    1.  **Priorize as Ações CRÍTICAS:** Focar em anúncios classificados como "⛔ PAUSAR" ou "🔄 RECRIAR" com prioridade CRÍTICA. Estes representam o maior desperdício de orçamento ou ineficiência fundamental para o objetivo.
    2.  **Acelerar Crescimento:** Duplicar e escalar anúncios classificados como "📈 DUPLICAR (Performance Excelente)" em todas as famílias de objetivos, incluindo a nova categoria de CPL excelente mesmo com CTR Link baixo/N/A.
    3.  **Renovação e Ajuste:** Criar novos criativos para anúncios com "🎨 NOVO CRIATIVO (Fadiga Detectada)". Otimizar anúncios "🔧 OTIMIZAR (...)" com base nos diagnósticos detalhados para cada objetivo.
    4.  **Revisão Estratégica Profunda:** Avaliar profundamente os anúncios em "🔄 RECRIAR (Métricas Fracas/Sem Direção)" e "💡 REAVALIAR ESTRATÉGIA (Outros Cenários)" para entender falhas e planejar novos testes com abordagens diferentes.
    5.  **Realocação de Orçamento:** Transferir o orçamento economizado dos anúncios de baixo desempenho para anúncios de alta performance e para novos testes estratégicos.
    6.  **Monitoramento Contínuo:** Utilize os filtros da 'Análise Detalhada' para acompanhar anúncios com prioridade BAIXA e aqueles que foram 'Mantidos em Análise'.
    """)