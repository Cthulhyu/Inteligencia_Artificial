#Gabriel Mendes Boaventura
#RA:22251646
#Data:29/05/2025
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
#Antecedentes, que são as predições que indicam o uso e ação do projeto
uso_cpu = ctrl.Antecedent(np.arange(0, 101, 1), 'uso_cpu')
taxa_requisicoes = ctrl.Antecedent(np.arange(0, 1001, 1), 'taxa_requisicoes')
#Ação feita pelo resultado do usp_cpu com taxa de requisitos
acao_servidor = ctrl.Consequent(np.arange(0, 101, 1), 'acao_servidor')
#DEFINIÇÕES DAS FUNÇÕES DE PERTINÊNCIA
#uso da CPU
uso_cpu['baixo'] = fuzz.trimf(uso_cpu.universe, [0, 0, 40])
uso_cpu['medio'] = fuzz.trimf(uso_cpu.universe, [30, 50, 70])
uso_cpu['alto'] = fuzz.trimf(uso_cpu.universe, [60, 100, 100])
#Taxa de requisitos
taxa_requisicoes['baixa'] = fuzz.trimf(taxa_requisicoes.universe, [0, 0, 300])
taxa_requisicoes['media'] = fuzz.trimf(taxa_requisicoes.universe, [200, 500, 700])
taxa_requisicoes['alta'] = fuzz.trimf(taxa_requisicoes.universe, [600, 1000, 1000])
#Ação do Servidor
acao_servidor['remover'] = fuzz.trimf(acao_servidor.universe, [0, 0, 30])
acao_servidor['manter'] = fuzz.trimf(acao_servidor.universe, [30, 50, 70])
acao_servidor['adicionar'] = fuzz.trimf(acao_servidor.universe, [70, 100, 100])
#Regras inpostas
regra1 = ctrl.Rule(uso_cpu['baixo'] & taxa_requisicoes['baixa'], acao_servidor['remover'])
regra2 = ctrl.Rule(uso_cpu['medio'] & taxa_requisicoes['media'], acao_servidor['manter'])
regra3 = ctrl.Rule(uso_cpu['alto'] & taxa_requisicoes['alta'], acao_servidor['adicionar'])
regra4 = ctrl.Rule(uso_cpu['medio'] & taxa_requisicoes['alta'], acao_servidor['adicionar'])
regra5 = ctrl.Rule(uso_cpu['baixo'] & taxa_requisicoes['alta'], acao_servidor['manter'])
regra6 = ctrl.Rule(uso_cpu['alto'] & taxa_requisicoes['baixa'], acao_servidor['manter'])

sistema = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
simulador = ctrl.ControlSystemSimulation(sistema)
#Cenarios Hipoteticos
cenarios = [
    (10, 100),   # Baixo uso_cpu, baixa taxa
    (50, 400),   # Médio uso_cpu, média taxa
    (80, 900),   # Alto uso_cpu, alta taxa
    (35, 700),   # Entre baixo-médio uso_cpu, alta taxa
    (90, 200),   # Alto uso_cpu, baixa taxa
]
#Roda os cenarios hipoteticos e mostra num Grafico
for i, (cpu, req) in enumerate(cenarios, 1):
    simulador.input['uso_cpu'] = cpu
    simulador.input['taxa_requisicoes'] = req
    simulador.compute()
    acao = simulador.output['acao_servidor']
    print(f"Cenário {i}: uso_cpu={cpu}%, taxa_requisicoes={req} req/s -> Ação: {acao:.2f}%")
    uso_cpu.view()
    taxa_requisicoes.view()
    acao_servidor.view()

