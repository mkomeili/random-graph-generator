import bisect 
import numpy as np
from utils.utils import get_module_attr

def generate_data(graph_type):
    generate_function = get_module_attr('generators.{graph_type}'.format(graph_type=graph_type), 'generate_data')
    data = generate_function()
    return data

def generate_random_distribution(parameters):
    num_layers = np.random.randint(*parameters.get('layers_range', ()))
    x_start = np.random.randint(*parameters.get('x_start_range', ()))
    x_end = np.random.randint(*parameters.get('x_end_range', ()))
    num_samples = np.random.randint(*parameters.get('num_samples_range', ()))

    # go through each layer
    y_layers = np.array([])
    for _ in range (0, num_layers):
        # get layer's unique random values
        y_start = np.random.randint(*parameters.get('y_start_range', ()))
        y_end = np.random.randint(*parameters.get('y_end_range', ()))
        if (y_start < y_end): y = np.random.randint(y_start, y_end, num_samples)
        elif (y_start == y_end): y = np.random.randint(y_start, y_end+1, num_samples)
        else: y = np.random.randint(y_end, y_start, num_samples)
        y_layers = np.append(y_layers, y)

    X = np.linspace(x_start, x_end, num_samples)
    y_layers = y_layers.reshape((num_layers, -1))        
    return X, y_layers

def generate_midpoint_displacement(parameters):
    num_layers = np.random.randint(*parameters.get('layers_range', ()))
    x_start = np.random.randint(*parameters.get('x_start_range', ()))
    x_end = np.random.randint(*parameters.get('x_end_range', ()))
    num_iterations = np.random.randint(*parameters.get('num_iterations_range', ()))
    vertical_displacement = np.random.randint(*parameters.get('vertical_displacement_range', ()))
    roughness = np.random.uniform(*parameters.get('rough_range', ()))

    # go through each layer
    y_layers = np.array([])
    for _ in range (0, num_layers):
        # get layer's unique random values
        y_start = np.random.randint(*parameters.get('y_start_range', ()))
        y_end = np.random.randint(*parameters.get('y_end_range', ()))

        # generate random layer and append
        points = midpoint_displacement([x_start, y_start], [x_end, y_end], roughness, vertical_displacement, num_iterations)
        np_points = np.array(points)
        X = np_points[:,0]
        y = np_points[:,1]
        y_layers = np.append(y_layers, y)
    
    # reshape y_layers to match the length of X
    y_layers = y_layers.reshape((num_layers, -1))
    return X, y_layers

def midpoint_displacement(start, end, roughness, vertical_displacement, num_iterations):
    # initial declarations
    points = [start, end]
    iteration = 1
    
    while iteration <= num_iterations:
        points_tup = tuple(points)

        for i in range(len(points_tup)-1):
            # calculate x and y midpoint coordinate:
            # [(x_i + x_(i+1))/2, (y_i + y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2, [0, 1]))
            
            # displace midpoint y-coordinate
            midpoint[1] += np.random.choice([-vertical_displacement, vertical_displacement])
            midpoint[1] = max(0, midpoint[1])
            
            # insert the displaced midpoint in the current list of points         
            bisect.insort(points, midpoint)
    
        # reduce displacement range
        vertical_displacement *= 2 ** (-roughness)
        iteration += 1
    
    # returns points list in the form points = [[x_0, y_0], [x_1, y_1], ..., [x_n, y_n]]
    return points