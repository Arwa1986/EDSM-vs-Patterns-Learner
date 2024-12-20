R = ''
P = ''
T = ''
Q = ''
S = ''
def design_group1_patterns(P, R):
    P_input = P[0]
    P_output = P[1]

    R_input = R[0]
    R_output = R[1]

    P_event = f'(input = {P_input} & output = {P_output})'
    R_event = f'(input = {R_input} & output = {R_output})'
    group1_patterns = []
    # ~~~ ONE EVENT ~~~
    # -- P is false before R
    #  LTLSPEC F (R) -> (!(P) U (R))
    if P != R:
        p1 = f'F {R_event} -> (!{P_event} U {R_event})'
        group1_patterns.append(p1)
    # -- P is false after R
    # LTLSPEC G((R) -> G(!(P)))
    p2 = f'G({R_event} -> G(!{P_event}))'
    group1_patterns.append(p2)

    # --P becomes true before R
    # LTLSPEC !(R) W ((P) & !(R))
    # p3 = f'!(input = {R_input} & output = {R_output}) W ((input = {P_input} & output = {P_output}) & !(input = {R_input} & output = {R_output}))'

    # --P becomes true after R
    # LTLSPEC G (!(R)) | F ((R) & F (P)))
    # p4 = f'G (!(input = {R_input} & output = {R_output})) | F ((input = {R_input} & output = {R_output}) & F (input = {P_input} & output = {P_output}))'

    # --P is true before R
    # LTLSPEC F (R) -> ((P) U (R))
    # p5 = f'F (input = {R_input} & output = {R_output}) -> ((input = {P_input} & output = {P_output}) U (input = {R_input} & output = {R_output}))'

    # --P is true after R
    # LTLSPEC G ((R) -> G((P)))
    # p6 = f'G ((input = {R_input} & output = {R_output}) -> G((input = {P_input} & output = {P_output})))'


    return group1_patterns

def design_group2_patterns(P, S, R):
    P_input = P[0]
    P_output = P[1]

    R_input = R[0]
    R_output = R[1]

    S_input = S[0]
    S_output = S[1]

    P_event = f'(input = {P_input} & output = {P_output})'
    R_event = f'(input = {R_input} & output = {R_output})'
    S_event = f'(input = {S_input} & output = {S_output})'
    group2_patterns = []

    if S != R and R != P:
        # --P is false between S and R
        # G ((S & !R & <>R) -> (!P U R))
        p1 = f'G(({S_event}  & ! {R_event} & F {R_event}) -> (!{P_event} U {R_event}))'
        group2_patterns.append(p1)
        # --P is false after Q until R
        # G(Q & !R -> (G (!P) | (!P U R)))
        p2 = f'G({S_event} & !{R_event} -> (G (!{P_event}) | (!{P_event} U {R_event})))'
        group2_patterns.append(p2)
    return group2_patterns

# ~~~ TWO EVENTS ~~~
# --S precedes P  Globally
f'!{P} W {S}'

# -- S responds to P globally
f'G ({P} -> F {S})'

# ~~~ THREE EVENTS ~~~

# --P becomes true between Q and R
f'G ({Q} & !{R} -> (!{R} W ({P} & !{R})))'

# --P becomes true after Q until R
f'G ({Q} & !{R} -> (!{R} U ({P} & !{R})))'

# --P is true between Q and R
f'G (({Q} & !{R} & F {R}) -> ({P} U {R}))'

# --P is true after Q until R
f'G ({Q} & !{R} -> ({P} W {R}))'

# -- S precedes P before R
f'F {R} -> (!{P} U ({S} | {R}))'

# -- S precedes P after Q
f'G !{Q} | F ({Q} & (!{P} W {S}))'

# --S precedes P between Q and R
f'G (({Q} & !{R} & F {R}) -> (!{P} U ({S} | {R})))'

# --S precedes P after Q until R
f'G ({Q} & !{R} -> (!{P} W ({S} | {R})))'

# -- S responds to P before R
f'F {R} -> ({P} -> (!{R} U ({S} & !{R}))) U {R}'

# -- S responds to P after Q
f'G ({Q} -> G({P} -> F {S}))'

# -- S responds to P between Q and R
f'G (({Q} & !{R} & F {R}) -> ({P} -> (!{R} U ({S} & !{R}))) U {R})'

# -- S responds to P after Q until R
f'G ({Q} & !{R} -> (({P} -> (!{R} U ({S} & !{R}))) W {R})'