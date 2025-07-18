import streamlit as st
import pandas as pd
import numpy as np

st.header('Métodos alternativos para atribuir mandatos nas eleições legislativas em Portugal')
st.caption('Atualizado em 3/2/2022')
#DATA_URL = ('./deputados.csv')
TOTAL_URL_2022 = ('./total_2019_b.csv')
TOTAL_URL_2019 = ('./total_2019.csv')
def load_data(ano):
    if ano == 2022:
        total = pd.read_csv(TOTAL_URL_2022)
    else:
        total = pd.read_csv(TOTAL_URL_2019)    
    return total

def dHondt(votes, seats):
    num_parties = len(votes)
    quotient = votes
    new_quotients = votes
    allocation = np.ones(num_parties)
    while seats > 0:
        quotient = votes/allocation
        idx = np.argmax(quotient)
        allocation[idx] = allocation[idx]+1
        seats = seats - 1
        new_quotients = votes/allocation
    return allocation-1, new_quotients


ano = st.radio(
            'Ano:', (2019,2022))
data_load_state = st.text('Loading data...')
votos = load_data(ano)
data_load_state.text('Loading data... done!')

option = st.selectbox(
     'Escolha a opção:',
     ('Início', 'Distribuição dos Mandatos'))

if option == 'Início':

    st.markdown("""Eleições Legislativas: E se os mandatos fossem distribuídos de forma diferente? \
    Nesta web app pode-se testar, com os resultados das eleições legislativas de 2019 e 2022, diferentes formas \
    de atribuir mandatos, como círculo eleitoral único, utilização de círculo de compensação, \
    fusão de pequenos círculos entre outras. 
    """)
    st.markdown("""Há também um **what-if scenario** para o PSD: o que aconteceria se o partido tivesse concorrido coligado? \
    Qual seria o efeito na representatividade dos resultados eleitorais? 
    """)
    st.markdown("""
    Para avaliar a representatividade destes métodos alternativos, incluí o **índice de Loosemore–Hanby** (LHI) \
    que mede a desproporção relativa entre votos e assentos obtidos pelos partidos em uma eleição. \
    Para calcular o índice somamos o valor absoluto das diferenças \
    (para que não haja cancelamento entre diferenças positivas e negativas) entre a porcentagem de votos \
    recebidos (V) e a porcentagem assentos obtidos (S). A divisão por 2 é para limitar a faixa de valores do \
    índice entre 0% e 100%
    """)
    st.latex(r'''LHI =\frac{1}{2}\sum_{i=1}^{n}\left|V_i-S_i\right|
     ''')



