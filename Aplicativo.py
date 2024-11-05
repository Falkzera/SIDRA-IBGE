import pandas as pd
import sidrapy
import streamlit as st
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from Creditos.Credito import display_credits

st.set_page_config(page_title='Pesquisa Trimestral do Leite - IBGE', page_icon='🐄', layout='wide')



with st.container(): # Extração, manipulação e limpeza dos dados.

    @st.cache_data(ttl=86400)
    def load_data():
        data = sidrapy.get_table(table_code='1086',
                                territorial_level='3',
                                ibge_territorial_code='all',
                                variable='283',
                                period='all')

        data.columns = data.iloc[0]
        df = data.iloc[1:,[7,6,4]].copy()
        df['DATA'] = pd.to_datetime(df['Trimestre (Código)'].str.slice(0,4) + '-' + df['Trimestre (Código)'].str.slice(4,6))
        df = df.drop(columns='Trimestre (Código)')
        df = df.rename(columns={'Unidade da Federação':'UF', 'Valor':'VALOR'})[['DATA','UF','VALOR']]
        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0).astype(float)
        df['UF'] = df['UF'].astype('string')    

        hora_consulta = datetime.now().strftime('%d/%m/%Y - %H:%M')

        return df, hora_consulta
    
    df, hora_consulta = load_data()

    ranking_estados = df.sort_values('DATA').groupby('UF').tail(1).sort_values('VALOR', ascending=False).reset_index(drop=True)





# todas_ufs = df['UF'].unique()

# fig = go.Figure()

# for uf in todas_ufs:
#     df_filtrado = df[df['UF'] == uf]
#     media_movel_simples = df_filtrado['VALOR'].rolling(window=3).mean()
#     fig.add_trace(go.Scatter(x=df_filtrado['DATA'], y=media_movel_simples, mode='lines', name=f'{uf}'))

# fig.update_layout(title='Série histórica do Leite Industrializado - Todas as UFs', template='plotly_dark')
# st.plotly_chart(fig)



with st.container(): # SIDEBAR

    st.sidebar.title('FILTROS: 📋')
    st.sidebar.write('---')


    uf = st.sidebar.selectbox('Selecione o ESTADO:', ['Brasil'] + sorted(df['UF'].unique()))

    if uf != 'Brasil':
        df = df[df['UF'] == uf].reset_index(drop=True)
    else:
        df = df.groupby('DATA', as_index=False)['VALOR'].sum().reset_index(drop=True)

with st.container(): # TÍTULOS

    st.title('Pesquisa Trimestral do Leite 🐄')
    st.write('---')
    st.info(f"Fonte: IBGE - Consultado em {hora_consulta}")
    st.subheader(f'Produção de Leite Industrializado - {uf}')

with st.container(): # FORMATAÇÃO DE VALORES

    def format_value(value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value / 1_000:,.2f} Mil"
        else:
            return f"{value:.0f}"
        
with st.container(): # METRICAS 
        
    col1, col2, col3, col4 = st.columns(4)
        
    ano_atual = df['DATA'].dt.year.values[-1]
    ano_anterior = ano_atual - 1

    mes_atual = df['DATA'].dt.month.values[-1]
    mes_anterior = mes_atual - 1
    porcentagem_diff_mes = (df[df['DATA'].dt.month == mes_atual]['VALOR'].sum() / df[df['DATA'].dt.month == mes_anterior]['VALOR'].sum() - 1) * 100

    ano_atual_mes_atual = df[(df['DATA'].dt.year == ano_atual) & (df['DATA'].dt.month <= mes_atual)]['VALOR'].sum()
    ano_passado_mes_atual = df[(df['DATA'].dt.year == ano_anterior) & (df['DATA'].dt.month <= mes_atual)]['VALOR'].sum()
    porcentagem_diff_ano_mes = (ano_atual_mes_atual / ano_passado_mes_atual - 1) * 100

    ultimos_5_trimestres = df[df['DATA'] >= (df['DATA'].max() - pd.DateOffset(months=12))]
    ultimos_5_trimestres_anterior = df[(df['DATA'] < (df['DATA'].max() - pd.DateOffset(months=12))) & (df['DATA'] >= (df['DATA'].max() - pd.DateOffset(months=25)))]
    porcentagem_diff_ultimos_5_trimestres = (ultimos_5_trimestres['VALOR'].mean() / ultimos_5_trimestres_anterior['VALOR'].mean() - 1) * 100

    with col1:
        st.metric(label='Produção Total', value=format_value(df['VALOR'].sum()))
    with col2:
        st.metric(label='Produção Média dos últimos 5 trimestres', value=format_value(ultimos_5_trimestres['VALOR'].mean()), delta=f"{porcentagem_diff_ultimos_5_trimestres:.2f}% Variação")
    with col3:
        st.metric(label=f'Produção Total {ano_atual} até o {mes_atual}°T', value=format_value(df[df['DATA'].dt.year == ano_atual]['VALOR'].sum()), delta=f"{porcentagem_diff_ano_mes:.2f}% Variação: {ano_anterior} até o {mes_atual}°T")
    with col4:
        st.metric(label=f'Produção do {ano_atual}-{mes_atual}°T', value=format_value(df['VALOR'].tail(1).sum()), delta=f"{porcentagem_diff_mes:.2f}% Variação Trimestre anterior")

