import csv
import os
import matplotlib.pyplot as plt

# Points to MERFISH data with NaNs in it
csv_name = "/Users/cgcouto/Downloads/data_release_baysor_merfish_gut/assignment_6_boundaries/high_resolution_cell_boundaries_head.csv"

# Change file location for pictures as appropriate!
os.chdir("/Users/cgcouto/Downloads/data_release_baysor_merfish_gut/assignment_6_boundaries/polygon_pics")

# Cols 0 and 1 are the feature_uID and feature_ID respectively
# Cols 6 through 19 are the alternating x-y pairs

# Function that takes in two lists of x's and y's (separated by semicolons)
# and gets them into the desired POLYGON((X Y, ...)) format for SQL
def draw_polygon(x_string, y_string, layer, cellid):

    # First split based on NaNs (if any are present), then split by semi-colons to separate each coordinate
    x_split = [poly.split(';') for poly in x_string.replace(' ', '').split('NaN')]
    y_split = [poly.split(';') for poly in y_string.replace(' ', '').split('NaN')]

    # Remove any empty strings in our list of lists
    x = [[float(point) for point in poly if point != ''] for poly in x_split]
    y = [[float(point) for point in poly if point != ''] for poly in y_split]


    # If it's a MULTIPOLYGON, plot it and save as png
    if len(x) == len(y) and len(x) > 1 and len(y) > 1:
        y_points = []
        x_points = []
        x_start_and_end_points = []
        y_start_and_end_points = []

        for i in range(len(x)):
            if len(x[i]) >= 3 and len(y[i]) >= 3: # Needs to be at least four points total to be a SQL polygon
                
                # Duplicate start point on end
                x[i].append(x[i][0])
                y[i].append(y[i][0])

                # Add start/end points of each polygon to special lists for scattering
                x_start_and_end_points.append(x[i][0])
                y_start_and_end_points.append(y[i][0])

                # Add finished polygon to our list of them
                x_points.append(x[i])
                y_points.append(y[i])

        fig, ax = plt.subplots()

        # Plot all the polygons
        for j in range(len(x_points)):
            plt.plot(x_points[j], y_points[j])

        # Add the start/end points too
        plt.scatter(x_start_and_end_points, y_start_and_end_points, s=50)

        # Build filename and save out as a png
        name = "layer_" + str(layer) + "_id_" + str(cellid) + ".png"
        plt.savefig(name)
        plt.close()

    

# Open relevant csv readers and writers, parse the data line by line and save formatted
# versions in another csv file
with open(csv_name) as input:
    data_reader = csv.reader(input, delimiter=',')
    next(data_reader) # Skip the header! 
    for row in data_reader:
        for i in range(7):
            # The x's and y's live from cols 6 to 19 so we map from layer id to that
            cell_boundary = draw_polygon(row[6+2*i], row[7+2*i], i, row[1])

                