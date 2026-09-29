# Importa o NumPy para trabalhar com os dados numéricos da rede neural.
import numpy as np

# Importa o modelo de rede neural MLP.
from sklearn.neural_network import MLPClassifier

# Importa o recurso para normalizar os valores de entrada.
from sklearn.preprocessing import StandardScaler

# Importa Pipeline para juntar normalização + rede neural.
from sklearn.pipeline import Pipeline

# Importa time para criar intervalos entre as análises.
import time


# Cria a classe principal do nosso agente Purple Team.
class PurpleNeuralAgent:

    # Método executado quando criamos o agente.
    def __init__(self, target):

        # Guarda o endereço do laboratório que será analisado.
        self.target = target

        # Indica se o comportamento foi considerado suspeito.
        self.detected = False

        # Cria o modelo de inteligência artificial.
        self.model = self.create_model()


    # Cria e treina uma pequena rede neural.
    def create_model(self):

        # Dados fictícios de treinamento.
        #
        # Cada linha representa:
        # [quantidade_de_conexoes,
        #  quantidade_de_portas,
        #  pacotes_por_segundo,
        #  taxa_de_erro]
        X = np.array([
            [5, 1, 10, 0.01],
            [8, 2, 20, 0.02],
            [10, 2, 30, 0.01],
            [15, 3, 40, 0.03],

            [100, 20, 500, 0.30],
            [150, 30, 800, 0.50],
            [200, 40, 1200, 0.70],
            [300, 50, 2000, 0.90]
        ])

        # Classe 0 significa comportamento normal.
        # Classe 1 significa comportamento suspeito.
        y = np.array([
            0,
            0,
            0,
            0,
            1,
            1,
            1,
            1
        ])

        # Cria uma pipeline.
        #
        # Primeiro os dados são normalizados.
        # Depois passam pela rede neural.
        model = Pipeline([
            (
                "normalizador",
                StandardScaler()
            ),
            (
                "rede_neural",
                MLPClassifier(
                    hidden_layer_sizes=(10, 10),
                    activation="relu",
                    max_iter=2000,
                    random_state=42
                )
            )
        ])

        # Treina a rede neural com os exemplos.
        model.fit(X, y)

        # Retorna a rede já treinada.
        return model


    # Analisa um evento de rede.
    def analyze_event(self, connections, ports, packets, error_rate):

        # Monta os dados no mesmo formato utilizado durante o treinamento.
        evento = np.array([
            [
                connections,
                ports,
                packets,
                error_rate
            ]
        ])

        # Descobre a classe prevista pela rede neural.
        prediction = self.model.predict(evento)[0]

        # Obtém a probabilidade de o evento ser suspeito.
        probability = self.model.predict_proba(evento)[0][1]

        # Mostra os dados analisados.
        print("\n[*] Analisando evento...")
        print(f"[*] Conexões: {connections}")
        print(f"[*] Portas: {ports}")
        print(f"[*] Pacotes/s: {packets}")
        print(f"[*] Taxa de erro: {error_rate}")
        print(f"[*] Risco calculado: {probability:.2%}")

        # Verifica a decisão da rede neural.
        if prediction == 1:

            # Marca o evento como suspeito.
            self.detected = True

            # Mostra o resultado.
            print("[!] COMPORTAMENTO SUSPEITO DETECTADO.")

            # Envia para o motor de decisão.
            self.decision_engine(probability)

        else:

            # Marca o evento como normal.
            self.detected = False

            # Mostra o resultado.
            print("[+] Comportamento considerado normal.")


    # Decide o que fazer depois da classificação.
    def decision_engine(self, probability):

        # Risco extremamente alto.
        if probability >= 0.90:

            # Em vez de atacar o endereço, direcionamos o evento
            # para o honeypot do laboratório.
            print("[!!!] RISCO MUITO ALTO.")

            # Ação defensiva.
            self.redirect_to_honeypot()

        # Risco intermediário.
        elif probability >= 0.70:

            # Solicita investigação.
            print("[!] RISCO ALTO.")
            print("[*] Ação: INVESTIGAR EVENTO.")

        # Risco abaixo do limite.
        else:

            # Apenas registra o evento.
            print("[*] Ação: MONITORAR.")


    # Simula o redirecionamento para o honeypot.
    def redirect_to_honeypot(self):

        # Mostra que a decisão foi tomada.
        print("[HONEYPOT] Evento encaminhado para ambiente de deception.")

        # Aqui, no laboratório, podemos posteriormente
        # conectar essa função ao seu honeypot.
        print("[HONEYPOT] Registrando comportamento...")


    # Executa o ciclo principal do agente.
    def run_loop(self):

        # Mostra qual laboratório está sendo monitorado.
        print(f"[*] Purple Neural Agent iniciado.")
        print(f"[*] Ambiente: {self.target}")

        # Eventos simulados para treinamento/teste.
        eventos = [

            # Evento normal.
            (8, 2, 20, 0.02),

            # Evento normal.
            (12, 2, 30, 0.01),

            # Evento suspeito.
            (120, 25, 600, 0.40),

            # Evento muito suspeito.
            (250, 45, 1800, 0.80)
        ]

        # Percorre cada evento.
        for evento in eventos:

            # Envia o evento para a rede neural.
            self.analyze_event(
                evento[0],
                evento[1],
                evento[2],
                evento[3]
            )

            # Aguarda antes de analisar o próximo evento.
            time.sleep(2)


# Verifica se este arquivo está sendo executado diretamente.
if __name__ == "__main__":

    # Define o laboratório.
    #
    # Aqui você pode usar o nome do seu ambiente,
    # sem transformar o programa em um atacante.
    target_ip = "192.168.1.50"

    # Cria o agente.
    agent = PurpleNeuralAgent(target_ip)

    # Inicia o ciclo de análise.
    agent.run_loop()