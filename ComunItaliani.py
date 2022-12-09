import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Comuni():
    def __init__(self):
        try:
            residenti = pd.read_csv("./Data/POSAS_2020_it_Comuni.csv", sep=";")
            strDF = pd.read_csv("./Data/STRASA_2020_it_Comuni.csv", sep=";")
            redditi = pd.read_csv("./Data/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2020.csv",
                                       sep=";")
            residenti.drop(residenti[residenti["Età"] != 999].index, inplace=True)
            popDF = pd.DataFrame(residenti[["Codice comune", "Comune", "Totale"]])
            popDF.rename(columns={'Totale': 'TotResidenti'}, inplace=True)

            strDF.drop(strDF[strDF["Età"] != 999].index, inplace=True)
            strDF["TotStranieri"] = strDF["Maschi"] + strDF["Femmine"]
            strDF.drop(columns=["Età", "Maschi", "Femmine"], inplace=True)

            popolazione = pd.merge(popDF, strDF, how='outer',
                                   left_on=["Codice comune", "Comune"], right_on=["Codice comune", "Comune"])
            popolazione["%Stranieri"] = ((popolazione["TotStranieri"] * 100) / popolazione["TotResidenti"]).round(2)
            popolazione["Comune"] = popolazione["Comune"].str.upper()

            reddDF = pd.DataFrame(redditi[["Codice catastale", "Codice Istat Comune", "Denominazione Comune",
                                           "Sigla Provincia", "Regione", "Codice Istat Regione",
                                           "Numero contribuenti", "Reddito imponibile - Ammontare in euro"]])
            reddDF["RedditoMedio"] = (
                    reddDF["Reddito imponibile - Ammontare in euro"] / reddDF["Numero contribuenti"]).round(2)
            reddDF.rename(columns={"Codice Istat Comune": "Codice comune", "Denominazione Comune": "Comune",
                                   "Sigla Provincia": "Provincia", "Codice Istat Regione": "Codice regione",
                                   "Reddito imponibile - Ammontare in euro": "RedditoTotale"}, inplace=True)

            comuniDF = pd.merge(reddDF, popolazione, how='outer',
                                left_on=["Codice comune", "Comune"], right_on=["Codice comune", "Comune"])
            comuniDF["Comune"] = comuniDF["Comune"].str.upper()
            comuniDF["%Occupati"] = ((comuniDF["Numero contribuenti"] * 100) / comuniDF["TotResidenti"]).round(2)
            comuniDF.drop(comuniDF.tail(302).index, inplace=True)
            self.comuniDF = comuniDF
        except Exception as eccezione:
            print("Errore nel percorso dei file... \nSostituirlo con quello corretto!")
            print(eccezione)

    def _salvaFile(self):
        while True:
            try:
                pathFinale = input('\nInserisci il percorso in cui verrà archiviato il file Excel '
                                   '\ndefault: C:/Users/JacopoAndreaSardelli/Downloads/ComuniDF.xlsx'
                                   '\n   >>: ')
                self.comuniDF.to_excel(pathFinale)
                print("\nSalvataggio completato con successo :)")
                break
            except Exception as errore:
                print(f"Errore nel salvataggio dei dati ...\n {errore}")

    def _infoDataset(self):
        print(f'\nMatrice delle correlazioni \n{self.comuniDF.corr().round(2)}')
        print(f'\nDescrizione del Dataset \n {self.comuniDF.describe().round(2).to_string()}')

    def _infoComuni(self):
        while True:
            try:
                selezionaComune = input('\nInserisci un Comune >>: \n')
                comuneCorrente = (self.comuniDF.loc[self.comuniDF['Comune'] == selezionaComune.upper()])
                for (colname, colval) in comuneCorrente.iteritems():
                    print(colname, ":   ",colval.values.squeeze())
                break
            except:
                print('Errore nel comune inserito. Riprovare')

    def _grafici(self):
        sns.displot(self.comuniDF, x="RedditoMedio")
        plt.title('Distribuzione del Reddito nei Comuni Italiani nel 2020')
        plt.xlabel("Reddito Medio")
        plt.ylabel("Numero di Comuni Italiani")
        plt.xlim(left=0, right=45000)
        medianaReddito = self.comuniDF["RedditoMedio"].median()
        print("\nMediana:  ",medianaReddito)
        plt.axvline(x=medianaReddito, color="black")
        plt.show()

        sns.scatterplot(data=self.comuniDF, x="%Occupati", y="RedditoMedio")
        plt.title('Correlazione tra la percentuale di Occupati e il Reddito medio nel 2020')
        plt.ylabel("Reddito Medio")
        plt.xlabel("Percentuale di persone occupate")
        plt.xlim(left=0,right=100)
        plt.ylim(bottom=0,top=45000)
        plt.show()

        sns.scatterplot(data=self.comuniDF, x="%Stranieri", y="RedditoMedio")
        plt.title('Correlazione tra gli Stranieri residenti e il Reddito medio nel 2020')
        plt.ylabel("Reddito Medio")
        plt.xlabel("Percentuale di Stranieri residenti")
        plt.xlim(left=0,right=100)
        plt.ylim(bottom=0, top=45000)
        plt.show()

        sns.heatmap(self.comuniDF.corr(), cmap="YlGnBu", annot=True, fmt=".2f", square=True)
        plt.title('HeatMap delle Correlazioni')
        plt.show()

    def _ErroreComando(self):
        print('\nErrore, il numero inserito non corrisponde a nessuna operazione... \nRiprova!')

    def menu(self):
        print("BENVENUTO :)")
        try:
            while True:
                inputUtente = int(input('\nMENU \n0. Terminare il programma '
                                        '\n1. Salvare i dati in Excel '
                                        '\n2. Informazioni generali sul Dataset'
                                        '\n3. Informazioni sui Comuni Italiani'
                                        '\n4. Grafici'
                                        '\n>>: '))
                if inputUtente == 0:
                    print('\nARRIVEDERCI!')
                    break
                azioni = {1:self._salvaFile,2:self._infoDataset, 3:self._infoComuni, 4:self._grafici}
                azioni.get(inputUtente,self._ErroreComando)()
        except Exception as err:
            print(f'\nErrore, comando non valido! \n  {err}')

    def __str__(self):
        return 'Programma per analizzare alcune statistiche dei Comuni Italiani nel 2020'



if __name__ == "__main__":
    start = Comuni()
    start.menu()