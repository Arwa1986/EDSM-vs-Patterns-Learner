import sys
import os
import subprocess
import re

import pexpect

smv = pexpect.spawn("/home/arwa/Programs/NuSMV-2.6.0-linux64/NuSMV-2.6.0-Linux/bin/NuSMV -int")

class Spec:
  def __init__(self, condition="", success=True, counterExample=""):
    self.condition = condition
    self.success = success
    self.counterExample = counterExample
    # self.name = self.get_name()

    # get_name() is a helper function to get the name of the specification

  def get_name(self):
    # Extract event values
    event_pattern = r'(input\s*=\s*.*?\s*&\s*output\s*=\s*.*?\d)'
    events = re.findall(event_pattern, self.condition)
    event_set = set(events)
    events_list = list(event_set)

    if len(events) < 2:
      print("Not enough events found")
      return 'Unknown pattern'

    # Debug: Print extracted events
    print(f"Extracted events: {events_list}")

    # Build patterns dynamically
    patterns = {}
    if len(events_list) == 3:
      patterns = {
        # f'G(({S_event}  & ! {R_event} & F {R_event}) -> (!{P_event} U {R_event}))'
        rf'G(({events_list[0]} & ! {events_list[1]} & F {events_list[1]}) -> (!{events_list[2] } U {events_list[1]}))': 'P_event "{P_event}" is false between S_event "{S_event}" and R_event "{R_event}"',
        # f'G({S_event} & !{R_event} -> (G (!{P_event}) | (!{P_event} U {R_event})))'
        rf'G({events_list[0]} & !{events_list[1]} -> (G (!{events_list[2]}) | (!{events_list[1]} U {events_list[1]})))': 'P_event "{P_event}" is false after S_event "{S_event}" until R_event "{R_event}"',

      }
    elif len(events_list) == 2:
      patterns = {
        # f'F {R_event} -> (!{P_event} U {R_event})'
        rf'F {events_list[0]} -> (!{events_list[1]} U{events_list[0]})': 'P_event "{P_event}" is false before R_event "{R_event}"',
        # f'G({R_event} -> G(!{P_event}))'
        rf'G({events_list[1]} -> G(!{events_list[0]}))': 'P_event "{P_event}" is false after R_event "{R_event}"'
      }

    # Debug: Print built patterns
    for pattern in patterns:
      print(f"Pattern: {pattern}")

    for pattern, name in patterns.items():
      match = re.match(pattern, self.condition)
      if match:
        # Debug: Print matched pattern
        print(f"Matched pattern: {pattern}")
        return name.format(**match.groupdict())

    print("No pattern matched")
    return 'Unknown pattern'

  def __str__(self):
    return f"Condition: {self.condition}\n"#Success: {self.success}\nCounter Example: {self.counterExample}"
  

def check_nusmv_model(input_model):

  print("----- 🚀 run_nusmv (Interactive) -----")
  path = ''; err=''; output=''
  if os.path.exists("ram-dir"):
    path = 'ram-dir/'

  fname = os.path.join(path, "model.smv")
  saveFile = open( fname, "w")
  saveFile.write(input_model)
  saveFile.close()  

  smv.sendline(f"read_model -i {fname}"); smv.expect("NuSMV >")
  err = smv.before.decode('utf-8')
  err = ''.join(err.splitlines(keepends=True)[1:])
  if err != '' :
    return output, err


  smv.sendline("flatten_hierarchy");  smv.expect("NuSMV >")
  smv.sendline("encode_variables");   smv.expect("NuSMV >")
  smv.sendline("build_model");        smv.expect("NuSMV >")

  smv.sendline("check_ltlspec");      smv.expect("NuSMV >")
  output = smv.before.decode('utf-8')
  # print(output)

  smv.sendline("reset");        smv.expect("NuSMV >")

  return output, err


