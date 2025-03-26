import imgui
import numpy as np
from OpenGL.GL import *
from utils.graphics import Object, Camera, Shader
from assets.objects.objects import transporterProps, pirateProps, planetProps, laserProps, spacestationProps, cube_props, arrow_props, crosshair_props
from assets.shaders.shaders import standard_shader, edge_shader, hud_shader

class Game:
    def __init__(self, height, width, gui):
        self.gui = gui
        self.height = height
        self.width = width
        self.screen = 0
        self.transporter_speed = 0.0
        self.max_speed = 10.0
        self.acceleration = 0.1
        self.view_mode = 1  # 1: 3rd person, 2: 1st person
        self.lasers = []  # Store active lasers
        self.laser_cooldown = 0.0  # Time until next laser can be fired
        self.laser_cooldown_time = 0.3  # Cooldown period between shots

    def InitScene(self):
        if self.screen == 1:
            # print("Initializing scene")
            ############################################################################
            # Define world state
            self.camera = Camera(self.height, self.width)
            self.shaders = [Shader(standard_shader["vertex_shader"], standard_shader["fragment_shader"])]
            self.edge_shader = Shader(edge_shader["vertex_shader"], edge_shader["fragment_shader"])
            self.hud_shader = Shader(hud_shader["vertex_shader"], hud_shader["fragment_shader"])
            self.gameState = {
                'transporter': None,
                'pirates': [],
                'planets': [],
                'spaceStations': [],
                'cube': None,
                'arrow': None,  
                'lasers': [],
                'crosshair': None,
                'test': None
            } # Can define keys as 'transporter', 'pirates', etc. Their values being Object() or list of Object()
            ############################################################################

            # self.gameState['test'] = Object('test', self.shaders[0], laserProps)
            # Initialize crosshair
            self.gameState['crosshair'] = Object('crosshair', self.hud_shader, crosshair_props)

            # Initialize minimap arrow
            self.gameState['arrow'] = Object('arrow', self.hud_shader, arrow_props)
            self.gameState['arrow'].properties['scale'] = np.array([1.0, 1.0, 1.0], dtype=np.float32)

            # Define world boundarie
            self.worldMin = np.array([-500, -500, -500], dtype=np.float32)
            self.worldMax = np.array([500, 500, 500], dtype=np.float32)
            ############################################################################
            # Initialize Planets and space stations (Randomly place n planets and n spacestations within world bounds)
            self.n_planets = 20
            self.n_spaceStations = 20
            for _ in range(self.n_planets):
                position = np.random.uniform(self.worldMin, self.worldMax)
                new_planet = Object('planet', self.shaders[0], planetProps)
                new_planet.properties['position'] = position
                self.gameState['planets'].append(new_planet)

                new_spaceStation = Object('spaceStation', self.shaders[0], spacestationProps)
                new_spaceStation.properties['position'] = position + np.array([0, 0, 10], dtype=np.float32)
                self.gameState['spaceStations'].append(new_spaceStation)
            
            new_planet = Object('planet', self.shaders[0], planetProps)
            new_planet.properties['position'] = np.array([0, -15, 0], dtype=np.float32)
            self.gameState['planets'].append(new_planet)

            new_spaceStation = Object('spaceStation', self.shaders[0], spacestationProps)
            new_spaceStation.properties['position'] = np.array([0, -15, 10], dtype=np.float32)
            self.gameState['spaceStations'].append(new_spaceStation)

            self.destination_index = np.random.randint(0, len(self.gameState['spaceStations']))
            self.gameState['spaceStations'][self.destination_index].properties['colour'] = np.array([1.0, 0.8, 0.2, 1.0], dtype=np.float32)  # Make it golden
            # print("Planet and spacestation initialized")
            ############################################################################
            # Initialize transporter (Randomly choose start and end planet, and initialize transporter at start planet)
            start_planet = np.random.choice(self.gameState['planets'])
            self.gameState['transporter'] = Object('transporter', self.shaders[0], transporterProps)
            # self.gameState['transporter'].properties['position'] = start_planet.properties['position']
            self.gameState['transporter'].properties['position'] = np.array([-1, -1, -1], dtype=np.float32)    
            # print("Transporter initialized")
            ############################################################################
            # Initialize Pirates (Spawn at random locations within world bounds)
            self.n_pirates = 20 # for example
            for _ in range(self.n_pirates):
                position = np.random.uniform(self.worldMin, self.worldMax)
                new_pirate = Object('pirate', self.shaders[0], pirateProps) 
                new_pirate.properties['position'] = position
                self.gameState['pirates'].append(new_pirate)
            # print("Pirate initialized")

            # cube = Object('cube', self.shaders[0], cube_props)
            # self.gameState['cube'] = cube
            ############################################################################
            # Initialize minimap arrow (Need to write orthographic projection shader for it)
            self.camera.position = np.array([-15/1.5,-1,4/1.5], dtype=np.float32)
            self.camera.lookAt = np.array([1,0,0], dtype=np.float32)

            # self.gameState['cube'].properties["scale"] = np.array([0.5, 0.5, 0.5], dtype=np.float32)

            ############################################################################

    def ProcessFrame(self, inputs, time):

        self.UpdateScene(inputs, time)
        self.DrawScene()
        self.DrawText()

    def DrawText(self):
        if self.screen == 0:
            pass

        if self.screen == 2: # YOU WON Screen
            pass

        if self.screen == 3: # GAME OVER Screen
            pass
        
    def UpdateScene(self, inputs, time):
        if self.screen == 0: # Example start screen
            # print(f'screen: {self.screen}')
            # if inputs["1"]:
            #     self.screen = 1
            #     self.InitScene()
            pass
        if self.screen == 2: # YOU WON
            pass
        if self.screen == 3: # GAME OVER
            pass
        
        if self.screen == 1: # Game screen
            # print(f'screen: {self.screen}')
            ############################################################################
            # Manage inputs 
            transporter = self.gameState['transporter']

            # Handle view mode switching
            if inputs["R_CLICK"]:
                self.view_mode = 2  # 1st person view when right-click is held
            else:
                self.view_mode = 1  # 3rd person view by default
            
            # Update laser cooldown timer
            if self.laser_cooldown > 0:
                self.laser_cooldown -= time["deltaTime"]

            # Handle input based on view mode
            if self.view_mode == 1:  # 3rd person view: can maneuver transporter
                rotation_speed = 0.025
                if inputs["W"]:
                    transporter.properties['rotation'][0] -= rotation_speed  # Pitch down
                if inputs["S"]:
                    transporter.properties['rotation'][0] += rotation_speed  # Pitch up
                if inputs["A"]:
                    transporter.properties['rotation'][1] -= rotation_speed  # Yaw left
                if inputs["D"]:
                    transporter.properties['rotation'][1] += rotation_speed  # Yaw right
                if inputs["Q"]:
                    transporter.properties['rotation'][2] -= rotation_speed  # Roll left
                if inputs["E"]:
                    transporter.properties['rotation'][2] += rotation_speed  # Roll right
                if inputs["SPACE"]:
                    self.transporter_speed += self.acceleration  # Accelerate forward
                    if self.transporter_speed > self.max_speed:
                        self.transporter_speed = self.max_speed

            elif self.view_mode == 2:  # 1st person view: can shoot lasers
                # Mouse movement can be used for aiming if needed
                # mouseDelta = inputs["mouseDelta"]
                
                # Fire laser with left click if cooldown is over
                if inputs["L_CLICK"] and self.laser_cooldown <= 0:
                    forward_dir = self.camera.lookAt - self.camera.position
                    # Create a new laser object
                    new_laser = Object('laser', self.shaders[0], laserProps)
                    # Position it at the transporter's position
                    new_laser.properties['position'] =self.camera.position + 2*forward_dir
                    # Use the same rotation as the transporter
                    new_laser.properties['rotation'] = np.copy(transporter.properties['rotation'])
                    # Adjust scale if needed
                    new_laser.properties['scale'] = np.array([1.0, 1.0, 1.0], dtype=np.float32)
                    # Calculate direction based on the forward direction
                    # Store the direction for updating laser position
                    new_laser.properties['direction'] = forward_dir
                    # Store the creation time
                    new_laser.properties['creation_time'] = time["currentTime"]
                    new_laser.properties['colour'] = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
                    # Add to game state
                    self.gameState['lasers'].append(new_laser)
                    # Add after creating a new laser:
                    # print(f"Laser created at position: {new_laser.properties['position']}")
                    # print(f"Laser direction: {new_laser.properties['direction']}")
                    # print(f"Total lasers: {len(self.gameState['lasers'])}")
                    # Set cooldown
                    self.laser_cooldown = self.laser_cooldown_time

            # Calculate forward direction
            rotation_matrix = np.array([
                [np.cos(transporter.properties['rotation'][1]) * np.cos(transporter.properties['rotation'][0]), 
                 np.sin(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][1]) * np.cos(transporter.properties['rotation'][0]) - np.cos(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][0]), 
                 np.cos(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][1]) * np.cos(transporter.properties['rotation'][0]) + np.sin(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][0])],
                [np.cos(transporter.properties['rotation'][1]) * np.sin(transporter.properties['rotation'][0]), 
                 np.sin(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][1]) * np.sin(transporter.properties['rotation'][0]) + np.cos(transporter.properties['rotation'][2]) * np.cos(transporter.properties['rotation'][0]), 
                 np.cos(transporter.properties['rotation'][2]) * np.sin(transporter.properties['rotation'][1]) * np.sin(transporter.properties['rotation'][0]) - np.sin(transporter.properties['rotation'][2]) * np.cos(transporter.properties['rotation'][0])],
                [-np.sin(transporter.properties['rotation'][1]), 
                 np.sin(transporter.properties['rotation'][2]) * np.cos(transporter.properties['rotation'][1]), 
                 np.cos(transporter.properties['rotation'][2]) * np.cos(transporter.properties['rotation'][1])]
            ], dtype=np.float32)
            forward_direction = rotation_matrix @ np.array([0, 0, -1], dtype=np.float32)
            # Rotate forward direction by 90 degrees about the y-axis
            rotation_90_y = np.array([
                [0, 0, -1],
                [0, 1, 0],
                [1, 0, 0]
            ], dtype=np.float32)
            forward_direction = rotation_90_y @ forward_direction
            ############################################################################
            # Update transporter (Update velocity, position, and check for collisions)
            transporter.properties['position'] += forward_direction * self.transporter_speed * time["deltaTime"]

            # Check collision with destination spacestation
            destination_station = self.gameState['spaceStations'][self.destination_index]
            dist_to_destination = np.linalg.norm(transporter.properties['position'] - destination_station.properties['position'])
            if dist_to_destination < 5.0:  # Collision threshold
                self.screen = 2  # YOU WON screen

            ############################################################################
            # Update spacestations (Update velocity and position to revolve around respective planet)
            for i, spaceStation in enumerate(self.gameState['spaceStations']):
                planet = self.gameState['planets'][i % len(self.gameState['planets'])]
                angle = time["currentTime"] * 0.5  # Adjust the speed of revolution as needed
                radius = 10.0  # Adjust the radius of revolution as needed
                spaceStation.properties['position'] = planet.properties['position'] + np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    0
                ], dtype=np.float32)

            ############################################################################
            # Update Minimap Arrow: (Set direction based on transporter velocity direction and target direction)
            # Calculate direction to destination
            destination_station = self.gameState['spaceStations'][self.destination_index]
            dir_to_destination = destination_station.properties['position'] - transporter.properties['position']

            # Calculate horizontal direction (XY plane)
            horizontal_dir = np.array([dir_to_destination[0], dir_to_destination[1], 0], dtype=np.float32)
            horizontal_norm = np.linalg.norm(horizontal_dir)

            if horizontal_norm > 0.001:  # Avoid near-zero vectors
                horizontal_dir = horizontal_dir / horizontal_norm
                # Calculate angle in the XY plane - arctan2 returns angle in radians
                angle = np.arctan2(horizontal_dir[1], horizontal_dir[0])
                
                # Add offset since our arrow points upward (positive Y) by default
                # arctan2 returns angle from positive X axis, so add π/2 to rotate from +Y
                self.gameState['arrow'].properties['rotation'][2] = angle + np.pi/2
            else:
                # Default angle if no clear direction
                self.gameState['arrow'].properties['rotation'][2] = np.pi/2

            # Debug output
            # print(f"Direction: ({horizontal_dir[0]:.2f}, {horizontal_dir[1]:.2f}), Angle: {self.gameState['arrow'].properties['rotation'][2]:.2f}")

            # Adjust color based on Z difference (red if above, blue if below)
            z_diff = dir_to_destination[2]
            if z_diff > 0:  # Destination is above
                red = min(1.0, 0.5 + abs(z_diff) * 0.005)
                blue = max(0.0, 1.0 - abs(z_diff) * 0.005)
                self.gameState['arrow'].properties['colour'] = np.array([red, 0.2, blue, 1.0], dtype=np.float32)
            else:  # Destination is below
                red = max(0.0, 1.0 - abs(z_diff) * 0.005)
                blue = min(1.0, 0.5 + abs(z_diff) * 0.005)
                self.gameState['arrow'].properties['colour'] = np.array([red, 0.2, blue, 1.0], dtype=np.float32)

            ############################################################################
            # Update Lasers (Update position of any currently shot lasers, make sure to despawn them if they go too far to save computation)
            laser_speed = 5.0
            max_laser_distance = 500.0
            # Create a list to hold lasers that should be removed
            lasers_to_remove = []
            for laser in self.gameState['lasers']:
                # Move laser forward
                laser.properties['position'] -= laser.properties['direction'] * laser_speed * time["deltaTime"]
                # print(f"Laser position: {laser.properties['position']}")
                # Check if laser has traveled too far
                distance_traveled = np.linalg.norm(laser.properties['position'] - transporter.properties['position'])
                if distance_traveled > max_laser_distance:
                    lasers_to_remove.append(laser)
                
                # Check for collisions with pirates
                for pirate in self.gameState['pirates']:
                    laser_to_pirate = pirate.properties['position'] - laser.properties['position']
                    distance = np.linalg.norm(laser_to_pirate)
                    if distance < 3.0:  # Collision threshold
                        if pirate in self.gameState['pirates']:  # Make sure pirate hasn't been removed yet
                            # Remove the pirate
                            self.gameState['pirates'].remove(pirate)
                            # print(f"Pirate removed at position: {pirate.properties['position']}")
                        lasers_to_remove.append(laser)
                        break
            
            # Remove lasers that have traveled too far or hit pirates
            for laser in lasers_to_remove:
                if laser in self.gameState['lasers']:
                    self.gameState['lasers'].remove(laser)
                    # print(f"Laser removed at position: {laser.properties['position']}")
            
            ############################################################################
            # Update Pirates (Write logic to update their velocity based on transporter position, and check for collision with laser or transporter)
            pirate_speed = 5.0  # Adjust as needed
            collision_distance_transporter = 3.0  # Collision distance for transporter
            collision_distance_objects = 5.0  # Collision distance for other objects
            
            for pirate in self.gameState['pirates']:
                # Calculate direction vector from pirate to transporter
                direction_to_transporter = transporter.properties['position'] - pirate.properties['position']
                
                # Normalize the direction vector (make it unit length)
                distance_to_transporter = np.linalg.norm(direction_to_transporter)
                
                # Check collision with transporter
                if distance_to_transporter < collision_distance_transporter:
                    # Collision detected - Game Over!
                    self.screen = 3  # Set to game over screen
                    break
                    
                if distance_to_transporter > 0:  # Avoid division by zero
                    direction_to_transporter = direction_to_transporter / distance_to_transporter
                    
                # Initialize avoidance force
                avoidance_force = np.zeros(3, dtype=np.float32)
                
                # Avoid other pirates
                for other_pirate in self.gameState['pirates']:
                    if other_pirate != pirate:
                        dir_to_other = pirate.properties['position'] - other_pirate.properties['position']
                        dist_to_other = np.linalg.norm(dir_to_other)
                        if dist_to_other < collision_distance_objects and dist_to_other > 0:
                            avoidance_force += dir_to_other / (dist_to_other * dist_to_other) * 10.0
                
                # Avoid planets
                for planet in self.gameState['planets']:
                    dir_to_planet = pirate.properties['position'] - planet.properties['position']
                    dist_to_planet = np.linalg.norm(dir_to_planet)
                    if dist_to_planet < collision_distance_objects * 3 and dist_to_planet > 0:
                        avoidance_force += dir_to_planet / (dist_to_planet * dist_to_planet) * 20.0
                        
                # Avoid spacestations
                for station in self.gameState['spaceStations']:
                    dir_to_station = pirate.properties['position'] - station.properties['position']
                    dist_to_station = np.linalg.norm(dir_to_station)
                    if dist_to_station < collision_distance_objects and dist_to_station > 0:
                        avoidance_force += dir_to_station / (dist_to_station * dist_to_station) * 15.0
                        
                # Normalize avoidance force if it's not zero
                if np.linalg.norm(avoidance_force) > 0:
                    avoidance_force = avoidance_force / np.linalg.norm(avoidance_force)
                    
                # Combine pursuit and avoidance (70% pursuit, 30% avoidance)
                combined_direction = 0.7 * direction_to_transporter + 0.3 * avoidance_force
                if np.linalg.norm(combined_direction) > 0:
                    combined_direction = combined_direction / np.linalg.norm(combined_direction)
                    
                # Update pirate position
                pirate.properties['position'] += combined_direction * pirate_speed * time["deltaTime"]
                
                # Make pirates face the direction they're moving
                if np.linalg.norm(combined_direction) > 0:
                    # Simple rotation to face the movement direction
                    pirate_forward = combined_direction
                    pirate.properties['rotation'][1] = np.arctan2(pirate_forward[0], pirate_forward[2])
                    pirate.properties['rotation'][0] = np.arctan2(-pirate_forward[1], np.sqrt(pirate_forward[0]**2 + pirate_forward[2]**2))


            ############################################################################
            # Update Camera (Check for view (3rd person or 1st person) and set position and LookAt accordingly)
            transporter_position = self.gameState['transporter'].properties['position']
            transporter_rotation = self.gameState['transporter'].properties['rotation']

            # Calculate the camera position behind the transporter
            offset = np.array([0, -10, 5], dtype=np.float32)  # Adjust the offset as needed
            rotation_matrix = np.array([
                [np.cos(transporter_rotation[1]) * np.cos(transporter_rotation[0]), 
                 np.sin(transporter_rotation[2]) * np.sin(transporter_rotation[1]) * np.cos(transporter_rotation[0]) - np.cos(transporter_rotation[2]) * np.sin(transporter_rotation[0]), 
                 np.cos(transporter_rotation[2]) * np.sin(transporter_rotation[1]) * np.cos(transporter_rotation[0]) + np.sin(transporter_rotation[2]) * np.sin(transporter_rotation[0])],
                [np.cos(transporter_rotation[1]) * np.sin(transporter_rotation[0]), 
                 np.sin(transporter_rotation[2]) * np.sin(transporter_rotation[1]) * np.sin(transporter_rotation[0]) + np.cos(transporter_rotation[2]) * np.cos(transporter_rotation[0]), 
                 np.cos(transporter_rotation[2]) * np.sin(transporter_rotation[1]) * np.sin(transporter_rotation[0]) - np.sin(transporter_rotation[2]) * np.cos(transporter_rotation[0])],
                [-np.sin(transporter_rotation[1]), 
                 np.sin(transporter_rotation[2]) * np.cos(transporter_rotation[1]), 
                 np.cos(transporter_rotation[2]) * np.cos(transporter_rotation[1])]
            ], dtype=np.float32)
            camera_offset = rotation_matrix @ offset

            if self.view_mode == 1:  # 3rd person view
                # self.camera.position = transporter_position + camera_offset
                self.camera.lookAt = forward_direction
                self.camera.position = transporter_position - 10 * forward_direction + np.array([0, 0, 5], dtype=np.float32)
            else: # 1st person view
                # Position camera at transporter position
                self.camera.lookAt = forward_direction
                # Look in the direction the transporter is facing
                self.camera.position = transporter_position + forward_direction * 5 # + np.array([0, 0, 5], dtype=np.float32)
            ############################################################################
    
    def DrawScene(self):
        if self.screen == 1: 
            # print("Drawing scene")
            ######################################################
            # Example draw statements

            
            for i, shader in enumerate(self.shaders):
               self.camera.Update(shader)
            self.camera.Update(self.edge_shader)
            # self.camera.Update(self.hud_shader)

            # self.gameState["cube"].Draw()
            # self.gameState["test"].Draw()
            self.gameState["transporter"].Draw()
            # self.gameState["transporter"].DrawEdges(self.edge_shader, self.camera.viewMatrix, self.camera.projectionMatrix)
            # print("Transporter drawn")
            # self.gameState["stars"].Draw()
            # self.gameState["arrow"].Draw()

            # if self.gameState["transporter"].properties["view"] == 2: # Conditionally draw crosshair
            #     self.gameState["crosshair"].Draw()

            # for laser in self.gameState["lasers"]:
            #     laser.Draw()
            for planet in self.gameState["planets"]:
                planet.Draw()
                # planet.DrawEdges(self.edge_shader, self.camera.viewMatrix, self.camera.projectionMatrix)
            # print("Planets drawn")
            for spaceStation in self.gameState["spaceStations"]:
                spaceStation.Draw()
                # spaceStation.DrawEdges(self.edge_shader, self.camera.viewMatrix, self.camera.projectionMatrix)
            # print("Spacestations drawn")
            for pirate in self.gameState["pirates"]:
                pirate.Draw()
                # pirate.DrawEdges(self.edge_shader, self.camera.viewMatrix, self.camera.projectionMatrix)
            # print("Pirates drawn")

            # Draw lasers
            for laser in self.gameState['lasers']:
                laser.Draw()
                # print(f"Laser drawn at position: {laser.properties['position']}")
            ######################################################

            # Draw arrow in screen space using HUD shader
            self.gameState["arrow"].shader.Use()
            glUseProgram(self.gameState["arrow"].shader.ID)

            # Set HUD shader uniforms
            screenPosLoc = glGetUniformLocation(self.gameState["arrow"].shader.ID, "screenPosition".encode('utf-8'))
            rotationLoc = glGetUniformLocation(self.gameState["arrow"].shader.ID, "rotation".encode('utf-8'))
            colorLoc = glGetUniformLocation(self.gameState["arrow"].shader.ID, "color".encode('utf-8'))
            
            # Position in bottom-right corner
            glUniform2f(screenPosLoc, 0.8, -0.8)
            glUniform1f(rotationLoc, self.gameState["arrow"].properties['rotation'][2])
            glUniform3f(colorLoc, 
                    self.gameState["arrow"].properties['colour'][0],
                    self.gameState["arrow"].properties['colour'][1],
                    self.gameState["arrow"].properties['colour'][2])
            
            # Draw the arrow
            self.gameState["arrow"].vao.Use()
            self.gameState["arrow"].ibo.Use()
            glDrawElements(GL_TRIANGLES, self.gameState["arrow"].ibo.count, GL_UNSIGNED_INT, None)

            # Draw crosshair in 1st person view
            if self.view_mode == 2:
                self.gameState["crosshair"].shader.Use()
                glUseProgram(self.gameState["crosshair"].shader.ID)
                    
                # Set HUD shader uniforms
                screenPosLoc = glGetUniformLocation(self.gameState["crosshair"].shader.ID, "screenPosition".encode('utf-8'))   
                rotationLoc = glGetUniformLocation(self.gameState["crosshair"].shader.ID, "rotation".encode('utf-8'))
                colorLoc = glGetUniformLocation(self.gameState["crosshair"].shader.ID, "color".encode('utf-8'))
                    
                # Position in center of screen
                glUniform2f(screenPosLoc, 0.0, 0.0)
                glUniform1f(rotationLoc, 0.0)
                glUniform3f(colorLoc, 1.0, 1.0, 1.0)  # White crosshair
                    
                # Draw the crosshair
                self.gameState["crosshair"].vao.Use()
                self.gameState["crosshair"].ibo.Use()
                glDrawElements(GL_TRIANGLES, self.gameState["crosshair"].ibo.count, GL_UNSIGNED_INT, None)