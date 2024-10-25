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

  def __str__(self):
    return f"Condition: {self.condition}\nSuccess: {self.success}\nCounter Example: {self.counterExample}"
  

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

  print("----- 🚀 run_nusmv  -----")
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

  # if err:
  #   print(output)
  #   print("---------- Error ----------")
  #   print(err)
  #   exit()

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