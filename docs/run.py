import ast
import os

def extract_function_names(file_path):
    function_names=[]
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
    return function_names

with open("tools.rst", "w") as rst_file:
            s="tools package"
            print(s,file=rst_file)
            print(len(s)*"=",file=rst_file)
            print(".. toctree::\n",file=rst_file)
            l=os.listdir("../tools")
            l.sort()
            for filename in l:
                if filename.endswith(".py") and not filename.endswith("__.py"): 
                    print("   ",filename[:-3],file=rst_file)
                    
for filename in os.listdir("../tools"):
    if filename.endswith(".py") and not filename.endswith("__.py"): 
        module = filename[:-3]       
        with open(module+".rst", "w") as rst_file:
            print(module,file=rst_file)
            print(len(module)*"=",file=rst_file)
            print(".. currentmodule:: gunfolds.tools."+module,file=rst_file)
            print("\n",file=rst_file)
            file_path="../tools"
            function_names = extract_function_names(file_path+"/"+filename)
            function_names.sort()
            for func in function_names:
                funct = ""
                for c in func:
                    if c=="_":
                        funct+="\\"
                        funct+=c
                    else:
                        funct+=c
                print(funct,file=rst_file)
                print(len(funct)*"-",file=rst_file)
                print(".. autofunction:: gunfolds.tools."+module+"."+func,file=rst_file)
                print("\n",file=rst_file)