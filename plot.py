import sys
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 50}

matplotlib.rc('font', **font)

def view_hexagon(sol):
    # Extract 3D coordinates and labels
    coordinates = []
    labels = []
    for x in sol:
        for y in sol[x]:
            for z in sol[x][y]:
                if int(x) + int(y) + int(z) == 0:
                    coordinates.append((int(x), int(y), int(z)))
                    labels.append(sol[x][y][z])

    # Horizontal cartesian coords
    hcoord = [c[0] for c in coordinates]

    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]
                                             ) / 3. for c in coordinates]

    fig, ax = plt.subplots(1)
    fig.tight_layout()
    ax.set_aspect('equal')

    # Add some coloured hexagons
    for x, y, l in zip(hcoord, vcoord, labels):
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3.,
                             orientation=np.radians(30), alpha=0.2, edgecolor='k')
        ax.add_patch(hex)
        ax.text(x, y, l, ha='center', va='center', size=10)

    # Also add scatter points in hexagon centres to keep axis fixed
    ax.scatter(hcoord, vcoord, alpha=0)

#   ax.get_xaxis().set_visible(False)
#   ax.get_yaxis().set_visible(False)
    ax.axis('off')

    plt.savefig(f"{sys.argv[1]}.pdf", dpi=300)
    print(f"{sys.argv[1]}.pdf")


with open(sys.argv[1], "r") as f:
    sol = json.load(f)
    view_hexagon(sol["hexagon"])