def run_nusmv(input_model):
  # x = os.system( f"nusmv model.smv" )

  # print("----- 🚀 run_nusmv  -----")
  path = ''
  if os.path.exists("ram-dir"):
    path = 'ram-dir/'

  fname = os.path.join(path, "model.smv") 
  saveFile = open( fname, "w")
  saveFile.write(input_model)
  saveFile.close()  

  nusmv_process = subprocess.run(["/home/arwa/Programs/NuSMV-2.6.0-linux64/NuSMV-2.6.0-Linux/bin/NuSMV", fname], capture_output=True, text=True)
  output = nusmv_process.stdout
  err = nusmv_process.stderr

  # Terminate the process
  # nusmv_process.terminate()

  # Wait for process to terminate
  # nusmv_process.wait()
  return output, err

def close_nusmv():
    # smv.sendline('exit')
    smv.close()

def parse_output(output, err):

  if err:
    print(output)
    print("---------- Error ----------")
    print(err)
    exit()

  output = output.replace("\r\n", "\n")
  output = output.replace("-- specification", "#####\n-- specification")
  output += "\n#####"

  ptrn = r"-- specification (.*?)  is (true|false)\n(#####|.*?Type: Counterexample(.*?)#####)"
  match = re.search(ptrn, output, re.DOTALL + re.MULTILINE)
  specs = []

  if not match:
    print(output)
    print(err)
    exit()

  for match in re.finditer(ptrn, output, re.DOTALL):
    condition = match.group(1).strip()
    success = match.group(2) == "true"
    counterExample = match.group(4).strip() if not success else ""
    sp = Spec(condition, success, counterExample)
    specs.append(sp)

  return specs


import re


def parse_nusmv_output(nusmv_output):
  elist = []

  # Regular expression to capture specifications and their results
  spec_pattern = re.compile(r"-- specification\s+(.*?)\s+is\s+(true|false)", re.DOTALL)

  # Find all specifications and their results
  for match in spec_pattern.finditer(nusmv_output):
    specification = match.group(1).strip()
    result = match.group(2).strip() == "true"  # Convert result to boolean
    counterexample = None

    # Debugging output
    # print(f"Found specification: {specification}, Result: {result}")

    # If the result is false, find the corresponding counterexample
    if not result:
      counterexample_search_start = match.end()
      counterexample_search = nusmv_output[counterexample_search_start:]

      # Find the counterexample based on the pattern
      counterexample_pattern = re.compile(
        r"Trace Description: LTL Counterexample.*?(\n.*?)*?(?=\n-- specification|$)", re.DOTALL)
      counterexample_match = counterexample_pattern.search(counterexample_search)

      if counterexample_match:
        counterexample = counterexample_match.group(0).strip()
        # print(f"Counterexample found for {specification}: {counterexample}")
      # else:
        # print(f"No counterexample found for {specification}")

    # Create a Spec object and append it to elist
    spec_object = Spec(specification, result, counterexample)
    elist.append(spec_object)

  # Return the list only if there are false specifications
  # false_specs = [spec for spec in elist if not spec.success]
  # return false_specs if false_specs else []
  return elist
def print_output(specs):

  for sp in specs:
    print(f"{'✅' if sp.success else '❌'}  {sp.condition}")
    # print(sp.condition)
    print(sp.success )
    print(sp.counterExample)

    print("--------------------------\n")

  return specs



#  حاولت بهذي الطريقة ومازبطت ،، ممكن نحاول فيها بعدين
# Start the interactive application
# process = subprocess.Popen(
#     ["nusmv", "-int"],  # Replace with your app's command
#     stdin=subprocess.PIPE,     # To send commands
#     stdout=subprocess.PIPE,    # To capture output
#     stderr=subprocess.PIPE,    # To capture errors (optional)
#     text=True,                 # To handle strings (instead of bytes)
#     shell=False                 # If you need to run the command in a shell
# )

# Send a command to the application
# process.stdin.write(f"read_model -i {fname}")
# process.stdin.write("flatten_hierarchy\n")
# process.stdin.write("encode_variables\n")
# process.stdin.write("build_model\n")
# process.stdin.write("print_reachable_states -v\n")
# process.stdin.flush()  # Ensure the command is sent

# output = process.stdout.read()
# err = process.stderr.read()
# process.terminate()