import json
import matplotlib.pyplot as plt
from skimage import io

# Takes the layer and id of a cell and draws its boundaries using matplotlib
def draw_cell(layer, id):

    # Load the data
    f = open('poly_per_z.json')
    data = json.load(f)

    # Arrays for storing x and y-coordinates
    x = []
    y = []

    coordinates = data[layer]['geometries'][id]['coordinates'][0]

    # Fill up the x's and y's
    for point in coordinates:
        x.append(point[0])
        y.append(point[1])
    
    # im = io.imread('/Users/cgcouto/Downloads/data_release_baysor_merfish_gut/data_analysis/cellpose/cell_boundaries/results/cellpose_dapi.tif')

    plt.plot(x,y)
    # plt.imshow(im[layer], cmap="gray")
    # print(coordinates)
    plt.show()

draw_cell(0,0)
# draw_cell(0,52) #Vertical line
# draw_cell(0,105) #Horizontal line
