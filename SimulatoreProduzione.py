import random

class SimulatoreProduzione:
    def __init__(self,lista_prodotti):
        self.prodotti = lista_prodotti
        self.quantita = {}
        self.ore_richieste_per_unita = {}
        self.capacita_giornaliera_prodotti = {}
        
    def genera_quantita(self, min_quantita_prodotto, max_quantita_prodotto):
        # Generazione delle quantità da produrre
        for prodotto in self.prodotti:
            self.quantita[prodotto] = random.randint(min_quantita_prodotto, max_quantita_prodotto)
        
    def genera_parametri(self, min_ore_per_unita_prodotto, max_ore_per_unita_prodotto, min_capacita_prodotto, max_capacita_prodotto, min_capacita_totale, max_capacita_totale, min_ore_ritardo_per_approvvigionamento, max_ore_ritardo_per_approvvigionamento):
        # Generazione dei tempi di produzione per ogni unita di prodotto
        for prodotto in self.prodotti:
           self.ore_richieste_per_unita[prodotto] = round(random.uniform(min_ore_per_unita_prodotto, max_ore_per_unita_prodotto), 2) 
        
        # Generazione delle capacità giornaliere massime di ogni prodotto
        for prodotto in self.prodotti:
            self.capacita_giornaliera_prodotti[prodotto] = random.randint(min_capacita_prodotto, max_capacita_prodotto)
        
        # Generazione della capacità giornaliera complessiva dell'azienda
        self.capacita_giornaliera_complessiva = random.randint(min_capacita_totale, max_capacita_totale)

        # Generazione delle ore di ritardo per l'approvvigionamento delle materie prime
        self.ore_ritardo_per_approvvigionamento = round(random.uniform(min_ore_ritardo_per_approvvigionamento, max_ore_ritardo_per_approvvigionamento),2)

    def simula_guasto(self, prodotto, min_probabilita_guasto, max_probabilita_guasto, min_ore_di_fermo, max_ore_di_fermo):
        probabilita_guasto = random.uniform(min_probabilita_guasto, max_probabilita_guasto)
        ore_di_fermo = round(random.uniform(min_ore_di_fermo,max_ore_di_fermo),2)
        if random.random() < probabilita_guasto:  
            print(f"\nGuasto durante la produzione di {prodotto}! Aggiunto un fermo di {ore_di_fermo} ore.")
            return ore_di_fermo
        return 0 # nessun guasto

    def calcola_tempo_produzione(self, min_probabilita_guasto, max_probabilita_guasto, min_ore_di_fermo, max_ore_di_fermo):
        
        # Calcolo dei giorni minimi necessari per ciascun prodotto in base al proprio vincolo di capacità giornaliera
        giorni_per_prodotto = {}
        for prodotto in self.prodotti:
            giorni_per_prodotto[prodotto] = self.quantita[prodotto] / self.capacita_giornaliera_prodotti[prodotto]
        # Essendo la produzione in parallelo, consideriamo quello più lento
        giorni_minimi_per_prodotto = max(giorni_per_prodotto.values())
        
        # Calcolo dei giorni minimi necessari per produrre il lotto in base al vincolo di capacità complessiva giornaliera
        giorni_minimi_per_capacita_complessiva = (sum(self.quantita.values()) / self.capacita_giornaliera_complessiva)

        # Calcolo del tempo totale di produzione in ore 
        ore_totali_per_prodotto = {}
        for prodotto in self.prodotti:
            ore_totali_per_prodotto[prodotto] = self.quantita[prodotto] * self.ore_richieste_per_unita[prodotto]
        
        # Simulazione di un guasto e aggiornamento dei tempi 
        for prodotto in self.prodotti:
            ore_di_fermo = self.simula_guasto(prodotto, min_probabilita_guasto, max_probabilita_guasto, min_ore_di_fermo, max_ore_di_fermo)
            ore_totali_per_prodotto[prodotto] += ore_di_fermo
            
        # Il numero di giorni totali effettivi di produzione del lotto è dato dal tempo di produzione del prodotto più lento
        giorni_effettivi_produzione_lotto = max(ore_totali_per_prodotto.values()) / 24
        
        return giorni_minimi_per_capacita_complessiva, giorni_minimi_per_prodotto, giorni_effettivi_produzione_lotto

    def stampa_configurazione(self):
        print("Quantità di produzione per prodotto:")
        for prodotto in self.prodotti:
            print(f"  {prodotto}: {self.quantita[prodotto]} unità")

        print("\nParametri di produzione:")
        print("  Tempi per unità (ore):")
        for prodotto in self.prodotti:
            print(f"    {prodotto}: {self.ore_richieste_per_unita[prodotto]} ore/unità")
        print("\nCapacità giornaliera per prodotto (unità):")
        for prodotto in self.prodotti:
            print(f"    {prodotto}: {self.capacita_giornaliera_prodotti[prodotto]} unità/giorno")
        print(f"\nCapacità giornaliera complessiva: {self.capacita_giornaliera_complessiva} unità/giorno")
    
    def verifica_parametri(self,parametri: dict):
        
        if len(self.prodotti) != 3 :
            raise ValueError("Il numero di prodotti deve essere 3")
        else :
            for i in range(len(self.prodotti)):
                if len(self.prodotti[i]) == 0 :
                    raise ValueError("Nome del prodotto " + str(i+1) + " non valido")
              
        # Lista dei parametri che devono essere >= 0
        parametri_non_negativi = [
            "min_quantita_prodotto", "max_quantita_prodotto",
            "min_ore_per_unita_prodotto", "max_ore_per_unita_prodotto",
            "min_capacita_prodotto", "max_capacita_prodotto",
            "min_capacita_totale", "max_capacita_totale",
            "min_ore_di_fermo", "max_ore_di_fermo",
            "min_ore_ritardo_per_approvvigionamento", "max_ore_ritardo_per_approvvigionamento"
        ]

        # Lista dei parametri che devono essere compresi tra 0 e 1 
        parametri_probabilita = ["min_probabilita_guasto", "max_probabilita_guasto"]
        
        # Verifica che tutti i parametri siano >= 0
        for chiave in parametri_non_negativi:
          if parametri[chiave] < 0:
             raise ValueError(f"Errore: {chiave} deve essere >= 0. Valore trovato: {parametri[chiave]}")

         # Verifica che le probabilità siano tra 0 e 1
        for chiave in parametri_probabilita:
            if not (0 <= parametri[chiave] <= 1):
                raise ValueError(f"Errore: {chiave} deve essere tra 0 e 1. Valore trovato: {parametri[chiave]}")

        # Verifica che min ≤ max per ogni coppia di parametri
        coppie_min_max = [
            ("min_quantita_prodotto", "max_quantita_prodotto"),
            ("min_ore_per_unita_prodotto", "max_ore_per_unita_prodotto"),
            ("min_capacita_prodotto", "max_capacita_prodotto"),
            ("min_capacita_totale", "max_capacita_totale"),
            ("min_probabilita_guasto", "max_probabilita_guasto"),
            ("min_ore_di_fermo", "max_ore_di_fermo"),
            ("min_ore_ritardo_per_approvvigionamento", "max_ore_ritardo_per_approvvigionamento"),
        ]

        for chiave_min, chiave_max in coppie_min_max:
            if parametri[chiave_min] > parametri[chiave_max]:
                raise ValueError(f"Errore: {chiave_min} ({parametri[chiave_min]}) deve essere ≤ {chiave_max} ({parametri[chiave_max]})")


    def simula(self, parametri: dict):
        # Verifica dei parametri
        self.verifica_parametri(parametri)

        # Estrazione dei parametri 
        min_quantita_prodotto = parametri["min_quantita_prodotto"]
        max_quantita_prodotto = parametri["max_quantita_prodotto"]
        min_ore_per_unita_prodotto = parametri["min_ore_per_unita_prodotto"]
        max_ore_per_unita_prodotto = parametri["max_ore_per_unita_prodotto"]
        min_capacita_prodotto = parametri["min_capacita_prodotto"]
        max_capacita_prodotto = parametri["max_capacita_prodotto"]
        min_capacita_totale = parametri["min_capacita_totale"]
        max_capacita_totale = parametri["max_capacita_totale"]
        min_probabilita_guasto = parametri["min_probabilita_guasto"]
        max_probabilita_guasto = parametri["max_probabilita_guasto"]
        min_ore_di_fermo = parametri["min_ore_di_fermo"]
        max_ore_di_fermo = parametri["max_ore_di_fermo"]
        min_ore_ritardo_per_approvvigionamento = parametri["min_ore_ritardo_per_approvvigionamento"]
        max_ore_ritardo_per_approvvigionamento = parametri["max_ore_ritardo_per_approvvigionamento"]

        # Generazione delle quantita e parametri
        self.genera_quantita(min_quantita_prodotto, max_quantita_prodotto)
        self.genera_parametri(min_ore_per_unita_prodotto, max_ore_per_unita_prodotto, min_capacita_prodotto, max_capacita_prodotto, min_capacita_totale, max_capacita_totale, min_ore_ritardo_per_approvvigionamento, max_ore_ritardo_per_approvvigionamento)
        
        # Stampa dei parametri di configurazione
        self.stampa_configurazione()

        # Calcolo del tempo totale in ore e il numero  di giorni
        giorni_minimi_per_capacita_complessiva, giorni_minimi_per_prodotto, giorni_effettivi_produzione_lotto = self.calcola_tempo_produzione(min_probabilita_guasto, max_probabilita_guasto, min_ore_di_fermo, max_ore_di_fermo)

        # Output della simulazione
        tempo_totale_produzione_lotto = max(giorni_minimi_per_capacita_complessiva, giorni_minimi_per_prodotto, giorni_effettivi_produzione_lotto) 
        print("\nOutput:")
        print(f"  Giorni minimi rispettando il vincolo di capacità complessiva: {round(giorni_minimi_per_capacita_complessiva, 2)} giorni")
        print(f"  Giorni minimi rispettando il vincolo di capacità del prodotto : {round(giorni_minimi_per_prodotto, 2)} giorni")
        print(f"  Giorni effettivi produzione del lotto ipotizzando una produzione continua : {round(giorni_effettivi_produzione_lotto, 2)} giorni")
        if self.ore_ritardo_per_approvvigionamento == 0:
          print(f" Tenendo conto dei vari vincoli il tempo totale di produzione lotto è : {round(tempo_totale_produzione_lotto, 2)} giorni")
        else :
            print(f" Tenendo conto dei vari vincoli e del ritardo dovuto all'approvvigionamento ({round(self.ore_ritardo_per_approvvigionamento / 24,2)} giorni) il tempo totale di produzione lotto è : {round(tempo_totale_produzione_lotto + self.ore_ritardo_per_approvvigionamento / 24, 2)} giorni")
        
