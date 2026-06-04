import json
import copy
import os
import pandas as pd

# windows are IDed as well, ['lComponent']['idWtC']
def importMETrData(data, templateName = "METrTemplate"):
    
    templateDict = {}
    componentDict = {}
  
    for component in data['lVariant'][0]['building']['lComponent']:

        if component['n'] != "":
            if component['idAssC'] != -1:
                componentDict[component['n']] = {"idAssC": component['idAssC']}
            if component['idWtC'] != -1:
                componentDict[component['n']] = {"idWtC": component['idWtC']}

    assemblyDict = {}
    windowDict = {}

    for assembly in data['lAssembly']:
        assemblyDict[assembly['id']] = assembly['n']

    for window in data['lWindow']:
        windowDict[window['id']] = window['n']

    for component_name, component in componentDict.items():
        if "idAssC" in component and component["idAssC"] in assemblyDict:
            componentDict[component_name] = assemblyDict[component["idAssC"]]
        elif "idWtC" in component and component["idWtC"] in windowDict:
            componentDict[component_name] = windowDict[component["idWtC"]]
    
    templateDict['caseName'] = data['lVariant'][0]['n']

    templateDict['caseID'] = data['lVariant'][0]['id']

    templateDict['Azimuth'] = data['lVariant'][0]['building']['azimN']

    templateDict['airTightness50'] = round(float(data['lVariant'][0]['PHIUS']['lCase'][0]['tightEnv50']) * (1/18.288), 4)
    templateDict  = templateDict | componentDict

    templatePath = os.path.join(os.path.dirname(__file__), templateName + ".csv")
    templateDF = pd.DataFrame([templateDict])
    templateDF.to_csv(templatePath, index=False)
    print(f"Template CSV created at {templatePath}")
    pass


def updateAssembly(case, componentName, newAssemblyName):
    caseIndex = int(case - 1)
    componentIndex = int(componentDict[componentName]) - 1
    assemblyID = float(assemblyDict[newAssemblyName])

    data['lVariant'][caseIndex]['building']['lComponent'][componentIndex]['idAssC'] = assemblyID

    print(f"Assembly updated for case {case}, component {componentName}, to {newAssemblyName}")

    pass

# CLI UI

introText = f"Welcome to the METr JSON Parametric Run Editor!"
introText += f"\nThis tool allows you to edit the JSON files for METr parametric runs in a more user-friendly way."
introText += f"\n\nThis is version 26.1.0, released June 2026, and has been tested with METr v1.57."
introText += f"\n\n"

print(introText)

inputMenu = "Please select a function to perform: \n1. Import METr data and create template CSV\n"
inputMenu += "2. Update METr JSON based on CSV input" 
inputMenu += "\n3. Read Results from JSON file and convert to CSV"
inputMenu += "\n4. Exit\n"

prgmFunc = input(inputMenu)

while prgmFunc != "4":
    if prgmFunc == "1":
        jsonPath = input("Please enter the path to the METr JSON file you want to import: ")
        
        
        if os.path.exists(jsonPath):
             with open(jsonPath.replace('"', ''), 'r') as f:
                data = json.load(f)
                importMETrData(data, templateName = input("Please enter a name for the template CSV (without .csv extension): "))
        prgmFunc = input(inputMenu)
             

# with open(r"C:\Users\amitc_crl\OneDrive\Documents\GitHub\Misc-_Calcs\METr json\Project (4).json", 'r') as f:
#     data = json.load(f)

#     assemblyDict = {}

#     for assembly in data['lAssembly']:
#         assemblyDict[assembly['n']] = assembly['id']
    
#     componentDict = {}

#     for component in data['lVariant'][0]['building']['lComponent']:
#         componentDict[component['n']] = component['id']

#     importMETrData(data)

    # a = data['lVariant'][0]
    # a['id'] = 13

    # data['lVariant'].append(copy.deepcopy(a))

    # a = data['lVariant'][0]
    # a['id'] = 14

    # data['lVariant'].append(copy.deepcopy(a))

    # updateAssembly(2, "Floor", "_Slab_Whole Slab R20 (4)")
    # updateAssembly(3, "Wall", "_Wall Wood R-13 FG Batt, 2x4, 16oc, OSB, R-4 EPS (5)")

    # json_str = json.dumps(data, indent=4)
    # with open(r"C:\Users\amitc_crl\Desktop\wufijsonCase2.json", "w") as f:
    #     f.write(json_str)

# print(json.dumps(data['lVariant'][0]['building']['lComponent'][0]['idAssC'], sort_keys=True, indent=2))
# print(json.dumps(data['lVariant'][0]['building']['lComponent'][0]['n'], sort_keys=True, indent=2))
