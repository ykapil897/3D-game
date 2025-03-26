import numpy as np
import os
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import standard_shader

###############################################################
# Write logic to load OBJ Files:
    # Will depend on type of object. For example if normals needed along with vertex positions 
    # then will need to load slightly differently.

# Can use the provided OBJ files from assignment_2_template/assets/objects/models/
# Can also download other assets or model yourself in modelling softwares like blender

###############################################################
# Create Transporter, Pirates, Stars(optional), Minimap arrow, crosshair, planet, spacestation, laser


###############################################################

def load_obj(filepath, colors):
    vertices = []
    faces = []
    color_index = 0
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.split()
                color = colors[color_index % len(colors)]
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3]), color[0], color[1], color[2]])
                color_index += 1
            elif line.startswith('f '):
                parts = line.split()
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                faces.append(face)
    vertices = np.array(vertices, dtype=np.float32)
    faces = np.array(faces, dtype=np.int32)
    faces = faces.flatten()
    return vertices, faces

def create_object(filepath, shader, objType='generic'):
    vertices, faces = load_obj(filepath)
    properties = {
        'vertices': vertices,
        'indices': faces.flatten(),
        'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
        'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
        'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
        'colour': np.array([1.0, 0.0, 0.0, 1.0], dtype=np.float32)
    }
    return Object(objType, shader, properties)

# Create shader
# shader = Shader(standard_shader["vertex_shader"], standard_shader["fragment_shader"])

# Create objects
# transporter = create_object('./assets/objects/models/transporter.obj', shader, objType='transporter')
# pirate = create_object('./assets/objects/models/pirate.obj', shader, objType='pirate')
# planet = create_object('./assets/objects/models/planet.obj', shader, objType='planet')
# laser = create_object('./assets/objects/models/laser.obj', shader, objType='laser')
# spacestation = create_object('./assets/objects/models/spacestation.obj', shader, objType='spacestation')

transporterVerts, transporterInds = load_obj('./assets/objects/models/transporter.obj', colors=[[0, 0, 1], [0, 0, 0.5], [0, 0, 0.25]])
pirateVerts, pirateInds = load_obj('./assets/objects/models/pirate.obj', colors=[[0, 1, 0], [0, 0.5, 0], [0, 0.25, 0]])
planetVerts, planetInds = load_obj('./assets/objects/models/planet.obj', colors=[[0, 1, 1], [0, 0.5, 0.5], [0, 0.25, 0.25]])
laserVerts, laserInds = load_obj('./assets/objects/models/laser.obj', colors=[[1, 0, 1], [0.5, 0, 0.5], [0.25, 0, 0.25]])
spacestationVerts, spacestationInds = load_obj('./assets/objects/models/spacestation.obj', colors=[[1, 1, 0], [0.5, 0.5, 0], [0.25, 0.25, 0]])

transporterProps = {
    'vertices': transporterVerts,
    'indices': transporterInds,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)
}

pirateProps = {
    'vertices': pirateVerts,
    'indices': pirateInds,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32)
}

planetProps = {
    'vertices': planetVerts,
    'indices': planetInds,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([1.0, 0.0, 1.0, 1.0], dtype=np.float32)
}

laserProps = {
    'vertices': laserVerts,
    'indices': laserInds,
    'position': np.array([2.0, 2.0, 2.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([0.0, 1.0, 1.0, 1.0], dtype=np.float32)
}

spacestationProps = {
    'vertices': spacestationVerts,
    'indices': spacestationInds,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([1.0, 1.0, 0.0, 1.0], dtype=np.float32)
}


# Define vertices and indices for a simple 3D cube
cube_vertices = np.array([
    #   x,   y,   z,    r,   g,   b
    -1, -1, -1,   1.0, 0.0, 0.0,  # Red
    -1, -1,  1,   0.0, 1.0, 0.0,  # Green
    -1,  1, -1,   0.0, 0.0, 1.0,  # Blue
    -1,  1,  1,   1.0, 1.0, 0.0,  # Yellow
     1, -1, -1,   1.0, 0.0, 1.0,  # Magenta
     1, -1,  1,   0.0, 1.0, 1.0,  # Cyan
     1,  1, -1,   1.0, 1.0, 1.0,  # White
     1,  1,  1,   0.0, 0.0, 0.0   # Black
], dtype=np.float32)

cube_indices = np.array([
    0, 1, 3,  
    0, 3, 2,  
    4, 5, 7,  
    4, 7, 6,  
    0, 1, 5,  
    0, 5, 4,  
    2, 3, 7, 
    2, 7, 6,  
    0, 2, 6,  
    0, 6, 4,  
    1, 3, 7,  
    1, 7, 5  
], dtype=np.uint32)

cube_props = {
    'vertices': cube_vertices,
    'indices': cube_indices,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)  # Red color
}

# Define vertices and indices for a simple arrow shape
arrow_vertices = np.array([
    #   x,   y,   z,    r,   g,   b
     0.0,  0.5,  0.0,  1.0, 0.0, 0.0,  # Tip (red)
    -0.3, -0.5,  0.0,  1.0, 0.3, 0.0,  # Bottom left
     0.3, -0.5,  0.0,  1.0, 0.3, 0.0,  # Bottom right
     0.0,  0.2,  0.0,  1.0, 0.6, 0.0,  # Middle
    -0.2, -0.2,  0.0,  1.0, 0.3, 0.0,  # Left middle
     0.2, -0.2,  0.0,  1.0, 0.3, 0.0,  # Right middle
], dtype=np.float32)

arrow_indices = np.array([
    0, 1, 2,  # Tip triangle
    3, 4, 5   # Base quadrilateral
], dtype=np.uint32)

arrow_props = {
    'vertices': arrow_vertices,
    'indices': arrow_indices,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32)  # Red color
}

