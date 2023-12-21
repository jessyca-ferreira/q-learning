import connection
import numpy
import random

RANDOMNESS = 0.01
LEARNING_RATE = 0.01
DISCOUNT_FACTOR = 0.9
RESULTS = numpy.loadtxt("resultado.txt")


def find_move (state):
    if random.random() < RANDOMNESS:
        print('Random')
        return random.randint(0,2)      # numero aleatorio que referencia possiveis movimentos
    
    print('Best')
    if RESULTS[state, 0] >= RESULTS[state, 1] and RESULTS[state, 0] >= RESULTS[state, 2]: return 0
    if RESULTS[state, 1] >= RESULTS[state, 0] and RESULTS[state, 1] >= RESULTS[state, 2]: return 1
    if RESULTS[state, 2] >= RESULTS[state, 0] and RESULTS[state, 2] >= RESULTS[state, 1]: return 2

def q_function (state, reard, current_state):
    return RESULTS[current_state][list(moves.values()).index(move)] + LEARNING_RATE * (reard + DISCOUNT_FACTOR * max(RESULTS[state]) - RESULTS[current_state][list(moves.values()).index(move)])
    
socket_connect = connection.connect(2037)

directions = {0: "Norte", 1: "Leste", 2: "Sul", 3: "Oeste"}
moves = {0: "left", 1: "right", 2: "jump"}

current_platform = 0
current_direction = 0
current_state = 0

max_iterations = 20
for i in range (max_iterations):
    print(f'Plataforma: {current_platform} | Direção: {current_direction}')
    move = moves[find_move(current_state)]
    print(f'Próxima ação: {move}')
    
    state, reard = connection.get_state_reward(socket_connect, move)
    state = state[2:]
    current_platform = int(state[:5], 2)
    current_direction = int(state[5:], 2)
    state = int(state, 2)
    
    RESULTS[current_state][list(moves.values()).index(move)] = q_function(state, reard, current_state)
    current_state = state
    
    numpy.savetxt('resultado.txt', RESULTS, fmt="%f")

