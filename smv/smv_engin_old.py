import sys
import os
import subprocess
import re



class Spec:
  def __init__(self, condition="", success=True, counterExample=""):
    self.condition = condition
    self.success = success
    self.counterExample = counterExample

  def __str__(self):
    return f"Condition: {self.condition}\nSuccess: {self.success}\nCounter Example: {self.counterExample}"

def run_nusmv(input_model):
  # x = os.system( f"nusmv model.smv" )

  print("----- run_nusmv -----")
  path = './'
  if os.path.exists("ram-dir"):
    path = './ram-dir/'

  fname = path + "model.smv"
  saveFile = open( fname, "w")
  saveFile.write(input_model)
  saveFile.close()

  nusmv_path = "/home/arwa/Programs/NuSMV-2.6.0-linux64/NuSMV-2.6.0-Linux/bin/NuSMV"
  result = subprocess.run([nusmv_path, fname], capture_output=True, text=True)
  output = result.stdout  

  return output



def parse_output(output):
  output = output.replace("-- specification", "#####\n-- specification")
  output += "\n#####"

  prtn = r"-- specification (.*?)  is (true|false).*?Type: Counterexample(.*?)(#####)"
  match = re.search(prtn, output, re.DOTALL+ re.MULTILINE)
  specs = []
  
  for match in re.finditer(prtn, output, re.DOTALL):
    condition = match.group(1).strip()
    success = match.group(2) == "true"
    counterExample = match.group(3).strip() if not success else ""
    sp = Spec(condition, success, counterExample)
    specs.append(sp)

  return specs
