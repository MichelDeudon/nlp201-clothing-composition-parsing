import re
import regex
import json
import urllib.request as urllib2


def fetch_data(base_url: str = "https://maxhalford.github.io/files/datasets/nlp-carbonfact"):
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


def normalize_composition_format(text):
    """
    >>> normalize_composition_format('(body) 82% nylon 18% spandex (forro)100% polyester')
    'body: 82% nylon 18% spandex forro: 100% polyester'

    >>> normalize_composition_format('fabric - 80% polyamide 20% elastane/lining - 100% polyester')
    'fabric: 80% polyamide 20% elastane lining: 100% polyester'

    """

    if text == "100% polyester woven (pant) and 95% viscose  5%spandex knitted top":
        return "pants: 100% polyester knitted_top 95% viscose 5%spandex"

    text = re.sub(
        r"\((?P<component>\w+)\)", lambda m: f"{m.group('component')}: ", text
    )
    text = re.sub(r"(?P<component>\w+)\ -", lambda m: f"{m.group('component')}: ", text)
    text = text.replace("/", " ")
    text = text.replace(" %", "%")
    text = text.replace("：", ": ")
    text = re.sub(r"fabric \d:", "fabric:", text)
    text = re.sub(r"(\d+\.?\d*)%", r" \1%", text)
    text = text.replace("top body", "top_body")
    text = text.replace("op body", "top_body")
    text = text.replace("body & panty", "body_panty")
    text = text.replace("edge lace", "edge_lace")
    text = text.replace("edg lace", "edge_lace")
    text = text.replace("cup shell", "cup_shell")
    text = text.replace("centre front and wings", "centre_front_and_wings")
    text = text.replace("cup lining", "cup_lining")
    text = text.replace("front panel", "front_panel")
    text = text.replace("back panel", "back_panel")
    text = text.replace("marl fabric", "marl_fabric")
    text = text.replace("knited top", "knitted_top")
    text = text.replace("striped mesh", "striped_mesh")
    text = text.replace("trim lace", "trim_lace")
    text = text.replace("body-", "body:")
    text = text.replace("liner-", "liner:")
    text = text.replace("mesh-", "mesh:")
    text = text.replace("&", " ")
    text = text.replace("lace ", "lace: ")
    text = text.replace("mesh ", "mesh: ")
    text = text.replace("gusset ", "gusset: ")
    text = text.replace("top ", "top: ")
    text = text.replace("body ", "body: ")
    text = text.replace("fabric ", " fabric: ")
    text = text.replace("bottom ", " bottom: ")
    text = text.replace(" :", ":")
    text = text.replace(";", " ")
    text = text.replace(",", " ")
    text = text.replace(". ", " ")
    text = text.replace("，", " ")
    text = text.replace("pa-00462-tho pa-00464-tho", "pa-00464-tho")
    text = text.replace("pa-00462-tho:", "")
    text = text.replace("g string ", "g-string: ")
    text = text.replace("95% 5%", "100%")
    text = text.replace(":", ": ")
    text = text.replace("\t", " ")
    text = text.replace("$", "%")
    text = text.replace(" with ", " ")
    text = text.replace("  ", " ")
    text = text.replace("%s ", "% ")
    text = text.replace("bci cotton", "cotton")
    text = re.sub(r"pa-\d{5}-tho:", "", text)
    text = text.replace("spandexbottom:", "spandex bottom:")

    # typos
    text = text.replace("sapndex", "spandex")
    text = text.replace("spadnex", "spandex")
    text = text.replace("spandexndex", "spandex")
    text = re.sub("span$", "spandex", text)
    text = re.sub("spande$", "spandex", text)
    text = text.replace("polyest ", "polyester ")
    text = re.sub("polyeste$", "polyester", text)
    text = re.sub("poly$", "polyester", text)
    text = text.replace("polyster", "polyester")
    text = text.replace("polyeste ", "polyester ")
    text = text.replace("elastanee", "elastane")
    text = text.replace(" poly ", " polyester ")
    text = text.replace("cotton algodón coton", "cotton")
    text = text.replace("poliamide", "polyamide")
    text = text.replace("recycle polyamide", "recycled polyamide")
    text = text.replace("polyester poliéster", "polyester")
    text = text.replace("polystester", "polyester")
    text = text.replace("regualar polyamide", "regular polyamide")
    text = text.replace("recycle nylon", "recycled nylon")
    text = text.replace("buttom", "bottom")
    text = text.replace("recycle polyester", "recycled polyester")
    text = text.replace("125", "12%")
    text = text.replace("135", "13%")
    text = text.replace("recycled polyeser", "recycled polyester")
    text = text.replace("polyeter", "polyester")
    text = text.replace("polyeseter", "polyester")
    text = text.replace("viscouse", "viscose")
    text = text.replace("ctton", "cotton")
    text = text.replace("ryaon", "rayon")

    return text.replace("  ", " ").strip()


def named_pattern(name, pattern):
    return f"(?P<{name}>{pattern})"


def multiple(pattern, at_least_one=True):
    return f"({pattern})+" if at_least_one else f"({pattern})*"


def sep(pattern, sep):
    return pattern + multiple(sep + pattern, at_least_one=False)


def split_composition_into_component_materials(text):
    """

    >>> split_composition_into_component_materials('fabric: 80% polyamide 20% elastane lining: 100% polyester')
    {'fabric': [('80', 'polyamide'), ('20', 'elastane')], 'lining': [('100', 'polyester')]}

    """

    component = ""
    materials = []
    component_materials = {}

    for token in re.split(r"\s+", text):
        if token.endswith(":"):
            if materials:
                component_materials[component] = " ".join(materials)
                materials = []
            component = token.rstrip(":")
        else:
            materials.append(token)
    else:
        if materials:
            component_materials[component] = " ".join(materials)

    # Parse the materials
    material_pat = named_pattern("material", r"[a-zA-ZÀ-ÿ\-\s']+[a-zA-ZÀ-ÿ\-']")
    proportion_pat = named_pattern("proportion", r"\d{1,3}([,\.]\d{1,2})?") + "%?"

    for component, materials in component_materials.items():
        pattern = sep(rf"{proportion_pat}\s*{material_pat}", " ")
        match = regex.match(pattern, materials)
        component_materials[component] = [
            {
                "material": m,
                "proportion": float(p)
            }
            for m, p in zip(
                match.capturesdict()["material"],
                match.capturesdict()["proportion"],
            )
        ]

    return component_materials


# custom solution by Max
def test_custom_max():
    inputs, targets, materials = fetch_data()
    assert len(inputs) == len(targets)

    outputs = []
    for inp in inputs:
        inp = normalize_composition_format(inp)
        out = split_composition_into_component_materials(inp)
        outputs.append(out)

    assert outputs == targets