with st.container(): # GŔAFICO

    media_movel_simples = df['VALOR'].rolling(window=3).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['DATA'], y=media_movel_simples, mode='lines', name='Média Móvel Simples'))
    fig.update_layout(title=f'Série histórica do Leite Industrializado', template='plotly_dark')
    st.plotly_chart(fig)

with st.container(): # EXPANDER

    df_tabular = df.copy()
    with st.expander(f'VISUALIZAR SÉRIE HISTÓRICA -- {uf.upper()}'):

        st.data_editor(
            df_tabular,
            column_config={
                "VALOR": st.column_config.ProgressColumn(
                    "VALOR",
                    format="%f",
                    min_value=0,
                    max_value=df['VALOR'].max(),
                ),
            },
            hide_index=True,
            use_container_width=True
        )

with st.container(): # RANKING
        
        st.write('---')
    
        st.subheader('Ranking dos Estados por Produção de Leite Industrializado')
        # ranking_estados['VALOR'] = ranking_estados['VALOR'].astype(float)

        st.data_editor(
            ranking_estados,
            column_config={
                "VALOR": st.column_config.ProgressColumn(
                    "VALOR",
                    format="%f",
                    min_value=0,
                    max_value=ranking_estados['VALOR'].values[0],
                ),
            },
            hide_index=True,
            use_container_width=True
        )


with st.container(): # Gráfico top 6

    # grafico de barras com ranking estados (apenas os 6 primeiros)
    top_6_estados = ranking_estados.head(6)
    fig_bar = go.Figure(go.Bar(
        x=top_6_estados['UF'],
        y=top_6_estados['VALOR'],
        text=top_6_estados['VALOR'],
        textposition='auto'
    ))

    fig_bar.update_layout(
        title='Ranking dos Estados por Produção de Leite Industrializado (Top 6)',
        xaxis_title='Estado',
        yaxis_title='Produção de Leite',
        template='plotly_dark'
    )

    st.plotly_chart(fig_bar)
    # Adicionando linha de tendência e anotação ao gráfico de barras

    # Calculando a linha de tendência
    z = np.polyfit(range(len(top_6_estados)), top_6_estados['VALOR'], 1)
    p = np.poly1d(z)

    # Adicionando a linha de tendência ao gráfico de barras
    fig_bar.add_trace(go.Scatter(
        x=top_6_estados['UF'],
        y=p(range(len(top_6_estados))),
        mode='lines',
        name='Tendência',
        line=dict(color='firebrick', width=2, dash='dash')
    ))

    # Adicionando anotações para destacar a diferença entre os estados
    for i, row in top_6_estados.iterrows():
        fig_bar.add_annotation(
            x=row['UF'],
            y=row['VALOR'],
            text=f"{row['VALOR']:.2f}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40
        )

    # Atualizando o layout do gráfico
    fig_bar.update_layout(
        title='Ranking dos Estados por Produção de Leite Industrializado (Top 6) com Linha de Tendência',
        xaxis_title='Estado',
        yaxis_title='Produção de Leite',
        template='plotly_dark'
    )

    st.plotly_chart(fig_bar)

with st.sidebar:
    display_credits()