# Initialize crosshair for 1st person view
crosshair_vertices = np.array([
    # Horizontal line
    -0.25, 0.02, 0.0, 1.0, 1.0, 1.0,  # Top left
    -0.25, -0.02, 0.0, 1.0, 1.0, 1.0,  # Bottom left
    0.25, -0.02, 0.0, 1.0, 1.0, 1.0,  # Bottom right
    0.25, 0.02, 0.0, 1.0, 1.0, 1.0,  # Top right
     
    # Vertical line 
    -0.02, 0.25, 0.0, 1.0, 1.0, 1.0,  # Top left
    -0.02, -0.25, 0.0, 1.0, 1.0, 1.0,  # Bottom left
    0.02, -0.25, 0.0, 1.0, 1.0, 1.0,  # Bottom right
    0.02, 0.25, 0.0, 1.0, 1.0, 1.0,  # Top right
], dtype=np.float32)

crosshair_indices = np.array([
    0, 1, 2, 0, 2, 3,  # Horizontal line
    4, 5, 6, 4, 6, 7  # Vertical line
], dtype=np.uint32)
        
crosshair_props = {
    'vertices': crosshair_vertices,
    'indices': crosshair_indices,
    'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
    'scale': np.array([1.0, 1.0, 1.0], dtype=np.float32),
    'colour': np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
}


# laser_vertices = np.array([
#     # Position (XYZ)        # Color (RGB)
#     # Front face (circle)
#     0.0, 0.0, 1.0,          1.0, 0.2, 0.2,  # Center
#     10.5, 0.0, 1.0,          1.0, 0.2, 0.2,  # Point 1
#     10.35, 10.35, 1.0,        1.0, 0.2, 0.2,  # Point 2
#     0.0, 10.5, 1.0,          1.0, 0.2, 0.2,  # Point 3
#     -10.35, 10.35, 1.0,       1.0, 0.2, 0.2,  # Point 4
#     -10.5, 0.0, 1.0,         1.0, 0.2, 0.2,  # Point 5
#     -10.35, -10.35, 1.0,      1.0, 0.2, 0.2,  # Point 6
#     0.0, -10.5, 1.0,         1.0, 0.2, 0.2,  # Point 7
#     10.35, -10.35, 1.0,       1.0, 0.2, 0.2,  # Point 8
    
#     # Back face (circle)
#     0.0, 0.0, -1.0,         1.0, 0.0, 0.0,  # Center
#     10.5, 0.0, -1.0,         1.0, 0.0, 0.0,  # Point 1
#     10.35, 10.35, -1.0,       1.0, 0.0, 0.0,  # Point 2
#     0.0, 10.5, -1.0,         1.0, 0.0, 0.0,  # Point 3
#     -10.35, 10.35, -1.0,      1.0, 0.0, 0.0,  # Point 4
#     -10.5, 0.0, -1.0,        1.0, 0.0, 0.0,  # Point 5
#     -10.35, -10.35, -1.0,     1.0, 0.0, 0.0,  # Point 6
#     0.0, -10.5, -1.0,        1.0, 0.0, 0.0,  # Point 7
#     10.35, -10.35, -1.0,      1.0, 0.0, 0.0,  # Point 8
# ], dtype=np.float32)

# # Create indices for a cylindrical laser beam
# laser_indices = np.array([
#     # Front face triangles
#     0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 7, 0, 7, 8, 0, 8, 1,
#     # Back face triangles
#     9, 11, 10, 9, 12, 11, 9, 13, 12, 9, 14, 13, 9, 15, 14, 9, 16, 15, 9, 17, 16, 9, 10, 17,
#     # Side quad 1
#     1, 10, 11, 1, 11, 2,
#     # Side quad 2
#     2, 11, 12, 2, 12, 3,
#     # Side quad 3
#     3, 12, 13, 3, 13, 4,
#     # Side quad 4
#     4, 13, 14, 4, 14, 5,
#     # Side quad 5
#     5, 14, 15, 5, 15, 6,
#     # Side quad 6
#     6, 15, 16, 6, 16, 7,
#     # Side quad 7
#     7, 16, 17, 7, 17, 8,
#     # Side quad 8
#     8, 17, 10, 8, 10, 1
# ], dtype=np.uint32)

# laserProps = {
#     'vertices': laser_vertices,
#     'indices': laser_indices,
#     'position': np.array([0.0, 0.0, 0.0], dtype=np.float32),
#     'rotation': np.array([0.0, 0.0, 0.0], dtype=np.float32),
#     'scale': np.array([0.5, 0.5, 4.0], dtype=np.float32),  # Make it longer and thinner
#     'colour': np.array([1.0, 0.2, 0.0, 1.0], dtype=np.float32)  # Bright orange-red
# }