import seaborn as sns
import plotly
import cmasher as cmr
import matplotlib.colors as mcolors
import matplotlib

plasma_15 = [
    '#ff7900',
    '#bd0071',
    '#410E66',
    '#130066',
    '#060087',
    '#3d5e87',
    '#006687',
    '#00877d',
    '#008000',
    '#32cd32',
    '#00fa9a',
    '#adff2f',
    '#f3ff00',
    '#fee838',
    '#e1cc55'
]

plasma_10 = [
    '#ff7900',
    '#bd0071',
    '#410E66',
    '#060087',
    '#006687',
    '#008000',
    '#32cd32',
    '#00fa9a',
    '#f3ff00',
    '#e1cc55'
]

plasma_2 = [
    '#ff7900',
    '#46039f'
]


def list_of_hex_colours(base_cmap, N):
    """
    Return a list of colors from a colourmap as hex codes

    Arguments:
        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Author: FJC
    """
    cmap = matplotlib.cm.get_cmap(base_cmap, N)
    hex_codes = []
    for i in range(base_cmap.N):
        rgb = base_cmap(i)[:3]
        hex_codes.append(mcolors.rgb2hex(rgb))

    return hex_codes


spectral = sns.color_palette("Spectral", as_cmap=True)
spectral_hex = list_of_hex_colours(spectral, 0)

icefire = sns.color_palette("icefire", as_cmap=True)
icefire = list_of_hex_colours(icefire, 0)

viridis = sns.color_palette("viridis", as_cmap=True)
viridis = list_of_hex_colours(viridis, 0)

magma = sns.color_palette("magma", as_cmap=True)
magma = list_of_hex_colours(magma, 0)

rocket = sns.color_palette("rocket", as_cmap=True)
rocket = list_of_hex_colours(rocket, 0)

YlOrBr = sns.color_palette("YlOrBr", as_cmap=True)
YlOrBr = list_of_hex_colours(YlOrBr, 0)

maplas = plotly.colors.sequential.Plasma
maplas.pop()
maplas.pop()
maplas.pop()
maplas.append("#ff7900")

# plasma_cm = mcolors.LinearSegmentedColormap.from_list('plasma', maplas)
# plasma = list_of_hex_colours(plasma_cm, 50)

noinfer = cmr.take_cmap_colors('inferno', 30, cmap_range=(0.15, 0.85), return_fmt='hex')
mininoinfer = cmr.take_cmap_colors('inferno', 10, cmap_range=(0.15, 0.85), return_fmt='hex')
