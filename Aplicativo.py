import pandas as pd
import sidrapy
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go



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
        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0).astype(int)
        df['UF'] = df['UF'].astype('string')

        hora_consulta = datetime.now().strftime('%d/%m/%Y - %H:%M')

        return df, hora_consulta
    
    df, hora_consulta = load_data()
    
with st.container(): # Títulos

    st.subheader('Pesquisa Trimestral do Leite- IBGE')
    st.info(f"Fonte: IBGE - Consultado em {hora_consulta}")

with st.container(): # Sidebar

    st.sidebar.subheader('Filtros')

    todas_uf = pd.Series(df['UF'].unique()).sort_values().tolist()
    uf_selecionada = st.sidebar.multiselect('UF:', todas_uf)

    if not uf_selecionada:
        st.warning('Selecione pelo menos uma UF.')
        st.stop()
    
    df_filtrado = df[df['UF'].isin(uf_selecionada)].copy().sort_values(by='DATA', ascending=False).reset_index(drop=True)
    st.write(df_filtrado)