if __name__ == "__main__":

    simulatore = SimulatoreProduzione(["ProdottoA","ProdottoB", "ProdottoC"])
     
    scenario_favorevole = {
        "min_quantita_prodotto": 10,
        "max_quantita_prodotto": 20,
        "min_ore_per_unita_prodotto": 1,
        "max_ore_per_unita_prodotto": 3,
        "min_capacita_prodotto": 15,
        "max_capacita_prodotto": 30,
        "min_capacita_totale": 20,
        "max_capacita_totale": 40,
        "min_probabilita_guasto": 0.01,
        "max_probabilita_guasto": 0.05,
        "min_ore_di_fermo": 0.1,
        "max_ore_di_fermo": 0.3,
        "min_ore_ritardo_per_approvvigionamento": 1,
        "max_ore_ritardo_per_approvvigionamento": 3
        }

    scenario_intermedio = {
        "min_quantita_prodotto": 10,
        "max_quantita_prodotto": 20,
        "min_ore_per_unita_prodotto": 2,
        "max_ore_per_unita_prodotto": 5,
        "min_capacita_prodotto": 10,
        "max_capacita_prodotto": 20,
        "min_capacita_totale": 15,
        "max_capacita_totale": 25,
        "min_probabilita_guasto": 0.1,
        "max_probabilita_guasto": 0.2,
        "min_ore_di_fermo": 2,
        "max_ore_di_fermo": 4,
        "min_ore_ritardo_per_approvvigionamento": 8,
        "max_ore_ritardo_per_approvvigionamento": 18
        }

    scenario_sfavorevole = {
        "min_quantita_prodotto": 10,
        "max_quantita_prodotto": 20,
        "min_ore_per_unita_prodotto": 5,
        "max_ore_per_unita_prodotto": 10,
        "min_capacita_prodotto": 5,
        "max_capacita_prodotto": 10,
        "min_capacita_totale": 10,
        "max_capacita_totale": 20,
        "min_probabilita_guasto": 0.2,
        "max_probabilita_guasto": 0.5,
        "min_ore_di_fermo": 3,
        "max_ore_di_fermo": 6,
        "min_ore_ritardo_per_approvvigionamento": 12,
        "max_ore_ritardo_per_approvvigionamento": 24
        }
    
    # Avvio della simulazione
    simulatore.simula(scenario_sfavorevole)
    