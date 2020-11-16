import pandas as pd
from IPython.core.display import HTML
import streamlit as st


###App
def main():
    """ Stock APP """
    ##General Settings
    st.set_page_config(page_title='CLUE - Crowdinvesting Rechner', page_icon='logo.jpg')
    
    st.success('Diversifikationsrechner - Rechne deine Investition durch')

    col1, col2 = st.beta_columns([1,3])

    with col1:
        pd.set_option('display.precision', 2)
        ##Eingabefelder
        eur = st.text_input('Investitonshöhe in EUR:', 500)
        i = st.text_input('Erwartete Rendite in %:', 5.0)
        years = st.text_input('Laufzeit d. Projekts (Jahre):', 3)

        ##Input
        in_years = [years]
        year = pd.DataFrame(in_years, dtype=int)
        year += 1
        in_eur = [eur]
        in_ret = [i]

        ##Convert and Calculation
        df_ret = pd.DataFrame(in_ret, dtype=float)

        intt = round(df_ret.astype(float) * (1 - (0.25 * (1 + 0.055))), 2)
        int_netto = pd.DataFrame(intt, dtype=float)

        df2 = pd.DataFrame(1, columns=['Jahresanfang', 'Zinssatz netto', 'Anlagebetrag-Entwicklung'], index=range(year[0][0].astype(int)))
        df2.reset_index()
        df2.index += 0
        df3 = df2.reset_index().rename(columns={'index': 'Jahr'})
        df3.Jahresanfang = in_eur[0]
        df3['Zinssatz netto'] = int_netto[0][0]
        df3['Anlagebetrag-Entwicklung'] = round(df3['Jahresanfang'].astype(int) / ((1 + int_netto[0][0].astype(float) / 100) ** (df3['Jahr'][0].astype(int) - df3['Jahr'].astype(int))), 2)
        df3['Zinsen p.a.'] = df3['Anlagebetrag-Entwicklung'].diff().fillna(0)
        df_out = df3[['Jahr','Anlagebetrag-Entwicklung', 'Zinsen p.a.']].set_index('Jahr')
        
        df_Zins = 'Zinsertrag (netto) über Projektaufzeit: ' + round(df_out['Zinsen p.a.'].sum(), 2).astype(str) + ' EUR'
        df_risk = 'Die Investition in ' + round(1 / (int_netto / 100), 2).astype(str) + ' Projekte kompensiert ein Ausfall.'
        df_invest = 'Dies bedeutet, dass du ' + (df3['Jahresanfang'].astype(int) * round(1 / (int_netto[0][0] / 100), 2)).astype(str) + ' EUR in verschiedene Projekte investieren müsstest.'

    
    with col2:
        st.table(df_out)
    
    #st.bar_chart(df_out['Zinsen p.a.'])
        
    st.text(df_Zins)
    st.text('Der Zinsertrag (netto) berücksichttigt Abgeltungssteuer und Soli, aber keinen Steuerfreibetrag')
    st.text(df_risk[0][0])
    st.text(df_invest[0])
    
        
    
    
    
    # with col1:
    #     in_eur = st.text_input('Investitonshöhe in €:', 500)
    #     in_return = st.text_input('Erwartete Rendite in %:', 5.0)

    #     res = in_return * (1 - (0.25 * (1 + 0.055)))
    #     st.text('Rendite n. Steuern:', res + ' %')

if __name__ == '__main__':
    main() 