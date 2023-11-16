#Importazione delle librerie ______________________________________________
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st

# set page layout
st.set_page_config(
    page_title="Vendita di abbigliamento in una catena di fast fashion",
    layout="centered",
    initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #32004C;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#Importazione di dati ______________________________________________
df = pd.read_csv(filepath_or_buffer='store.csv', sep=',')
df['date'] = pd.to_datetime(df['date'])
df['item'] = df['item'].astype(str)

#--------------------------------------------------------------------------
st.title('Vendita di abbigliamento in una catena di fast fashion')

#--------------------------------------------------------------------------
st.header('_Introduzione_')

st.write('''
Il nostro set di dati originale aveva circa 400.000 righe sui prodotti venduti in una 
grande catena di negozi di abbigliamento (fast fashion) con 6 colonne (data, negozio,
articolo, quantità, prezzo_unitario, categoria_articolo).
\n
Quindi, per prima cosa abbiamo dovuto pulire e selezionare i nostri dati. Per fare ciò abbiamo dovuto:
- convertire le colonne data in datetime,
- ordinare i valori per data, crescente,
- convertire la colonna di quantità e prezzo in numeri interi,
- convertire l'elemento della colonna in una stringa,
- creare il totale della colonna (quantità * prezzo),
- convertire il totale della colonna in un numero intero,
- eliminare le colonne archivio, categoria, senza nome,
\n
In secondo luogo selezioniamo solo le righe relative ai primi 10 articoli più venduti:
\n
In terzo luogo, uniamo quel set di dati con un altro set di dati temporali sulla temperatura.
Tuttavia quei dati erano in Farenheit, quindi abbiamo dovuto convertirli in Celsius.
\n
In quarto luogo, mappiamo il nuovo set di dati con un elenco di nomi di vestiti,
dal momento che il nostro set di dati originale non aveva i nomi dei vestiti.
\n
Infine, abbiamo terminato con un nuovo set di dati di 6310 righe e 6 colonne (date,item,qty,total,Celsius,cloth).
\n
Abbiamo scelto di effettuare un'analisi esplorativa solo sulle vendite e
profitti dei prodotti più venduti nel periodo da marzo 2017 a
Marzo 2019. Questa opzione è stata scelta per ragioni di riduzione dell'analisi.
In altre parole, non ci siamo concentrati sui negozi e sulle categorie di prodotto.
''')

st.write('Ecco il nostro set di dati pulito:')

with st.expander('Data Set'):
    st.dataframe(df)

st.write('''And here is our data cleaning code:''')

with st.expander('Data cleaning'):
    st.code('''
#Import libraries
import pandas as pd

#Import dataset         
df = pd.read_csv('sales_data.csv')
             
#Convert 'date' do 'datetime'
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

#sort by date ascending
df = df.sort_values(by='date', ascending=True)

#Convert columns
df['qty'] = df['qty'].astype(int)
df['unit_price'] = df['unit_price'].astype(int)
df['item'] = df['item'].astype(str)

#creat column 'total'
df['total'] = df['qty']*df['unit_price']

#convert total:
df['total'] = df['total'].astype(int)

#delet column unnamed:6
df = df.drop(['store', 'item_category', 'Unnamed: 6'], axis=1)
             
#Select only the rows concerning the top most sold itens:
df2 = df.groupby(['date', 'item'])[['qty', 'total']].sum().reset_index().sort_values(by='date', ascending=True)
top_items = df.groupby(['item'])['qty'].sum().reset_index().sort_values(by='qty', ascending=False).head(10)
df1 = df2[df2['item'].isin(top_items['item'])]
             
#Merge with temperature dates:
celsius = pd.read_csv('temperature_italy.csv')
celsius['Date'] = pd.to_datetime(celsius['Date'], format='%Y-%m-%d')
df1 = pd.merge(df1, celsius, left_on='date', right_on='Date', how='inner')
df1 = df1.drop(['Country', 'Date'], axis=1)
             
#Map with clothes
itens = top_items['item'].to_list()
nomes = ['canotta bianca', 'maglietta', 'wind-giacca', 'maglione', 'camicia', 'pantalone', 'canotta nera', 'giubotto', 'calzini', 'mutande']
dicionario_itens_nomes = dict(zip(itens, nomes))
df1['cloth'] = df1['item'].map(dicionario_itens_nomes)

#Save as 'store.csv':        
df1.to_csv(path_or_buf='store.csv', sep=',', index=False)
             
''')

#-----------------------------------------------------------------------------------
st.header('_1. Come è il comportamento dei primi 10 articoli più venduti nel periodo?_')

st.write('''Controliamo come sono le vendite da marzo 2017 a marzo 2019.''')

fig1 = px.line(
    data_frame=df, 
    x="date", 
    y='qty', 
    color='item', 
    title='TOP 10 ARTICOLI PIÙ VENDUTI DURANTE IL PERIODO')
fig1.update_layout(
    font_size=10, 
    paper_bgcolor='#32004C', 
    plot_bgcolor='#712C94', 
    hoverdistance=10, 
    spikedistance=5)
st.plotly_chart(
    figure_or_data=fig1,
    use_container_width=False,
    sharing='streamlit',
    theme='streamlit')

st.write('''
Una rapida occhiata a questo grafico ci mostra alcune informazioni:
- Gli articoli più venduti sono stati: ['185', '186', '416', '385', '519', '179', '408', '346', '158', '352'],
- L'articolo 185 è stato venduto solo fino al 01/06/2018,
- Gli articoli 408 e 519 iniziarono ad essere venduti il giorno dopo,
- Si suggerisce che gli articoli 408 e 519 potrebbero essere un nuovo articolo simile al 185 che lo ha sostituto,
- Sembra che ci sia una leggera correlazione tra le vendite,
- Le vendite dell'articolo 185 può essere considerata un outlier,
''')

#-----------------------------------------------------------------------------------
st.header('_2. Come è stato il comportamento dei primi 10 articoli più profitti nel periodo?_')

st.write('''Vediamo come è il profitto da marzo 2017 a marzo 2019.''')

fig2 = px.line(
    data_frame=df, 
    x="date", 
    y='total', 
    color='item', 
    title='I 10 ARTICOLI PIÙ PROFITTI DURANTE IL PERIODO')
fig2.update_layout(
    font_size=10, 
    paper_bgcolor='#32004C', 
    plot_bgcolor='#712C94', 
    hoverdistance=10, 
    spikedistance=-1)
st.plotly_chart(
    figure_or_data=fig2,
    use_container_width=False,
    sharing='streamlit',
    theme='streamlit')

st.write('''
- Gli articoli più redditizi sono stati: ['186', '416', '179', '385', '185', '408', '352', '346', '158', '519']
''')

#-------------------------------------------------------
st.header('_3. Confronto tra gli articoli più venduti e redditizi per stagione_')

st.write('''
Visualizziamo questi dati divisi per stagioni. Dal momento che stiamo lavorando con i dati dell'abbigliamento
settore, e questo settore cambia stagionalmente i suoi prodotti, è interessante e corretto da vedere
il comportamento dei dati per stagione.
''')

periods = [('2017-03-15', '2017-09-21'), ('2017-09-22', '2018-03-21'), ('2018-03-22', '2018-09-21'), ('2018-09-22', '2019-03-30')]
period_names = ['Primavera-Estate 2017', 'Autunno-Inverno 2017', 'Primavera-Estate 2018', 'Autunno-Inverno 2018']

results_qty = {}
for i, (period_start, period_end) in enumerate(periods):
    current_period = df[(df['date'] >= period_start) & (df['date'] <= period_end)]
    top_10_item_qty = current_period.groupby(['item'])[['qty']].sum().reset_index().sort_values(by='qty', ascending=False).head(10)
    period_name = f"{period_names[i]}: {period_start} - {period_end}"
    results_qty[period_name] = top_10_item_qty

results_total = {}
for i, (period_start, period_end) in enumerate(periods):
    current_period = df[(df['date'] >= period_start) & (df['date'] <= period_end)]
    top_10_item_total = current_period.groupby(['item'])[['total']].sum().reset_index().sort_values(by='total', ascending=False).head(10)
    period_name = f"{period_names[i]}: {period_start} - {period_end}"
    results_total[period_name] = top_10_item_total

fig3 = make_subplots(
    rows=2, 
    cols=2, 
    subplot_titles=('Primavera-Estate 2017', 'Autunno-Inverno 2017', 'Primavera-Estate 2018', 'Autunno-Inverno 2018'), 
    column_widths=[2, 2] )

for i, (period_name, top_10_products_qty) in enumerate(results_qty.items(), 1):
    trace_qty = go.Bar(
        x=top_10_products_qty['item'], 
        y=top_10_products_qty['qty'], 
        name=period_name, 
        marker_color='#45951d')
    row_qty = (i - 1) // 2 + 1
    col_qty = (i - 1) % 2 + 1
    fig3.add_trace(trace_qty, row=row_qty, col=col_qty)

for i, (period_name, top_10_products_total) in enumerate(results_total.items(), 1):
    trace_total = go.Bar(
        x=top_10_products_total['item'], 
        y=top_10_products_total['total'], 
        name=period_name, 
        marker_color='#DBA507' )
    row_total = (i - 1) // 2 + 1
    col_total = (i - 1) % 2 + 1
    fig3.add_trace(trace_total, row=row_total, col=col_total)

fig3.update_layout(
    title_text="ARTICOLI PIÙ VENDUTI E PIÙ PROFITTI PER STAGIONE",
    font_size=12,
    paper_bgcolor='#32004C',
    plot_bgcolor='#712C94',
    hoverdistance=10,
    spikedistance=-1)

st.plotly_chart(
    figure_or_data=fig3, 
    use_container_width=True, 
    sharing="streamlit", 
    theme="streamlit")

#-------------------------------------------------------------------
st.subheader('_Confronto profitto totale_')

st.write('''
Per conoscere il confronto del profitto totale, dobbiamo calcolare 
il profitto totale e le vendite per ciascun prodotto nel periodo.
Successivamente, dobbiamo confrontare i loro profitti e le loro 
vendite totali per determinare se i profitti combinati degli articoli 
408 e 519 compensano l'estinto articolo 185.
\n
Conclusione:
- Gli articoli 408 e 519 NON hanno compensato le VENDITE dell'articolo 185 in 619.573 unità,
- Hanno comunque compensato il proffito dell'articolo 185 in 2.533.996 euro,
- Pertanto, l'inserimento di questi nuovi 2 articoli, nonostante le minori vendite, ha ottenuto maggiori profitti e, probabilmente
portato risparmi nella produzione.
- Pertanto, a nostro giudizio, è stata una saggia decisione da parte della azienda 
quella di sostituire l'articolo 185 con gli articoli 408 e 519.
''')

with st.expander('Confronto profitto totale'):
    st.code('''
#TOTAL PROFIT COMPARISION (comparação do lucro total)

lucro_por_item = df1.groupby('item')['total'].sum().sort_values(ascending=False).to_dict()

a = lucro_por_item['408'] + lucro_por_item['519']
b = lucro_por_item['185']

if a >= b:
    print(f"Os itens 408 e 519 compensaram em lucros o item 185 em {a - b} euro")
else:
    None
''')

#---------------------------------------------------------------------
st.header('_4. Correlazione tra vendita e temperatura_')

st.write('''
Uno dei dati più importanti per l'industria della moda sono i dati climatici.
È estremamente importante disporre di serie di dati storici su pioggia, temperatura, vento, ecc.,
In questo modo puoi pianificare una collezione moda in modo ottimizzato, a partire dalla scelta
dalle tipologie di tessuti più adatte al design finale del prodotto.
Pertanto in questo dataset inseriamo i dati relativi alla temperatura media della città in questione,
nel periodo storico di vendita degli articoli.
Possiamo quindi sapere qual è il coefficiente di correlazione tra la media delle vendite totali
di prodotti e la temperatura media in ogni giorno di ogni vendita.
\n
Vediamolo:
''')

media = df.groupby(['date', 'Celsius'])['qty'].mean().reset_index()
media['Celsius'] = media['Celsius'] * 100
fig4 = px.line(
    media, 
    x="date", 
    y='qty', 
    color_discrete_sequence=['#d8b5e9'],)
fig4.add_trace(px.line(
    media, 
    x="date", 
    y='Celsius', 
    color_discrete_sequence=['#DBA507']).data[0])
fig4.update_layout(
    title='Correlazione tra vendite e temperatura', 
    xaxis_title='Data', 
    yaxis_title='Valor',
    font_size=12,
    paper_bgcolor='#32004C',
    plot_bgcolor='#712C94',
    hoverdistance=10,
    spikedistance=-1)
st.plotly_chart(
    figure_or_data=fig4, 
    use_container_width=True, 
    sharing="streamlit", 
    theme="streamlit")

st.write('''
Interpretare questo grafico è un po' complicato, poiché ci sono più di 6.000 dati di due anni
in un grafico a linee sovrapposto.
Tuttavia, c'è una leggera tendenza da parte delle vendite a seguire la temperatura.
Se la temperatura scende, scendono anche le vendite.
\n
Però, questa interpretazione avrebbe senso solo se lavorassimo con i dati di un negozio
focalizzato esclusivamente sull'abbigliamento primavera-estate, ma non è questo il caso.
\n
Naturalmente la temperatura non è solo un fattore rilevante per le vendite.
In una grande catena di moda, ci sono anche promozioni stagionali, lancio di
nuove collezioni, marketing e pubblicità e, sì, la volontà imprevedibile del cliente.
\n
Per sapere veramente se esiste una correlazione, dobbiamo fare un calcolo di correlazione.
\n
Fatto il calcolo otteniamo una forte correlazione positiva pari a 0.42,
il che significa che esiste effettivamente una correlazione tra queste due variabili.
''')

#------------------------------------------------------------------------------------------
st.header('_5. Dopo tutto, quali sono i vestiti?_')

st.write('''
Ora che abbiamo fatto una breve analisi esplorativa, possiamo scoprire quali sono gli 
abiti più venduti e più redditizi.
\n
Sulla base delle informazioni precedenti, possiamo provare a indovinare il nome dell'articolo più venduto e quale è il più redditizio.
\n
Abbiamo visto che:
\n
- Il nostro set di dati conteneva 83 articoli, ma abbiamo visto solo i 10 articoli più venduti e più redditizi,
- Questi elementi sono stati analizzati su un periodo di 744 giorni, compresso 8 stagioni, 2 primavera-estate e 2 autunno-inverno,
- C'era una differenza tra gli articoli più venduti e gli articoli più redditizi, quindi non tutti gli articoli più venduti erano i più redditizi,
- L'articolo 185 è stato venduto solo fino all'inizio dell'autunno-inverno 2018, quando hanno iniziato ad essere venduti gli articoli 408 e 519, il che suggerisce
nn cambiamento nella strategia di vendita, 
- Esiste una forte correlazione positiva pari a 0.42 tra il numero medio di articoli venduti e la temperatura media della città,
- L'articolo più venduto è stato 185, ma il più redditizio è stato 186.
\n
Ora possiamo provare a indovinare quali sono gli articoli 185 (più venduto) e il 186 (più proffito)
''')

itens_disponiveis = df['cloth'].unique()
itens_sold = df.groupby(['item', 'cloth'])['qty'].sum().sort_values(ascending=False).reset_index().loc[0, 'cloth']
itens_prof = df.groupby(['item', 'cloth'])['total'].sum().sort_values(ascending=False).reset_index().loc[0, 'cloth']

itens_disponiveis = df['cloth'].unique()
itens_sold = df.groupby(['item', 'cloth'])['qty'].sum().sort_values(ascending=False).reset_index().loc[0, 'cloth']
itens_prof = df.groupby(['item', 'cloth'])['total'].sum().sort_values(ascending=False).reset_index().loc[0, 'cloth']

st.write('\n ARTICOLO PIÙ VENDUTO')
item_mais_vendido = st.selectbox('''Secondo te, qual è stato l'articolo più venduto: ''', itens_disponiveis)
verificar_mais_vendido = st.button('Controlla il più venduto')
if verificar_mais_vendido:
    if item_mais_vendido == itens_sold:
        st.success('Hai indovinato!', icon='\U0001F389')
        st.balloons()
    else:
        st.error(body='Hai sbagliato!', icon= '\U0001F480')

st.write('\n ARTICOLO PIÙ REDDITIZIO')
item_mais_lucrativo = st.selectbox('''Secondo te, qual è stato l'articolo più redditizio: ''', itens_disponiveis)
verificar_mais_lucrativo = st.button('Controlla il più redditizio')
if verificar_mais_lucrativo:
    if item_mais_lucrativo == itens_prof:
        st.success('Hai indovinato!', icon='\U0001F389')
        st.balloons()
    else:
        st.error(body='Hai sbagliato!', icon= '\U0001F480')