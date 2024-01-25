def solution(m):
    # making m 2d*2d array
    min_width = min([len(row) for row in m])
    min_height = len(m)
    if min_width != min_height:
        square_size=min(min_width,min_height)
        m=[[m[row][col] for col in range(square_size)] for row in range(square_size)]

        
    def get_absorption_probabilities(transition_matrix):
        critical_chips = []
        for transition_row in transition_matrix:
            critical_chips.append(sum(transition_row))
        transient_states = []
        terminal_states = []
        for idx,state in enumerate(transition_matrix):
            if sum(state) == state[idx]:
                terminal_states.append(idx)
            else:
                transient_states.append(idx)
        chips = get_chips(transition_matrix, critical_chips, transient_states)
        total_chips = 0
        for terminal_state in terminal_states:
            total_chips += chips[terminal_state]
        absorption_probabilities = []
        for terminal_state in terminal_states:
            absorption_probabilities.append(float(chips[terminal_state]))
        return absorption_probabilities

    def get_chips(transition_matrix, critical_chips, transient_states):
        chips = []
        for state in range(len(transition_matrix)):
            if state in transient_states:
                chips.append(critical_chips[state])
            else:
                chips.append(0)
        chips[0] += .000000000001
        while True:
            any_move = False
            for transient_state in transient_states:
                while chips[transient_state] > critical_chips[transient_state]:
                    for next_state, transition_chips in enumerate(transition_matrix[transient_state]):
                        if transition_chips > 0:
                            any_move = True
                            chips[transient_state] -= transition_chips
                            chips[next_state] += transition_chips
            if not any_move:
                chips[0] = critical_chips[0]
                all_critical = True
                for transient_state in transient_states:
                    if chips[transient_state] != critical_chips[transient_state]:
                        all_critical = False
                if all_critical:
                    return chips
                else:
                    chips[0] += .000000000001
    absorption_probabilities=get_absorption_probabilities(m)
    absorption_probabilities=[int(absorption) for absorption in absorption_probabilities]
    return absorption_probabilities+[sum(absorption_probabilities)]

test_1=[  
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability  
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities  
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)  
    [0,0,0,0,0,0],  # s3 is terminal  
    [0,0,0,0,0,0],  # s4 is terminal  
    [0,0,0,0,0,0],  # s5 is terminal
]

# test_1=[
#     [0, 2, 1, 0, 0], 
#     [0, 0, 0, 3, 4], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0]
# ]

print(solution(test_1))