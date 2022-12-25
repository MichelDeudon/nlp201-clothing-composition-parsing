import json
import urllib.request as urllib2


def fetch_data(base_url: str = "https://maxhalford.github.io/files/datasets/nlp-carbonfact"):
    ''' Fetch inputs, expected outputs and list of materials from Max Halford blog '''

    inputs_url = "{}/{}".format(base_url, "inputs.txt")
    inputs = urllib2.urlopen(inputs_url).read().decode("utf-8") 
    inputs = inputs.split("\n") # then split it into lines
    
    targets_url = "{}/{}".format(base_url, "outputs.json")
    targets = urllib2.urlopen(targets_url).read() #.decode("utf-8") 
    targets = json.loads(targets)    
    
    materials_url = "{}/{}".format(base_url, "materials.txt")
    materials = urllib2.urlopen(materials_url).read().decode("utf-8") 
    materials = materials.split("\n") # then split it into lines
    
    assert len(inputs) == len(targets)
    return inputs, targets, materials
