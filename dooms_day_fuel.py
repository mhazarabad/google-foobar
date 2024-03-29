def solution(m):
    min_width = min([len(row) for row in m])
    min_height = len(m)
    sqaure_size = min(min_width, min_height)
    m = [row[:sqaure_size] for row in m[:sqaure_size]]
    from fractions import Fraction
    
    for row_idx, row in enumerate(m):
        for col_idx, col in enumerate(row):
            if col < 0:
                m[row_idx][col_idx] = 0
    non_terminal_with_probability = dict()
    terminal_states_with_probability = dict()
    for state_idx, state in enumerate(m):
        if sum(state) == state[state_idx]:
            terminal_states_with_probability[state_idx] = state
        else:
            non_terminal_with_probability[state_idx] = state

    if len(non_terminal_with_probability.keys())==len(m):
        return [0,0]
    if len(terminal_states_with_probability.keys())==len(m):
        return [len(m),len(m)]
    I = []
    Q = []
    R = []
    def make_I_matrix(n):
        return [[Fraction(1,1) if row == col else Fraction(0,1) for col in range(n)] for row in range(n)]
    for non_terminal_state in non_terminal_with_probability.keys():
        sum_of_non_terminal_state = sum(m[non_terminal_state])        
        row=[Fraction(probability,sum_of_non_terminal_state) for idx, probability in enumerate(non_terminal_with_probability[non_terminal_state]) if idx in non_terminal_with_probability.keys()]
        Q.append(row)
    for non_terminal_state in non_terminal_with_probability.keys():
        sum_of_non_terminal_state = sum(m[non_terminal_state])
        row=[Fraction(probability,sum_of_non_terminal_state) for idx, probability in enumerate(non_terminal_with_probability[non_terminal_state]) if idx in terminal_states_with_probability.keys()]
        R.append(row)
    I = make_I_matrix(len(Q))
    I_Q = [[I[row][col] - Q[row][col] for col in range(len(Q[row]))] for row in range(len(Q))]

    def inverse(A):
        n = len(A)
        AM = A
        I = make_I_matrix(n)
        IM = I
        for fd in range(n):
            fdScaler = Fraction(1,1) / AM[fd][fd]
            for j in range(n):
                AM[fd][j] *= fdScaler
                IM[fd][j] *= fdScaler
            for i in list(range(n))[0:fd] + list(range(n))[fd+1:]:
                crScaler = AM[i][fd]
                for j in range(n):
                    AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                    IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
        return IM
    F = inverse(I_Q)

    def multiply(A,B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        C = [[Fraction(0,1) for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    C[i][j] += (A[i][k] * B[k][j])
        return C
    FR = multiply(F,R)[0]
    
    def gcd(a, b, rtol = 1e-05, atol = 1e-08):
        t = min(abs(a), abs(b))
        while abs(b) > rtol * t + atol:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    denominator = 1
    for probability in FR:
        denominator = lcm(denominator, probability.denominator)
    return [probability.numerator * (denominator//probability.denominator) for probability in FR] + [denominator]

test_1=[  
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability  
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities  
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)  
    [0,0,0,0,0,0],  # s3 is terminal  
    [0,0,0,0,0,0],  # s4 is terminal  
    [0,0,0,0,0,0],  # s5 is terminal
]


test_1=[
    [0, 2, 1, 0, 0], 
    [0, 0, 0, 3, 4], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0]
]

test_1=[
    [0]*5,
    [0]*5,
    [0]*5,
    [0]*5,
    [0]*5
]

print(solution(test_1))




