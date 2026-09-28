# -*- coding: utf-8 -*-
"""
FG/A · Maturidade de Segurança da Informação — Rumo ao IG1 (CIS Controls v8)
Apresentação executiva para a diretoria.

Como rodar:
    pip install streamlit plotly
    streamlit run app_maturidade_fga.py

Estética baseada no Manual de Marca FG/A (paleta sage/verde + neutros quentes,
cinza-escuro #58595B para texto, tipografia geométrica).
"""

import streamlit as st
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# PALETA DE MARCA (Manual de Uso de Marca FG/A)
# ----------------------------------------------------------------------------
INK          = "#58595B"   # cinza-escuro — texto principal
INK_SOFT     = "#808184"   # texto secundário
SAGE         = "#899C92"   # verde-sage principal
SAGE_DEEP    = "#5C7350"   # verde profundo
GREEN_DEEP   = "#3D5233"   # verde escuro (títulos de destaque)
SAGE_LIGHT   = "#C1C7BD"   # sage claro
BEIGE        = "#CDCBBD"   # bege/tan
GREEN_MID    = "#809973"
GREEN_SOFT   = "#A6BFA6"
PAPER        = "#FFFFFF"
PAPER_ALT    = "#F5F4EF"   # neutro quente muito claro
LINE         = "#E3E1D8"

# Cores de risco — uso exclusivo em gráficos/indicadores (permitido pelo manual).
# Escolhidas para harmonizar com os neutros quentes da marca.
RISK_HIGH = "#A65A4A"   # terracota discreta
RISK_MED  = "#C29A4A"   # ocre quente
RISK_LOW  = SAGE_DEEP   # verde da marca = "bom"
RISK_NA   = SAGE_LIGHT  # neutro

