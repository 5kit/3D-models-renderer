import json

def parse_obj_file(file_path, scale):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'v':  # Vertex definition
                x, y, z = map(float, parts[1:4])
                vertices.append([x*scale, y*scale, z*scale])
            elif parts[0] == 'f':  # Face definition
                # Extract vertex indices (faces can have extra data, so we only take the first part)
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                # Add the face with default color 'ffffff'
                faces.append(["ffffff"] + [face[0], face[1], face[2]])
                if len(face) == 4:
                    faces.append(["ffffff"] + [face[0], face[2], face[3]])

    return vertices, faces

# Example usage
file_path = 'Blender/Chicken_01.obj'  # Replace with your OBJ file path
scale = 0.5
vertices, faces = parse_obj_file(file_path, scale)

name = input("Enter file name: ")
filename = "Models/" + name + ".obj"

data = [[v for v in vertices], faces]

with open(filename, 'w') as objF:
    json.dump(data,objF)
