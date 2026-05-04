import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    data = pd.read_excel('Base.xlsx', sheet_name='Base')
    title = 'Dashboard - Projeto Vendas'
    st.set_page_config(page_title=title, layout='wide')
    st.title(title)

    ano = data['Ano'].unique()
    paises = data['País'].unique()

    filtro_ano = st.sidebar.selectbox('Selecione o Ano:', options=['Todos'] + sorted(ano), index=0)
    filtro_pais = st.sidebar.selectbox('Selecione o País:', options=['Todos'] + sorted(paises), index=0)

    data_filtrada = data.copy()
    if filtro_ano != 'Todos':
            data_filtrada = data_filtrada[data_filtrada['Ano'] == filtro_ano]
    if filtro_pais != 'Todos':
        data_filtrada = data_filtrada[data_filtrada['País'] == filtro_pais]

    gf_lucroporsegmento = px.bar(
    data_filtrada.groupby('Segmento')['Lucro'].sum().reset_index(),
    x = 'Segmento', y = 'Lucro',
    title='Lucro por Segmento',
    color='Segmento',
    text_auto=True
    ) 
    gf_lucroporsegmento.update_layout(showlegend=False)

    gf_vendas_tempo = px.line(
    data_filtrada.groupby('Data')['Vendas Brutas'].sum().reset_index(),
    x='Data', y='Vendas Brutas',
    title='Vendas ao Longo do Tempo',
    markers=True
    )

    gf_venda_produto = px.pie(
    data_filtrada.groupby('Unidades Vendidas')['Produto'].sum().reset_index(),
    values='Unidades Vendidas', names='Produto',
    title='Distribuição de Produtos Vendidos',
    )

    custo_lucro_data = data_filtrada.groupby(['Segmento'])[['COGS', 'Lucro']].sum().reset_index().melt(
        id_vars='Segmento', value_vars=['COGS', 'Lucro'])
    custo_lucro_data['value_formatado'] = custo_lucro_data['value'].apply(lambda x: f'R$ {x:.2f}')

    gf_custo_lucro = px.bar(
    custo_lucro_data,
    x='Segmento', y='value',
    title='Relação Entre Custo e Lucro',
    color='variable',
    barmode='group',
    text='value_formatado'
    )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col1.plotly_chart(gf_lucroporsegmento, use_container_width=True)
    col2.plotly_chart(gf_vendas_tempo, use_container_width=True)
    col3.plotly_chart(gf_venda_produto, use_container_width=True)
    col4.plotly_chart(gf_custo_lucro, use_container_width=True)

main()