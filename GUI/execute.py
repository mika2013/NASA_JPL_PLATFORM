import os
import subprocess

class Execute:
    def mkdirs(self):
        command = 'mkdir -p Netlist Output FitCurve Library Library/temp'
        os.system(command)
        command = 'touch Library/library.json Library/name.json'
        os.system(command)
        return
    
    def rm_all(self):
        command = 'rm -f ./Output/*'
        os.system(command)
        return

    def execute_module3(self, path):
        # command = 'whereis bin/Xyce'# the command that going to be executed
        #Xyce_path = subprocess.getoutput(command)
        #command = Xyce_path.split(' ')[1] + ' ' + path  # the command that going to be executed
        # print(command)
        #result = subprocess.getoutput(command)
        # print(result)
        command = 'Xyce ' + path
        result = subprocess.call(command, shell = True, executable="/bin/tcsh")
        return result
