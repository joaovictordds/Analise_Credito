import streamlit as st
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

paginas = ['Home','Modelo - Liberação de Crédito']

pagina = st.sidebar.radio('Navegue por aqui:', paginas)

if pagina == 'Home':
    st.title('Meus modelos em produção :gem:')
    
if pagina == 'Modelo - Liberação de Crédito':
      
    subpag = ['Liberação de crédito'] #'Sugestão de quantia' 
    pag = st.sidebar.selectbox('Selecione o modelo:', subpag)
    
    if pag == 'Liberação de crédito':
          
        modelo = joblib.load('modelo_boosting.pkl')
        st.title('LIberação de crédito')
        st.markdown('---')
        
        st.write('Parcelamento: ')
        duração = st.number_input('Meses', 18, 65, 18)
        
        st.write('Selecione a idade entre 18 e 65 anos:')
        idade = st.number_input('Idade', 18, 65, 18)
        
        st.write('Garantias:')
        gar = ['nenhum','fiador','co-aplicante']
        garantia = st.selectbox('Garantias', gar) 
        
        st.write('Histórico do cliente:')
        his = ['pagamento em dia','conta crítica','já atrasou pagamentos','creditos quitados','primeira vez']
        historico = st.selectbox('Historico', his)
        
        st.write('Saldo na conta:')
        saldo = ['sem conta','negativo','ate 200','200+']
        conta = st.selectbox('Valor', saldo)
        
        input0 = {'Meses':[duração], 'Idade':[idade], 'Garantias':[garantia], 'Historico':[historico],'Valor':[conta]}
        input = pd.DataFrame(input0)
        
        st.markdown('---')
        
        if st.button('Executar'):
            previsao_novos_dados = modelo.predict(input)
            saida = []
            #saida = previsao_novos_dados
            if previsao_novos_dados == 0:
                saida = 'Não aprovar novo crédito'
            else:
                saida= 'Aprovado'   
            st.subheader(saida)
            
    if pag == 'Sugestão de quantia':  
        
        modelo = joblib.load('modelo_regressao.pkl')     
        st.title('Sugestão de valor de liberação de crédito')
        st.write('O modelo a seguir sugere um valor aproximado para tomar de empréstimo.')
        st.markdown('---')
        
        st.write('**Cliente apto para um novo crédito?**')
        st.write('0: NAO | 1: SIM')
        apto = st.selectbox('Creditability', [0,1])
        
        st.write('Saldo atual do cliente:')
        saldo = st.number_input('Account_Balance', 0, 100000, 250)
        
        st.write('Quantidade de parcelas:')
        parcelas = st.number_input('Duration_of_Credit_monthly', 0, 200, 12)
        
        st.write('**Tempo de Serviço:** **0** - Menos de 1 ano, **1:** 1 a 4 anos **2:** 4 a 7 anos **3:** 7 ou mais')
        tempo_servico = st.selectbox('Length_of_current_employment', [0,1,2,3])
        
        st.write('**Sexo:**     0 - solteiro, 1 - casado 2- feminino')
        sexo = st.selectbox('Sex_Marital_Status',[0,1,2])
        
        st.write('Selecione a idade entre 18 e 65 anos:')
        idade = st.number_input('Age_years', 18, 65, 18)    
        
        st.write('Possui outros financiamentos')
        st.write('**0**: Outros bancos, **1:** Em lojas de departamento, **2:** nenhum')
        outros_cred = st. selectbox('No_of_Credits_at_this_Bank', [0,1,2])
         
        
        input0 = {'Creditability':[apto], 'Account_Balance':[saldo], 'Duration_of_Credit_monthly':[parcelas],
                  'Length_of_current_employment':[tempo_servico], 'Sex_Marital_Status':[sexo],
                  'Age_years':[idade], 'No_of_Credits_at_this_Bank':[outros_cred]}
        
        input = pd.DataFrame(input0)
        
        st.markdown('---')
        
        if st.button('Executar'):
            qtia = modelo.predict(input)
            st.subheader(f'Valor sugerido de $ {qtia.round(2)}')


        
            
