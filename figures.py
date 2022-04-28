import toytree
import toyplot
import toyplot.svg
import numpy as np
from decimal import Decimal

def render(tree_name, depth, clades, ancestors, ds, colour_labels=False, step=None, suffix=None):
    with open("trees/{}.tre".format(tree_name)) as inf:
       newick = inf.read().strip()

    tre = toytree.tree(newick)
    tre = tre.root("Hittite")

    root_age = round(tre.treenode.height)

    if ds == "broad":
        height = 1150
        if suffix:
            height = 1300
    elif ds == "medium":
        height = 1050
    elif ds == "narrow":
        height = 700

    if not colour_labels:
        width = 1000
    else:
        width = 600

    canvas = toyplot.Canvas(width=width, height=height)

    ax0 = canvas.cartesian(bounds=(0, width, 30, height - 30))
    ax0.show = True
    ax0.x.show = True
    ax0.y.show = False
    ax0.x.ticks.show = True
    ax0.x.spine.position = "high"
    ax0.x.spine.show = False

    if step is None: 
        step = 500
    locs = np.linspace(0, (-depth) + step, depth // step)

    fmt = "{:.0f}"
    ax0.x.ticks.locator = toyplot.locator.Explicit(
        locations=locs,
        labels=[fmt.format(i) for i in np.abs(locs)],
        )

    if suffix:
        ax0.x.ticks.labels.style = {"font-size": "16px"}

    if not suffix: 
        ax0.vlines(locs, style={"stroke": "LightGray", "stroke-dasharray": "8,10"})

    colour_map = {}
    if not suffix:
        for a in ancestors:
            colour_map[a] = "IndianRed"
    colour_map.update(clades)

    if not colour_labels:
        opts = {"edge_colors": tre.get_edge_values_mapped(colour_map)}
    else:
        ncols = {}
        for clade, col in clades.items():
            for n in clade:
                ncols[n] = col
        opts = {"tip_labels_colors": [ncols[n] for n in tre.get_tip_labels()]}

    tip_names = tre.get_tip_labels()
    tip_labels = [name.replace("_", " ") for name in tip_names]
    if suffix:
        for i, lbl in enumerate(tip_labels):
            if lbl == "Eastern Armenian":
                tip_labels[i] = "East. Armenian"
            if lbl == "Upper Sorbian":
                tip_labels[i] = "Up. Sorbian"
            if lbl == "Lower Sorbian":
                tip_labels[i] = "Low. Sorbian"
            if lbl == "Luxembourgish":
                tip_labels[i] = "Lux'bourgish"

    edge_style = {"stroke": "Gray"}
    if suffix:
        edge_style["stroke-width"] = 4

    tre.draw(tip_labels=tip_labels, tip_labels_style={"font-size": "12px" if not suffix else "14px", "-toyplot-anchor-shift": "5px"}, axes=ax0, padding = 5, use_edge_lengths=True, edge_style=edge_style, **opts)

    ax0.x.domain.min = -depth
    ax0.x.domain.show = True

    if not suffix:
        canvas.text(150, height - 50, "Root Age: {} years B.P.".format(root_age), style={"font-size": "18px"})
    toyplot.svg.render(canvas, "figs/{}{}.svg".format(tree_name, "-" + suffix if suffix else ""))

def albanian(ds):
    if ds == "broad" or ds == "medium":
        return ("Tosk", "Arvanitika")

def greek(ds):
    if ds == "broad" or ds == "medium" or ds == "narrow":
        return ("Ancient_Greek", "Modern_Greek")


def armenian(ds):
    if ds == "broad" or ds == "medium" or ds == "narrow":
        return ("Classical_Armenian", "Adapazar", "Eastern_Armenian")


def tocharian(ds):
    if ds == "broad":
        return ("Tocharian_A", "Tocharian_B")
    if ds == "medium" or ds == "narrow":
        return ("Tocharian_B",)

def baltic(ds):
    if ds == "broad":
        return ("Lithuanian", "Latvian", "Old_Prussian")
    if ds == "medium":
        return ("Lithuanian", "Latvian")


def slavic(ds):
    if ds == "broad":
        return ("Russian", "Ukrainian", "Belarusian", "Polish", "Slovak", "Czech", "Upper_Sorbian",
         "Lower_Sorbian", "Bulgarian", "Macedonian", "Serbian", "Slovenian", "Old_Church_Slavic")
    if ds == "medium":
        return ("Russian", "Ukrainian", "Belarusian", "Polish", "Slovak", "Czech", "Upper_Sorbian",
         "Bulgarian", "Macedonian", "Serbian", "Slovenian", "Old_Church_Slavic")
    if ds == "narrow":
        return ("Old_Church_Slavic",) 


def celtic(ds):
    if ds == "broad" or ds == "medium":
        return ("Old_Irish", "Irish", "Scots_Gaelic", "Cornish", "Breton", "Welsh")
    if ds == "narrow":
        return ("Old_Irish", "Irish", "Scots_Gaelic")

def romance(ds):
    if ds == "broad":
        return ("Latin", "Nuorese", "Cagliari", "Arumanian", "Portuguese", "Spanish", "Catalan", "French", "Walloon", "Provencal", "Romansh", "Friulian", "Ladin", "Italian", "Romanian")
    if ds == "medium" or ds == "narrow":
        return ("Latin", "Nuorese", "Cagliari", "Portuguese", "Spanish", "Catalan", "French", "Walloon", "Provencal", "Romansh", "Friulian", "Ladin", "Italian", "Romanian")

def germanic(ds):
    if ds == "medium" or ds == "broad":
        return ("Gothic", "Old_High_German", "German", "Swiss_German",
                "Luxembourgish", "Frisian", "Dutch", "Flemish",
                "Afrikaans", "Old_English", "English", "Swedish", "Danish",
                "Norwegian", "Old_West_Norse", "Faroese", "Icelandic")
    if ds == "narrow":
        return ("Gothic", "Old_High_German", "German", "Swiss_German",
                "Luxembourgish", "Old_English", "English",
                "Norwegian", "Old_West_Norse", "Faroese", "Icelandic")

def iranian(ds):
    if ds == "broad":
        return ("Avestan", "Digor_Ossetic", "Persian", "Tajik", "Baluchi", "Pashto", "Waziri",
                "Sogdian", "Wakhi", "Sariqoli", "Shughni", "Zazaki", "Kurdish")
    if ds == "medium":
        return ("Avestan", "Digor_Ossetic", "Persian", "Tajik", "Baluchi", "Pashto", "Waziri")
    if ds == "narrow":
        return ("Avestan",) 


def indian(ds):
    if ds == "broad":
        return ("Vedic_Sanskrit", "Kashmiri", "Romani", "Singhalese", "Sindhi", "Marwari", "Nepali",
                "Bengali", "Oriya", "Assamese", "Gujarati", "Marathi",
                "Bihari", "Hindi", "Urdu", "Panjabi", "Lahnda")
    if ds == "medium":
        return ("Vedic_Sanskrit", "Kashmiri", "Romani", "Singhalese", "Nepali",
                "Bengali", "Oriya", "Assamese", "Gujarati", "Marathi",
                "Bihari", "Hindi", "Urdu", "Panjabi", "Lahnda")
    if ds == "narrow":
        return ("Vedic_Sanskrit", "Kashmiri", "Romani", "Singhalese", "Nepali",
                "Bengali", "Oriya", "Assamese", "Gujarati", "Marathi",
                "Bihari", "Hindi", "Urdu", "Panjabi", "Lahnda")

if __name__ == "__main__":
    def clades(ds):
        clades = {("Hittite",): "SaddleBrown"}

        def add_clade(fn, colour):
            clade = fn(ds)
            if clade:
                clades[clade] = colour

        add_clade(albanian, "MediumTurquoise")
        add_clade(greek, "LightSeaGreen")
        add_clade(armenian, "SteelBlue")
        add_clade(tocharian, "DarkSalmon")
        add_clade(baltic, "OliveDrab")
        add_clade(slavic, "MediumSeaGreen")
        add_clade(iranian, "LightSlateGray")
        add_clade(indian, "MediumPurple")
        add_clade(germanic, "YellowGreen")
        add_clade(romance, "BurlyWood")
        add_clade(celtic, "RosyBrown")
        return clades

    ancestors = [
        "Ancient_Greek",
        "Classical_Armenian",
        "Vedic_Sanskrit",
        "Old_English",
        "Old_High_German",
        "Old_West_Norse",
        "Old_Irish",
        "Latin",
    ]
    
    render("runs24-broad-generalised", 8500, clades("broad"), ancestors, "broad")
    render("runs24-broad-constant", 8500, clades("broad"), ancestors, "broad")
    render("runs24-medium-generalised", 8500, clades("medium"), ancestors, "medium")
    render("runs24-medium-constant", 8500, clades("medium"), ancestors, "medium")
    render("runs24-narrow-constant", 8500, clades("narrow"), ancestors, "narrow")

    render("runs26-conv1", 5000, clades("narrow"), ancestors, "narrow", colour_labels=True)
    render("runs26-conv2", 8000, clades("narrow"), ancestors, "narrow", colour_labels=True)
    render("runs26-conv3", 10000, clades("narrow"), ancestors, "narrow", colour_labels=True, step=1000)
    render("runs26-conv4", 7000, clades("narrow"), ancestors, "narrow", colour_labels=True)

    render("runs24-broad-constant", 6500, clades("broad"), ancestors, "broad", suffix="poster")

