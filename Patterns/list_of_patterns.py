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

    # ~~~ ONE EVENT ~~~
    # -- P is false before R
    #  LTLSPEC F (P) -> (!(P) U (R))
    p1 = f'F (input = {P_input} & output = {P_output}) -> (!(input = {P_input} & output = {P_output}) U (input = {R_input} & output = {R_output}))'

    # -- P is false after R
    # LTLSPEC G((R) -> G(!(P)))
    p2 = f'G((input = {R_input} & output = {R_output}) -> G(!(input = {P_input} & output = {P_output})))'

    # --P becomes true before R
    # LTLSPEC !(R) W ((P) & !(R))
    # p3 = f'!(input = {R_input} & output = {R_output}) W ((input = {P_input} & output = {P_output}) & !(input = {R_input} & output = {R_output}))'

    # --P becomes true after R
    # LTLSPEC G (!(R)) | F ((R) & F (P)))
    p4 = f'G (!(input = {R_input} & output = {R_output})) | F ((input = {R_input} & output = {R_output}) & F (input = {P_input} & output = {P_output}))'

    # --P is true before R
    # LTLSPEC F (R) -> ((P) U (R))
    p5 = f'F (input = {R_input} & output = {R_output}) -> ((input = {P_input} & output = {P_output}) U (input = {R_input} & output = {R_output}))'

    # --P is true after R
    # LTLSPEC G ((R) -> G((P)))
    p6 = f'G ((input = {R_input} & output = {R_output}) -> G((input = {P_input} & output = {P_output})))'

    group1_patterns = [p1, p2, p4, p5, p6]
    return group1_patterns

# ~~~ TWO EVENTS ~~~
# --S precedes P  Globally
f'!{P} W {S}'

# -- S responds to P globally
f'G ({P} -> F {S})'

# ~~~ THREE EVENTS ~~~
# --P is false between Q and R
f'G(({Q} & !{R} & F {R}) -> (!{P} U {R}))'

# --P is false after Q until R
f'G({Q} & !{R} -> (!{P} W {R}))'

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