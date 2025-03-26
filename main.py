from OpenGL.GL import *
from utils.window_manager import Window
from game import Game
import imgui

class App:
    def __init__(self):
        self.window = Window()
        self.game = Game(self.window.windowHeight, self.window.windowWidth, self.window.impl)
        self.show_main_menu = True
        self.show_game_over = False
        self.show_you_won = False

    def RenderLoop(self):
        while self.window.IsOpen():
            inputs, time = self.window.StartFrame(0.0, 0.0, 0.0, 1.0)
            
            # Check if game changed to game over or win state
            if self.game.screen == 3 and not self.show_game_over:
                self.show_game_over = True
            elif self.game.screen == 2 and not self.show_you_won:
                self.show_you_won = True
            
            if self.show_main_menu:
                self.DrawMainMenu()
            elif self.show_game_over:
                self.DrawGameOverScreen()
            elif self.show_you_won:
                self.DrawYouWonScreen()
            else:
                self.game.ProcessFrame(inputs, time)
            
            self.window.EndFrame()
        
        self.window.Close()

    def DrawMainMenu(self):
        window_w, window_h = 400, 200  # Set the window size
        x_pos = (self.window.windowWidth - window_w) / 2
        y_pos = (self.window.windowHeight - window_h) / 2

        imgui.new_frame()
        # Centered window
        imgui.set_next_window_position(x_pos, y_pos)
        imgui.set_next_window_size(window_w, window_h)
        imgui.begin("Main Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        # Center text horizontally
        imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 1: New Game")[0]) / 2)
        if imgui.button("New Game", width=200, height=50):
            self.show_main_menu = False
            self.game.screen = 1
            self.game.InitScene()

        imgui.end()

        imgui.render()
        self.window.impl.render(imgui.get_draw_data())

    def DrawGameOverScreen(self):
        window_w, window_h = 400, 250  # Set the window size
        x_pos = (self.window.windowWidth - window_w) / 2
        y_pos = (self.window.windowHeight - window_h) / 2

        imgui.new_frame()
        # Centered window
        imgui.set_next_window_position(x_pos, y_pos)
        imgui.set_next_window_size(window_w, window_h)
        imgui.begin("Game Over", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        # Game Over text
        game_over_text = "GAME OVER"
        text_width = imgui.calc_text_size(game_over_text)[0]
        imgui.set_cursor_pos_x((window_w - text_width) / 2)
        imgui.text_colored(game_over_text, 1.0, 0.0, 0.0, 1.0)
        
        imgui.dummy(0, 20)  # Add some spacing
        
        # Buttons
        button_width = 200
        imgui.set_cursor_pos_x((window_w - button_width) / 2)
        if imgui.button("Return to Main Menu", width=button_width, height=40):
            self.show_main_menu = True
            self.show_game_over = False
            self.game.screen = 0  # Set back to main menu
            
        imgui.set_cursor_pos_x((window_w - button_width) / 2)
        if imgui.button("Exit Game", width=button_width, height=40):
            self.window.shouldClose = True  # This will close the window and end the game
            
        imgui.end()

        imgui.render()
        self.window.impl.render(imgui.get_draw_data())

    def DrawYouWonScreen(self):
        window_w, window_h = 400, 250  # Set the window size
        x_pos = (self.window.windowWidth - window_w) / 2
        y_pos = (self.window.windowHeight - window_h) / 2

        imgui.new_frame()
        # Centered window
        imgui.set_next_window_position(x_pos, y_pos)
        imgui.set_next_window_size(window_w, window_h)
        imgui.begin("You Won!", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        # Victory text
        victory_text = "MISSION ACCOMPLISHED!"
        text_width = imgui.calc_text_size(victory_text)[0]
        imgui.set_cursor_pos_x((window_w - text_width) / 2)
        imgui.text_colored(victory_text, 0.0, 1.0, 0.0, 1.0)
        
        imgui.dummy(0, 10)  # Add some spacing
        
        congrats_text = "Congratulations! You reached the destination!"
        text_width = imgui.calc_text_size(congrats_text)[0]
        imgui.set_cursor_pos_x((window_w - text_width) / 2)
        imgui.text(congrats_text)
        
        imgui.dummy(0, 20)  # Add some spacing
        
        # Buttons
        button_width = 200
        imgui.set_cursor_pos_x((window_w - button_width) / 2)
        if imgui.button("Return to Main Menu", width=button_width, height=40):
            self.show_main_menu = True
            self.show_you_won = False
            self.game.screen = 0  # Set back to main menu
            
        imgui.set_cursor_pos_x((window_w - button_width) / 2)
        if imgui.button("Exit Game", width=button_width, height=40):
            self.window.shouldClose = True  # This will close the window and end the game
            
        imgui.end()

        imgui.render()
        self.window.impl.render(imgui.get_draw_data())

if __name__ == "__main__":
    app = App()
    app.RenderLoop()