
from smv_engin import *
import pexpect

input_model = """
  MODULE main
  VAR
    request : boolean;
    state : {ready, busy};
  ASSIGN
    init(state) := ready;
    
    next(state) := case
      state = ready & request = TRUE : busy;
      TRUE : {ready, busy};
    esac;
    
    SPEC AG state=ready;
    SPEC AG state=busy;
    SPEC AF state=ready;
    SPEC AF state=busy;
"""

output = "" 
err = ""

# Approach-1: run serperately on each model
# output, err = run_nusmv(input_model)
# specs = parse_output(output, err)
# print_output(specs)





# Approach-2: run once for all models
#   Start the interactive NuSMV
#   Linux Only

smv.expect("NuSMV >")  # Wait for a prompt

output, err = check_nusmv_model(input_model)
specs = parse_output(output, err)
print_output(specs)


# check another model
input_model = input_model.replace("{ready, busy};", "{ready, busy}")
output, err = check_nusmv_model(input_model)
specs = parse_output(output, err)
print_output(specs)