elif option == 'Distribuição dos Mandatos':
    total_2019 = votos.copy()
    total_2019 = total_2019.set_index('Círculo')
    circulos = list(total_2019.index)
    partidos = list(total_2019.columns[:-5])
    barreira = 0
    sup = 0

    whatif_partidos = 'PSD2019'
    whatif_circulos = '2019'
    whatif_distritos = '2019'

    flag_circulo = st.checkbox(
     'Cenários Alternativos')

    if flag_circulo:
        option = st.radio('Círculos Eleitorais:',
        ('2019/2022','Fusão de pequenos círculos', '6 círculos no território nacional (4 continente + 2 ilhas)', 'Círculo Único'))
        if option != 'Círculo Único':
            st.write('Obs: Em 2022, para efeito de atribuição de mandatados no círculo único e no círculo de compensação, as coligações na Madeira e Açores contam para o PSD')
            sup = st.slider('Tamanho do Círculo de Compensação', 0,20,0,5)
            if sup != 0: 
                whatif_circulos = 'misto'
                barreira = st.radio('Clausula de Barreira (%):', (0, 0.5, 1, 2))
            if option == 'Fusão de pequenos círculos':
                whatif_distritos = 'distritos_8'
            elif option == '6 círculos no território nacional (4 continente + 2 ilhas)':
                whatif_distritos = 'grandes'
        else:
            st.write('Obs: Em 2022, para efeito de atribuição de mandatados no círculo único e no círculo de compensação, as coligações na Madeira e Açores contam para o PSD')

            whatif_circulos = 'circulo unico'
            barreira = st.radio(
            'Clausula de Barreira (%):', (0, 0.5, 1, 2))
        with st.expander("Detalhes"):
            st.markdown("""
            **Fusão de pequenos círculos**: unir círculos que elegem menos de 6 deputados:\n
            Alentejo (8): Évora + Beja + Portalegre\n
            Beira Interior (7): Castelo Branco + Guarda\n
            Trás os Montes (8): Vila Real + Bragança 
            """)
            st.markdown("""
            **6 círculos**: os quatro círculos do continente\n
            Norte (33): Braga, Viana do Castelo, Vila Real, Bragança\n
            Centro1 (33): Aveiro, Coimbra, Viseu\n
            Centro2 (28): Leiria, Santarém, Portalegre, Castelo Branco, Guarda\n
            Sul (33): Setúbal, Évora, Beja, Faro\n
            """)
            st.markdown("""
            **Círculo de Compensação:** Quantos mandatos cada círculo perde.\n
            5: Lisboa 3, Porto 2 \n
            10: Lisboa 4, Porto 3, Braga 1, Setúbal 1, Aveiro \n
            15: Lisboa 5, Porto 4, Braga 2, Setúbal 2, Aveiro 2 \n
            20: Lisboa 5, Porto 4, Braga 3, Setúbal 3, Aveiro 2, Faro 1, Leiria 1, Santarém 1
            """)
            st.markdown("""
            **Cláusula de Barreira:**: Quantidade mínima de votos (%) para um partido ser \
            elegível a lugares no parlamento em caso de círculo único ou para concorrer aos lugares \
            atribuídos pelo círculo de compensação.
            """)
        
        option_direita = st.radio('Centro-Direita:',
        ('2019/2022', 'PSD e CDS coligados'))
        if option_direita == 'PSD 2015 = PSD+ALI+CHEGA':
            whatif_partidos = 'PSD2015'
        if option_direita == 'PSD e CDS coligados':
            whatif_partidos = 'PSD/CDS-PP'
        elif option_direita == 'PaF 2019 = PSD+CDS-PP':
            whatif_partidos = 'PaF2019'
        elif option_direita == 'PaF 2015 = PSD + CDS-PP + ALI + CHEGA':
            whatif_partidos = 'PaF2015'
        else:
            whatif_partidos = 'PSD2019'


    if  sup == 20:
     #   if ano == 2022:
     #       total_2019['misto'] = [5,14,3,16,3,4,9,3,8,3,9,43,6,2,36,8,15,6,5,8,0,0]   # 20 suplementares
     #   else:
        total_2019['misto'] = [5,14,3,16,3,4,9,3,8,3,9,43,6,2,36,8,15,6,5,8,2,2]   # 20 suplementares
    elif sup == 15:
    #    if ano == 2022:
    #        total_2019['misto'] = [5,14,3,17,3,4,9,3,9,3,10,43,6,2,36,9,16,6,5,8,2,0]   # 15 suplementares
    #    else:
        total_2019['misto'] = [5,14,3,17,3,4,9,3,9,3,10,43,6,2,36,9,16,6,5,8,2,2]   # 15 suplementares
    elif sup == 10:
    #    if ano == 2022:
    #        total_2019['misto'] = [5,15,3,18,3,4,9,3,9,3,10,44,6,2,37,9,17,6,5,8,0,0]   # 10 suplementares
    #    else:
        total_2019['misto'] = [5,15,3,18,3,4,9,3,9,3,10,44,6,2,37,9,17,6,5,8,2,2]   # 10 suplementares        
    elif sup == 5:
    #    if ano == 2022:
    #        total_2019['misto'] = [5,16,3,19,3,4,9,3,9,3,10,45,6,2,38,9,18,6,5,8,0,0]   # 5 suplementares 
    #    else:
        total_2019['misto'] = [5,16,3,19,3,4,9,3,9,3,10,45,6,2,38,9,18,6,5,8,2,2]   # 5 suplementares
    else:
    #    if ano == 2022:
    #        total_2019['misto'] = [5,16,3,19,3,4,9,3,9,3,10,48,6,2,40,9,18,6,5,8,0,0]   # 0 suplementares
    #    else:
        total_2019['misto'] = [5,16,3,19,3,4,9,3,9,3,10,48,6,2,40,9,18,6,5,8,2,2]   # 0 suplementares




    if whatif_partidos == 'PSD2019':
        total_2019_s = total_2019.copy()  
        if ano == 2022:
            total_2019_s.loc[:, 'PSD'] = total_2019_s['PSD'] + total_2019_s['PSD/CDS-PP']
            total_2019_s = total_2019_s.drop(['PSD/CDS-PP'], axis=1)
    elif whatif_partidos == 'PaF2019':
        total_2019_s = total_2019.copy()
        ilhas = total_2019_s.index.isin(['Açores','Madeira'])
        total_2019_s['PaF'] = 0
        total_2019_s.loc[~ilhas, 'PaF'] = total_2019_s['PSD'] + total_2019_s['CDS-PP']
        total_2019_s.loc[~ilhas, ['PSD', 'CDS-PP']] = 0     
        colunas = list(total_2019_s.columns)
        colunas = [colunas[0]] + [colunas[-1]] + colunas[1:-1]
        total_2019_s = total_2019_s[colunas]
    elif whatif_partidos == 'PaF2015':
        total_2019_s = total_2019.copy()
        ilhas = total_2019_s.index.isin(['Açores','Madeira'])
        total_2019_s['PaF'] = 0
        total_2019_s.loc[~ilhas, 'PaF'] = total_2019_s['PSD'] + total_2019_s['CDS-PP'] + total_2019_s['Aliança']  + total_2019_s['Chega']
        total_2019_s.loc[~ilhas, ['PSD', 'CDS-PP']] = 0    
        total_2019_s.loc[ilhas, 'PSD'] =  total_2019_s['PSD'] + total_2019_s['Aliança']  + total_2019_s['Chega']        
        total_2019_s = total_2019_s.drop(['Aliança','Chega'], axis=1) 
        colunas = list(total_2019_s.columns)
        colunas = [colunas[0]] + [colunas[-1]] + colunas[1:-1]
        total_2019_s = total_2019_s[colunas]
    elif whatif_partidos == 'PSD2015':
        total_2019_s = total_2019.copy()
        total_2019_s.loc[:, 'PSD2015'] = total_2019_s['PSD'] + total_2019_s['Aliança']  + total_2019_s['Chega'] 
        total_2019_s = total_2019_s.drop(['Aliança','Chega','PSD'], axis=1) 
        colunas = list(total_2019_s.columns)
        colunas = [colunas[0]] + [colunas[-1]] + colunas[1:-1]
        total_2019_s = total_2019_s[colunas]
    elif whatif_partidos == 'PSD/CDS-PP':
        total_2019_s = total_2019.copy()
        if ano == 2022:
            total_2019_s.loc[:, 'PSD+CDS'] = total_2019_s['PSD'] + total_2019_s['CDS-PP']  + total_2019_s['PSD/CDS-PP']
            total_2019_s = total_2019_s.drop(['CDS-PP','PSD','PSD/CDS-PP'], axis=1)
        else:
            total_2019_s.loc[:, 'PSD+CDS'] = total_2019_s['PSD'] + total_2019_s['CDS-PP']
            total_2019_s = total_2019_s.drop(['CDS-PP','PSD'], axis=1) 
        colunas = list(total_2019_s.columns)
        colunas = [colunas[0]] + [colunas[-1]] + colunas[1:-1]
        total_2019_s = total_2019_s[colunas]

    partidos = list(total_2019_s.columns[:-6])
    zzz = pd.DataFrame(columns=partidos)

    if whatif_distritos == 'distritos_8':

        total_2019_s.loc['Alentejo'] = total_2019_s.loc['Beja'] + total_2019_s.loc['Évora'] + total_2019_s.loc['Portalegre']        
        total_2019_s.loc['Tras-os-Montes'] = total_2019_s.loc['Vila Real'] + total_2019_s.loc['Bragança']        
        total_2019_s.loc['Beira Interior'] = total_2019_s.loc['Guarda'] + total_2019_s.loc['Castelo Branco']

        circulos_s = circulos
        circulos_s.remove('Évora')
        circulos_s.remove('Beja')
        circulos_s.remove('Portalegre')
        circulos_s.remove('Guarda')
        circulos_s.remove('Bragança')
        circulos_s.remove('Vila Real')

        circulos_s.remove('Castelo Branco')    
        circulos_s.append('Alentejo')
        circulos_s.append('Tras-os-Montes')
        circulos_s.append('Beira Interior')

        total_2019_s = total_2019_s.loc[circulos_s]

    elif whatif_distritos == 'grandes':

        total_2019_s.loc['Sul'] = (total_2019_s.loc['Beja'] + total_2019_s.loc['Évora'] +
                                total_2019_s.loc['Faro'] + total_2019_s.loc['Setúbal']) 
        total_2019_s.loc['Norte'] = (total_2019_s.loc['Braga'] + total_2019_s.loc['Viana do Castelo'] + 
                                    total_2019_s.loc['Vila Real'] + total_2019_s.loc['Bragança']) 
        total_2019_s.loc['Centro 1'] = (total_2019_s.loc['Aveiro'] + total_2019_s.loc['Viseu'] + 
                                    total_2019_s.loc['Coimbra'] ) 
        total_2019_s.loc['Centro 2'] = (total_2019_s.loc['Santarém'] + total_2019_s.loc['Castelo Branco'] + 
                                    total_2019_s.loc['Leiria'] + total_2019_s.loc['Portalegre'] 
                                        +  total_2019_s.loc['Guarda']  ) 
                                    
        circulos_s = circulos
        circulos_s.remove('Évora')
        circulos_s.remove('Beja')
        circulos_s.remove('Portalegre')
        circulos_s.remove('Braga')
        circulos_s.remove('Guarda')
        circulos_s.remove('Bragança')
        circulos_s.remove('Vila Real')
        circulos_s.remove('Viana do Castelo')        
        circulos_s.remove('Castelo Branco')
        circulos_s.remove('Setúbal')
        circulos_s.remove('Viseu')
        circulos_s.remove('Faro')
        circulos_s.remove('Santarém')
        circulos_s.remove('Coimbra')
        circulos_s.remove('Leiria')
        circulos_s.remove('Aveiro')  
        circulos_s.append('Centro 1')
        circulos_s.append('Centro 2')
        circulos_s.append('Sul')
        circulos_s.append('Norte')
    #    for circ in circulos_s:
    #        z = dHondt(total_2019_s.loc[circ][:-5].values, total_2019_s.loc[circ][-2])
    #        total +=z
    #        zzz.loc[circ] = z

            #print(circ,z)
        total_2019_s = total_2019_s.loc[circulos_s]

    total = 0
    circulos = list(total_2019_s.index)

    if whatif_circulos == '2019':

        if ano == 2022:
            wasted_df = pd.DataFrame()
            for circ in circulos:
                votos = total_2019_s.loc[circ][:-6].values
                z,q = dHondt(votos, total_2019_s.loc[circ]['lug_2022'])

                for j in range(len(z)):
                    q_temp = q.copy()
                    if z[j] == 0:
                        wasted_df.loc[circ,partidos[j]] = int(votos[j])
                    else:
                        q_temp = np.delete(q_temp,j)
                        needed_votes = max(np.ceil(q_temp.max()*z[j]),q_temp.max()*z[j]+1)
                        wasted_df.loc[circ,partidos[j]] = int(votos[j] - needed_votes)

                total += z
                zzz.loc[circ] = z
            
        else:
            wasted_df = pd.DataFrame()
            for circ in circulos:
                votos = total_2019_s.loc[circ][:-6].values
                z,q = dHondt(total_2019_s.loc[circ][:-6].values, total_2019_s.loc[circ]['lug_2019'])

                for j in range(len(z)):
                    q_temp = q.copy()
                    if z[j] == 0:
                        wasted_df.loc[circ,partidos[j]] = int(votos[j])
                    else:
                        q_temp = np.delete(q_temp,j)
                        needed_votes = max(np.ceil(q_temp.max()*z[j]),q_temp.max()*z[j]+1)
                        wasted_df.loc[circ,partidos[j]] = int(votos[j] - needed_votes)

                total += z
                zzz.loc[circ] = z
        wasted_df = wasted_df.astype(int)
        wasted_df['TOTAL'] = wasted_df.sum(axis=1)

        wasted_df['VOTOS'] = total_2019_s.iloc[:,:-6].sum(axis=1)
        wasted_df.loc['TOTAL'] = wasted_df.sum()
        wasted_df.loc['VOTOS'] = total_2019_s.iloc[:,:-6].sum()
        wasted_df = wasted_df.fillna(0)        

    elif whatif_circulos == '2015':
        for circ in circulos:
            z,_= dHondt(total_2019.loc[circ][:-6].values, total_2019.loc[circ]['lug_2015'])
            zzz.loc[circ] = z
            total += z
    #elif whatif_circulos == 'circulo unico':
    #    total_2019_s = total_2019.copy()
    #    total = dHondt(total_2019_s.sum()[:-5].values, 226)

    elif whatif_circulos == 'circulo unico':
        soma = total_2019_s.sum(axis=0)  
        tot = soma[:-6].sum()
        soma.loc[soma/tot < barreira/100] = 0
        soma = soma[:-6]
    #   print(soma)
        wasted_df = pd.DataFrame()
        if ano == 2022:     
            total,q = dHondt(soma.values,230)
        else:
            total,q = dHondt(soma.values,230)

        for j in range(len(soma.values)):
                    q_temp = q.copy()
                    if total[j] == 0:
                        wasted_df.loc[partidos[j]] = soma[j]
                    else:
                        q_temp = np.delete(q_temp,j)
                        needed_votes = max(np.ceil(q_temp.max()*total[j]),q_temp.max()*total[j]+1)
                        wasted_df.loc[partidos[j],'votos desperdicados'] = int(soma.values[j] - needed_votes)
        


 

    elif whatif_circulos == 'misto':

        for circ in circulos:
            z,_ = dHondt(total_2019_s.loc[circ][:-6].values, total_2019_s.loc[circ]['misto'])
            zzz.loc[circ] = z
            total += z
        soma = total_2019_s.sum(axis=0)  
        tot = soma[:-6].sum()
        soma.loc[soma/tot < barreira/100] = 0
        soma = soma[:-6]
        #print(soma)
        p =soma.div(total+1).values
    # print(p)
        total += dHondt(p, sup)[0]        
        zzz.loc['Compensação'],_ = dHondt(p, sup)
        #total_2019_s = total_2019_s.drop('misto', axis=1)  
    
    
    zzz.loc['TOTAL'] = zzz.sum()
    yyy=zzz.astype(int)
    yyy = yyy.loc[:, (yyy != 0).any(axis=0)]    
    yyy['TOTAL'] = yyy.sum(axis=1)
    #yyy = yyy.iloc[yyy.loc['TOTAL'] > 0]
    #st.write(yyy.loc['TOTAL'] > 0)
    
    mand = pd.DataFrame(partidos, columns=['Partido'])
    mand['Votos'] = list(total_2019_s.sum()[:-6])
    tot = total_2019_s.sum()[:-4].sum()
    mand['Pct'] = (mand['Votos']/tot*100).map('{:,.2f}'.format)
    mand['Pct Validos'] = (100*mand['Votos']/mand['Votos'].sum()).map('{:,.2f}'.format)
    mand['Mandatos'] = total.astype(int)
    if ano == 2022:
        mand['Pct Mandatos'] = (100*mand['Mandatos']/230).map('{:,.2f}'.format)
    else:
        mand['Pct Mandatos'] = (100*mand['Mandatos']/230).map('{:,.2f}'.format)

    st.subheader('Total')
    st.write(mand.sort_values(by='Votos',ascending=False).style.hide(axis='index').format({'Votos':'{:,.0f}'}))

    st.write('Loosemore–Hanby index (LHI): ', 
       round((50*(abs(0.01*mand['Pct Validos'].astype(float)-0.01*mand['Pct Mandatos'].astype(float))).sum()),2),'%')
    #st.write('Obs: em 2022 como os círculos do exterior ainda não foram apurados, todas \
    #as percentagens e cálculos de proporcionalidade utilizam 226 mandatos como referência.')   

    if whatif_circulos == 'circulo unico':
        pass
    else:
        st.subheader('Distribuição pelos círculos eleitorais')
        st.write(yyy)

    if 'wasted_df' in locals():
        st.subheader('Análise de Votos Desperdiçados')

        if whatif_circulos == 'circulo unico':

            df1 = pd.DataFrame()
            df1 = wasted_df
            
            df1['aux'] = total_2019_s.sum()
            df1['Pct do total'] = 100*df1['votos desperdicados']/df1['aux']

            kapa1 = round(100*int(df1['votos desperdicados'].sum())/int(df1['aux'].sum()),1)
            st.markdown('##### Foram desperdiçados ' + str(int(df1['votos desperdicados'].sum())) + ' ('+str(kapa1)+ '%) dos \
            '+str(int(df1['aux'].sum()))+' votos válidos depositados')
            st.write(df1[['votos desperdicados', 'Pct do total']].dropna().sort_values(by='Pct do total', ascending=True).style.format({'votos desperdicados':'{:,.0f}',
                                                                                                'Pct do total':'{:,.1f}'}))

        
        else:

            df1 = pd.DataFrame()
            df1['votos desperdicados'] = wasted_df.iloc[:-2,:-2].sum(axis=1)
            df1['Pct do total'] = (100*wasted_df['TOTAL']/wasted_df['VOTOS'])


            kapa1 = round(100*int(df1['votos desperdicados'].sum())/int(wasted_df.loc['TOTAL','VOTOS'].sum()),1)
            st.markdown('##### Foram desperdiçados ' + str(int(df1['votos desperdicados'].sum())) + ' ('+str(kapa1)+ '%) dos \
            '+str(int(wasted_df.loc['TOTAL','VOTOS'].sum()))+' votos válidos depositados')
            st.markdown('###### Por círculo eleitoral')
            st.write(df1.dropna().sort_values(by='Pct do total', ascending=True).style.format({'votos desperdicados':'{:,.0f}',
                                                                                                'Pct do total':'{:,.1f}'}))
            st.markdown('###### Por partido político')

            df2 = pd.DataFrame()
            df2['votos desperdicados'] = wasted_df.iloc[:-2,:-2].sum()
            df2['Pct do total'] = 100*wasted_df.loc['TOTAL']/wasted_df.loc['VOTOS']
            st.write(df2.sort_values(by='Pct do total', ascending=True).style.format({'votos desperdicados':'{:,.0f}',
                                                                                                        'Pct do total':'{:,.1f}'}))