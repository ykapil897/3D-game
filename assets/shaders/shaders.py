######################################################
# Write other shaders for minimap and crosshair (Since they need orthographic projection)

# Following is the standard perspective projection shader with uniform colour to all vertices. Can modify as required
standard_shader = {
    "vertex_shader" : '''
        
        #version 330 core
        layout(location = 0) in vec3 vertexPosition;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform float focalLength;

        void main() {
            vec4 camCoordPos = viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * vec4(focalLength * (camCoordPos[0] / abs(camCoordPos[2])), focalLength * (camCoordPos[1] / abs(camCoordPos[2])), camCoordPos[2], 1.0);
        }

        ''',

        "fragment_shader" : '''

        #version 330 core

        out vec4 outputColour;

        uniform vec4 objectColour;
        uniform vec3 camPosition;

        void main() {
            vec3 camPos = camPosition;
            outputColour = objectColour;
        }

        '''

}

edge_shader = {
    "vertex_shader" : '''
        
        #version 330 core
        layout(location = 0) in vec3 vertexPosition;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
        }

        ''',

        "fragment_shader" : '''

        #version 330 core

        out vec4 outputColour;

        void main() {
            outputColour = vec4(1.0, 1.0, 1.0, 1.0); // white color for edges
        }

        '''

}

# Add this to your shaders.py file
hud_shader = {
    "vertex_shader" : '''
        #version 330 core
        layout(location = 0) in vec3 vertexPosition;
        layout(location = 1) in vec3 vertexColor;
        
        uniform vec2 screenPosition;
        uniform float rotation;
        uniform vec3 color;
        
        out vec3 fragColor;
        
        void main() {
            // Apply rotation
            float cosAngle = cos(-rotation);
            float sinAngle = sin(-rotation);
            vec2 rotatedPos = vec2(
                vertexPosition.x * cosAngle - vertexPosition.y * sinAngle,
                vertexPosition.x * sinAngle + vertexPosition.y * cosAngle
            );
            
            // Scale and position the arrow in screen space
            vec2 finalPos = screenPosition + rotatedPos * 0.1;
            
            // Keep Z at 0 for 2D
            gl_Position = vec4(finalPos, 0.0, 1.0);
            
            // Pass color to fragment shader
            fragColor = mix(vertexColor, color, 0.8);
        }
    ''',

    "fragment_shader" : '''
        #version 330 core
        in vec3 fragColor;
        out vec4 outputColour;
        
        void main() {
            outputColour = vec4(fragColor, 1.0);
        }
    '''
}

# standard_shader = {
#     "vertex_shader" : '''
        
#         #version 330 core

#         layout(location = 0) in vec3 aPos; // Position attribute
#         layout(location = 1) in vec3 aNormal; // Normal attribute

#         uniform mat4 modelMatrix;
#         uniform mat4 viewMatrix;
#         uniform mat4 projectionMatrix;

#         out vec3 FragPos; // Position of the fragment in world space
#         out vec3 Normal; // Normal of the fragment in world space

#         void main()
#         {
#             FragPos = vec3(modelMatrix * vec4(aPos, 1.0));
#             Normal = mat3(transpose(inverse(modelMatrix))) * aNormal; // Transform normal to world space

#             gl_Position = projectionMatrix * viewMatrix * vec4(FragPos, 1.0);
#         }

#         ''',

#         "fragment_shader" : '''

#         #version 330 core

#         in vec3 FragPos; // Position of the fragment in world space
#         in vec3 Normal; // Normal of the fragment in world space

#         uniform vec3 objectColour;
#         uniform vec3 lightColour;
#         uniform vec3 lightPos;
#         uniform vec3 viewPos;

#         out vec4 FragColor;

#         void main()
#         {
#             // Ambient lighting
#             float ambientStrength = 0.1;
#             vec3 ambient = ambientStrength * lightColour;

#             // Diffuse lighting
#             vec3 norm = normalize(Normal);
#             vec3 lightDir = normalize(lightPos - FragPos);
#             float diff = max(dot(norm, lightDir), 0.0);
#             vec3 diffuse = diff * lightColour;

#             // Specular lighting
#             float specularStrength = 0.5;
#             vec3 viewDir = normalize(viewPos - FragPos);
#             vec3 reflectDir = reflect(-lightDir, norm);
#             float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
#             vec3 specular = specularStrength * spec * lightColour;

#             vec3 result = (ambient + diffuse + specular) * objectColour;
#             FragColor = vec4(result, 1.0);
#         }

#         '''

# }
######################################################