# ----------------------------------------------------------------------------
# CONFIG DA PÁGINA + CSS
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="FG/A · Maturidade de Segurança — Rumo ao IG1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {{ font-family: 'Poppins', -apple-system, sans-serif; }}
    .stApp {{ background: {PAPER}; }}
    section[data-testid="stSidebar"] {{ background: {PAPER_ALT}; border-right: 1px solid {LINE}; }}
    h1, h2, h3 {{ color: {INK}; font-family: 'Poppins', sans-serif; font-weight: 600; letter-spacing: -0.01em; }}
    p, li, .stMarkdown {{ color: {INK}; }}

    .script {{ font-family: 'Caveat', cursive; color: {SAGE_DEEP}; line-height: 1; }}
    .eyebrow {{ color: {SAGE}; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }}
    .lede {{ color: {INK_SOFT}; font-size: 1.02rem; max-width: 60ch; }}

    /* cartões */
    .card {{ background: {PAPER}; border: 1px solid {LINE}; border-radius: 10px;
             padding: 18px 20px; height: 100%; }}
    .card-good {{ border-left: 4px solid {SAGE_DEEP}; }}
    .card-bad  {{ border-left: 4px solid {RISK_HIGH}; }}
    .card-warn {{ border-left: 4px solid {RISK_MED}; }}
    .card h4 {{ margin: 0 0 6px 0; font-size: 1.0rem; color: {INK}; font-weight: 600; }}
    .card p  {{ margin: 0; font-size: 0.86rem; color: {INK_SOFT}; line-height: 1.5; }}

    .pill {{ display:inline-block; padding: 3px 12px; border-radius: 100px;
             font-size: 0.72rem; font-weight: 600; }}
    .pill-hi {{ background:#F1E1DD; color:{RISK_HIGH}; }}
    .pill-md {{ background:#F3E9D3; color:#8A6A22; }}
    .pill-lo {{ background:#E4EBE2; color:{SAGE_DEEP}; }}

    .big-stat {{ font-size: 3.2rem; font-weight: 700; color: {SAGE_DEEP}; line-height: 1; }}
    .stat-label {{ color: {INK_SOFT}; font-size: 0.9rem; }}

    .divider {{ height:1px; background:{LINE}; border:none; margin: 1.4rem 0; }}
    hr {{ border-color: {LINE}; }}
    .stApp footer {{ visibility: hidden; }}
    #MainMenu {{ visibility: hidden; }}

    /* barra de milestones */
    .ms {{ background:{PAPER}; border:1px solid {LINE}; border-top:4px solid {SAGE}; border-radius:10px; padding:16px 18px; height:100%; }}
    .ms .n {{ display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; border-radius:50%;
              background:{INK}; color:#fff; font-weight:700; font-size:0.9rem; margin-bottom:10px; }}
    .ms h4 {{ margin:4px 0 8px 0; color:{INK}; font-size:1.02rem; }}
    .ms ul {{ margin:0; padding-left:18px; }}
    .ms li {{ font-size:0.82rem; color:{INK_SOFT}; margin-bottom:5px; }}
</style>
""", unsafe_allow_html=True)

# marca de topo (wordmark FG/A com "/" em sage, conforme manual)
LOGO_HTML = f"""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
  <svg width="34" height="34" viewBox="0 0 100 100">
     <path d="M20 78 C20 50 34 30 50 22 L50 78 Z" fill="{SAGE_LIGHT}"/>
     <path d="M50 78 C50 46 62 28 80 22 C74 52 64 70 50 78 Z" fill="{BEIGE}"/>
     <path d="M20 78 C34 66 44 62 80 62 L80 78 Z" fill="{SAGE_DEEP}" opacity="0.75"/>
  </svg>
  <span style="font-family:'Poppins'; font-weight:700; font-size:1.3rem; color:{INK};">FG<span style="color:{SAGE}">/</span>A</span>
</div>
"""

# ----------------------------------------------------------------------------
# DADOS (derivados da Matriz de Segurança — Evidências de Gaps, L&L Solutions)
# ----------------------------------------------------------------------------
NOTA_ATUAL = 53.1
NOTA_META  = 80.0

RISCO = {"Alto": 8, "Moderado": 5, "Baixo": 4, "Não avaliado": 1}
ESFORCO = {"Já prontos": 11, "A formalizar": 18, "Do zero": 21}
IG = {"IG1": 56, "IG2 (+74)": 74, "IG3 (+23)": 23}

# ----------------------------------------------------------------------------
# GRÁFICOS
# ----------------------------------------------------------------------------
def fig_gauge():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=NOTA_ATUAL,
        number={"suffix": "%", "font": {"size": 46, "color": INK, "family": "Poppins"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": INK_SOFT, "tickfont": {"size": 11}},
            "bar": {"color": SAGE_DEEP, "thickness": 0.28},
            "bgcolor": PAPER_ALT,
            "borderwidth": 0,
            "steps": [
                {"range": [0, NOTA_ATUAL], "color": SAGE_LIGHT},
            ],
            "threshold": {"line": {"color": RISK_MED, "width": 4}, "thickness": 0.85, "value": NOTA_META},
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=10, b=0),
                      paper_bgcolor="rgba(0,0,0,0)", font={"color": INK})
    return fig

def fig_risco():
    labels = list(RISCO.keys())[::-1]
    values = list(RISCO.values())[::-1]
    colors = [RISK_NA, RISK_LOW, RISK_MED, RISK_HIGH]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors, text=values, textposition="outside",
        textfont={"size": 15, "color": INK, "family": "Poppins"},
    ))
    fig.update_layout(
        height=280, margin=dict(l=10, r=30, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 9.5]),
        yaxis=dict(showgrid=False, tickfont={"size": 13, "color": INK}),
        font={"color": INK},
    )
    return fig

def fig_esforco():
    labels = list(ESFORCO.keys())
    values = list(ESFORCO.values())
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=[RISK_LOW, RISK_MED, RISK_HIGH], line=dict(color=PAPER, width=3)),
        textinfo="value", textfont={"size": 16, "color": "#fff", "family": "Poppins"},
        sort=False,
    ))
    fig.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0.5, xanchor="center",
                    font={"size": 12, "color": INK}),
        annotations=[dict(text="50<br><span style='font-size:12px'>mapeados</span>",
                          x=0.5, y=0.5, font_size=24, font_color=INK, showarrow=False, font_family="Poppins")],
    )
    return fig

def fig_ig():
    fig = go.Figure()
    order = ["IG1", "IG2 (+74)", "IG3 (+23)"]
    colors = [SAGE_DEEP, BEIGE, SAGE_LIGHT]
    for name, col in zip(order, colors):
        fig.add_bar(y=["Safeguards"], x=[IG[name]], name=name, orientation="h",
                    marker_color=col, text=[f"{name} · {IG[name]}"], textposition="inside",
                    insidetextanchor="middle",
                    textfont={"color": "#fff" if name == "IG1" else INK, "size": 13, "family": "Poppins"})
    fig.update_layout(
        barmode="stack", height=130, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        showlegend=False, font={"color": INK},
    )
    return fig

def fig_progress():
    fig = go.Figure()
    fig.add_bar(x=[NOTA_ATUAL], y=["Nota"], orientation="h", marker_color=SAGE_DEEP, width=0.5,
                text=[f"{NOTA_ATUAL}%"], textposition="inside", insidetextanchor="end",
                textfont={"color": "#fff", "size": 14, "family": "Poppins"})
    fig.add_shape(type="line", x0=NOTA_META, x1=NOTA_META, y0=-0.5, y1=0.5,
                  line=dict(color=RISK_MED, width=3, dash="dot"))
    fig.add_annotation(x=NOTA_META, y=0.55, text=f"meta ~{int(NOTA_META)}%",
                       showarrow=False, font=dict(color=RISK_MED, size=12, family="Poppins"))
    fig.update_layout(
        height=110, margin=dict(l=10, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, ticksuffix="%",
                   tickfont={"size": 10, "color": INK_SOFT}),
        yaxis=dict(showgrid=False, showticklabels=False),
    )
    return fig

# ----------------------------------------------------------------------------
# SIDEBAR / NAVEGAÇÃO
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(LOGO_HTML, unsafe_allow_html=True)
    st.markdown(f"<div style='color:{INK_SOFT}; font-size:0.78rem; margin-bottom:1rem;'>"
                "Maturidade de Segurança da Informação<br>CIS Controls v8 · Diretoria</div>",
                unsafe_allow_html=True)
    secao = st.radio(
        "Navegação",
        ["Visão geral",
         "1 · O problema de hoje",
         "2 · O framework (CIS & IG)",
         "3 · O plano rumo ao IG1"],
        label_visibility="collapsed",
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{INK_SOFT}; font-size:0.72rem;'>"
                "Fonte: revisão conduzida pela L&amp;L Solutions · setembro de 2025.<br><br>"
                "Documento de uso interno · confidencial.</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SEÇÃO: VISÃO GERAL
# ----------------------------------------------------------------------------
if secao == "Visão geral":
    st.markdown("<div class='eyebrow'>Maturidade de Segurança · CIS Controls v8</div>", unsafe_allow_html=True)
    st.markdown("<div class='script' style='font-size:4rem; margin:-6px 0 2px;'>Onde estamos</div>", unsafe_allow_html=True)
    st.markdown("<p class='lede'>Uma leitura de um minuto sobre a segurança digital da FG/A: "
                "o ponto de partida, o alvo e o tamanho do esforço.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.1, 1, 1])
    with c1:
        st.markdown("<div class='stat-label'>Nota geral do ambiente</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_gauge(), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='color:{INK_SOFT}; font-size:0.8rem; text-align:center;'>"
                    f"linha tracejada = meta de ~{int(NOTA_META)}% ao completar o IG1</div>",
                    unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-label'>Como os riscos se distribuem (18 domínios)</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_risco(), use_container_width=True, config={"displayModeBar": False})
    with c3:
        st.markdown("<div class='stat-label'>Esforço para completar o IG1</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_esforco(), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='card card-good'><h4>O que já protege</h4>"
                    "<p>Perímetro (VPN+MFA), antivírus/EDR gerido, SIEM terceirizado e auditoria "
                    "externa independente já funcionam. Não é um projeto do zero.</p></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='card card-bad'><h4>O que ainda expõe</h4>"
                    "<p>Faltam visibilidade dos ativos, proteção formal de dados, higiene operacional, "
                    "continuidade testada e fator humano. Lacunas concentradas, não espalhadas.</p></div>",
                    unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='card card-warn'><h4>Por que agora</h4>"
                    "<p>A XP condiciona o acesso direto via API à comprovação de maturidade. "
                    "É uma condição comercial — não só compliance.</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SEÇÃO 1: O PROBLEMA
# ----------------------------------------------------------------------------
elif secao == "1 · O problema de hoje":
    st.markdown("<div class='eyebrow'>Ato 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='script' style='font-size:4rem; margin:-6px 0 2px;'>O problema</div>", unsafe_allow_html=True)
    st.markdown("<p class='lede'>A segurança da FG/A tem uma base sólida em algumas frentes e lacunas "
                "relevantes em outras. O que importa para a diretoria é a divisão entre o que funciona, "
                "o que não funciona e o que isso custa ao negócio.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("#### O que já é funcional")
    g1, g2, g3, g4 = st.columns(4)
    for col, t, d in [
        (g1, "Perímetro e acesso", "VPN com MFA e 2FA nas interfaces administrativas; firewall com filtro de spam e inspeção de tráfego."),
        (g2, "Defesa e monitoramento", "Antivírus/EDR gerido por parceiro dedicado e SIEM terceirizado com triagem por IA — a área técnica mais madura."),
        (g3, "Governança externa", "Auditoria independente e verificação regulatória para nuvem no exterior — o domínio mais bem avaliado."),
        (g4, "Resposta a incidentes", "Processo formal de resposta apoiado por parceiro especializado (MSSP)."),
    ]:
        col.markdown(f"<div class='card card-good'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#### O que ainda não é funcional")
    b1, b2, b3 = st.columns(3)
    for col, t, d in [
        (b1, "Visibilidade dos ativos", "Sem inventário de equipamentos e de softwares. Não se protege o que não se enxerga — é o principal ponto cego."),
        (b2, "Proteção de dados", "Faltam mapeamento, classificação e criptografia formal de dados pessoais — exposição direta à LGPD."),
        (b3, "Higiene operacional", "Correções sem processo formal, estações sem hardening e contas sem controle e rotação de senha."),
    ]:
        col.markdown(f"<div class='card card-bad'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)
    b4, b5, b6 = st.columns(3)
    for col, t, d in [
        (b4, "Continuidade", "Backup existe, mas sem plano de continuidade formal nem recuperação de desastre testada."),
        (b5, "Fator humano", "Sem programa contínuo de conscientização nem simulação de phishing — o vetor de ataque mais comum."),
        (b6, "Validação", "Nenhum teste de invasão formal já realizado — a eficácia das defesas nunca foi comprovada na prática."),
    ]:
        col.markdown(f"<div class='card card-bad'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#### As consequências para o negócio")
    k1, k2, k3, k4 = st.columns(4)
    for col, t, d in [
        (k1, "Comercial", "Acesso direto via API à XP travado — uma nova fonte de dados e receita bloqueada."),
        (k2, "Regulatório", "Exposição à LGPD e risco perante o regulador por dados pessoais sem proteção formal."),
        (k3, "Operacional", "Resposta a incidentes limitada pela falta de inventário e por continuidade não testada."),
        (k4, "Reputacional", "Gestora que custodia dados sensíveis sem higiene básica comprovada perde confiança de clientes e parceiros."),
    ]:
        col.markdown(f"<div class='card card-warn'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SEÇÃO 2: O FRAMEWORK
# ----------------------------------------------------------------------------
elif secao == "2 · O framework (CIS & IG)":
    st.markdown("<div class='eyebrow'>Ato 2</div>", unsafe_allow_html=True)
    st.markdown("<div class='script' style='font-size:4rem; margin:-6px 0 2px;'>O framework</div>", unsafe_allow_html=True)
    st.markdown("<p class='lede'>Para medir maturidade de forma reconhecida pelo mercado, usamos o "
                "CIS Controls v8 — o mesmo padrão que a XP e o setor financeiro reconhecem.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.1])
    with c1:
        st.markdown("#### O que é o CIS Controls v8")
        st.markdown(f"<p style='color:{INK_SOFT}; font-size:0.92rem;'>"
                    "Um conjunto de boas práticas de segurança organizado em <b>18 controles</b> e "
                    "<b>153 salvaguardas</b> (safeguards). Em vez de teoria, ele prioriza as ações que "
                    "de fato barram os ataques mais comuns — do essencial ao avançado.</p>",
                    unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("#### Os três níveis (Grupos de Implementação)")
        for t, d, pill, cls in [
            ("IG1 — Higiene essencial", "56 salvaguardas. O piso mínimo. Defende contra os ataques não direcionados, que são a maioria. <b>É a nossa meta.</b>", "Nosso alvo", "pill-lo"),
            ("IG2 — Dados sensíveis de terceiros", "+74 salvaguardas. Para quem gere dados de clientes em múltiplas áreas e enfrenta ataques mais elaborados.", "Nível seguinte", "pill-md"),
            ("IG3 — Ambientes-alvo", "+23 salvaguardas. Para organizações sujeitas a ataques sofisticados e direcionados.", "Avançado", "pill-md"),
        ]:
            st.markdown(f"<div class='card' style='margin-bottom:10px;'>"
                        f"<span class='pill {cls}'>{pill}</span>"
                        f"<h4 style='margin-top:8px;'>{t}</h4>"
                        f"<p>{d}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("#### Onde o IG1 nos coloca")
        st.markdown(f"<p style='color:{INK_SOFT}; font-size:0.92rem;'>O IG1 é um subconjunto do total de "
                    "salvaguardas — o piso reconhecido pelo mercado.</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_ig(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>"
                    f"<div style='display:flex; align-items:baseline; gap:14px;'>"
                    f"<span class='big-stat'>53,1% → ~80%</span></div>"
                    f"<p style='margin-top:8px;'>Completar o IG1 eleva a nota geral do ambiente de "
                    f"<b>53,1%</b> para cerca de <b>80%</b>. O caminho é mais curto do que a nota atual sugere: "
                    f"boa parte é formalizar o que já existe.</p></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_progress(), use_container_width=True, config={"displayModeBar": False})

# ----------------------------------------------------------------------------
# SEÇÃO 3: O PLANO
# ----------------------------------------------------------------------------
elif secao == "3 · O plano rumo ao IG1":
    st.markdown("<div class='eyebrow'>Ato 3 · Rumo ao IG1</div>", unsafe_allow_html=True)
    st.markdown("<div class='script' style='font-size:4rem; margin:-6px 0 2px;'>O caminho</div>", unsafe_allow_html=True)
    st.markdown("<p class='lede'>Um plano em marcos — não em datas. Cada marco fecha um lote de salvaguardas do IG1. "
                "A priorização é por esforço e dependência, do mais leve ao mais estruturante.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    e1, e2 = st.columns([1, 1.4])
    with e1:
        st.markdown("#### O tamanho do trabalho")
        st.plotly_chart(fig_esforco(), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<p style='color:{INK_SOFT}; font-size:0.85rem;'>Dos ~50 itens do IG1 no nosso escopo, "
                    "<b>11 já estão prontos</b>. Restam <b>39</b>: 18 de formalização e 21 a implementar do zero.</p>",
                    unsafe_allow_html=True)
    with e2:
        st.markdown("#### O que falta, por marco")
        st.markdown(f"<p style='color:{INK_SOFT}; font-size:0.9rem;'>Selecione um marco para ver as ações "
                    "que faltam. A ordem é a sequência recomendada de execução.</p>", unsafe_allow_html=True)
        marco = st.select_slider(
            "Marco",
            options=["Marco 0", "Marco 1", "Marco 2", "Marco 3"],
            value="Marco 0",
            label_visibility="collapsed",
        )
        detalhes = {
            "Marco 0": ("Governança", [
                "Definir a matriz de responsabilidades (quem aprova, executa e revisa cada frente).",
                "Instalar um comitê de acompanhamento com checkpoint periódico à diretoria.",
                "Fechar o modelo de execução misto — time interno + parceiro.",
            ]),
            "Marco 1": ("Ganhos rápidos", [
                "Organizar a gestão de contas (eliminar contas genéricas, rotação de senha).",
                "Contratar teste de invasão externo e independente.",
                "Iniciar programa contínuo de conscientização e simulação de phishing.",
                "Formalizar processos já praticados (correções, backup, configuração de firewall).",
            ]),
            "Marco 2": ("Visibilidade e higiene", [
                "Levantar o inventário de ativos e de softwares com ferramentas já licenciadas.",
                "Estabelecer gestão formal de correções, com prazo por criticidade.",
                "Validar a segmentação de rede entre ambientes.",
            ]),
            "Marco 3": ("Proteção e resiliência", [
                "Estruturar a proteção de dados exigida pela LGPD (mapeamento, classificação, criptografia).",
                "Formalizar o plano de continuidade e testar a recuperação de desastre.",
                "Aplicar hardening completo em estações e notebooks.",
                "Implantar gestão de acesso privilegiado e segregação de funções.",
            ]),
        }
        titulo, itens = detalhes[marco]
        n = marco.split()[-1]
        lis = "".join(f"<li>{i}</li>" for i in itens)
        st.markdown(f"<div class='ms'><span class='n'>{n}</span><h4>{titulo}</h4><ul>{lis}</ul></div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card card-good'>"
                f"<h4>Resultado ao fim do Marco 3</h4>"
                f"<p style='font-size:0.95rem;'>Os 39 itens fechados levam o IG1 a <b>100%</b> — e a nota geral "
                f"do ambiente para <b>~80%</b>, o piso que a XP e o mercado reconhecem. "
                f"Itens de maior criticidade e custo (proteção de dados, continuidade) entram no último marco "
                f"por dependerem dos anteriores — é um trade-off consciente entre esforço e impacto.</p></div>",
                unsafe_allow_html=True)
    st.caption("Marcos representam sequência e dependência, não prazos. O cronograma é definido no Marco 0, "
               "junto com a matriz de responsabilidades.")
