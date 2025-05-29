#Gabreiel Mendes Boaventura
#RA:22251646
#29/05/2025
import random

# Dados do problema
PROFESSORES = ['P1', 'P2', 'P3', 'P4', 'P5']
DISCIPLINAS = ['Matemática', 'Física', 'Química', 'História', 'Biologia']
SALAS = ['S1', 'S2', 'S3', 'S4']
TURNOS = ['Manhã', 'Tarde', 'Noite']

PROFESSOR_DISCIPLINAS = {
 'P1': ['Matemática', 'Física'],
 'P2': ['Física', 'Química'],
 'P3': ['História', 'Biologia'],
 'P4': ['Matemática', 'História'],
 'P5': ['Química', 'Biologia']
}

CARGA_HORARIA = {
 'Matemática': 4,
 'Física': 3,
 'Química': 3,
 'História': 2,
 'Biologia': 3
}

CAPACIDADE_SALA = {
 'S1': 30,
 'S2': 25,
 'S3': 40,
 'S4': 20
}

AULAS_POR_TURNO = 4

def cria_individuo():
    individuo = []
    for disciplina in DISCIPLINAS:
        prof_possiveis = [p for p, d in PROFESSOR_DISCIPLINAS.items() if disciplina in d]
        professor = random.choice(prof_possiveis)
        sala = random.choice(SALAS)
        turno = random.choice(TURNOS)
        individuo.append((disciplina, professor, sala, turno))
    return individuo

def fitness(individuo):
    return 1  # fitness constante

def crossover(ind1, ind2):
    ponto = random.randint(1, len(DISCIPLINAS) - 1)
    filho1 = ind1[:ponto] + ind2[ponto:]
    filho2 = ind2[:ponto] + ind1[ponto:]
    return filho1, filho2

def mutacao(ind):
    idx = random.randint(0, len(DISCIPLINAS) - 1)
    disc, prof, sala, turno = ind[idx]
    antes = (disc, prof, sala, turno)
    op = random.choice(['professor', 'sala', 'turno'])
    if op == 'professor':
        prof_possiveis = [p for p, d in PROFESSOR_DISCIPLINAS.items() if disc in d]
        prof = random.choice(prof_possiveis)
    elif op == 'sala':
        sala = random.choice(SALAS)
    else:
        turno = random.choice(TURNOS)
    ind[idx] = (disc, prof, sala, turno)
    print(f"Mutação no gene índice {idx}: {antes} -> {ind[idx]}")

POPULACAO_SIZE = 20
GERACOES = 20

def seleciona_pais(pop):
    torneio = random.sample(pop, 3)
    torneio.sort(key=lambda ind: fitness(ind), reverse=True)
    return torneio[0], torneio[1]

# algoritmo genético
populacao = [cria_individuo() for _ in range(POPULACAO_SIZE)]

for ger in range(GERACOES):
    nova_pop = []
    while len(nova_pop) < POPULACAO_SIZE:
        pai1, pai2 = seleciona_pais(populacao)
        filho1, filho2 = crossover(pai1, pai2)

        # Controle da mutação com valor aleatório
        r1 = random.random()
        if 0.1 <= r1 <= 0.7:
            print(f"[Geração {ger+1}] Mutando filho 1 (r = {r1:.2f})")
            mutacao(filho1)

        r2 = random.random()
        if 0.1 <= r2 <= 0.7:
            print(f"[Geração {ger+1}] Mutando filho 2 (r = {r2:.2f})")
            mutacao(filho2)

        nova_pop.append(filho1)
        if len(nova_pop) < POPULACAO_SIZE:
            nova_pop.append(filho2)

    populacao = nova_pop
    melhor = max(populacao, key=fitness)
    print(f"Geração {ger+1} concluída.")

print("\nMelhor solução encontrada:")
for gene in melhor:
    print(gene)