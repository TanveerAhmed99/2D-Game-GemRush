import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys
import os
from math import cos, sin, pi

# Game Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60
FRAME_TIME = 1000 // FPS

# Game Physics
BASKET_SPEED = 12
GEM_BASE_SPEED = 4.5
GEM_SPEED_INCREASE = 0.8
GRAVITY = 0.2

# Colors
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
BLUE = (0.0, 0.8, 1.0)
ORANGE = (1.0, 0.5, 0.0)
BLACK = (0.0, 0.0, 0.0)

class GameState:
    def __init__(self):
        self.is_paused = False
        self.is_game_over = False
        self.move_left = False
        self.move_right = False

class Diamond:
    def __init__(self):
        self.reset()
        self.score = 0
        self.size = 20
        self.sparkle_timer = 0
        
    def reset(self):
        self.pos_x = random.randint(-220, 220)
        self.pos_y = 340
        self.velocity = 0
        self.color_rgb = self.generate_diamond_color()
        self.rotation = random.uniform(0, 360)
    
    def generate_diamond_color(self):
        # Generate realistic diamond colors (clear to slight blue tint)
        blue_tint = random.uniform(0.8, 1.0)
        return (1.0, 1.0, blue_tint)
    
    def update(self, game_state):
        if not game_state.is_paused and not game_state.is_game_over:
            self.velocity += GRAVITY
            self.pos_y -= GEM_BASE_SPEED + (self.score * GEM_SPEED_INCREASE) + self.velocity
            self.rotation += 2
            self.sparkle_timer = (self.sparkle_timer + 1) % 10
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos_x, self.pos_y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        
        # Main diamond shape
        glPointSize(2)
        glColor3f(*self.color_rgb)
        
        # Draw kite-shaped trapezium
        top = (0, self.size * 1.2) 
        right = (self.size * 0.8, 0)  
        bottom = (0, -self.size * 0.8)  
        left = (-self.size * 0.8, 0)  
        top_right = (self.size * 0.4, self.size * 0.6)  
        top_left = (-self.size * 0.4, self.size * 0.6) 
        
        # Draw the kite shape using triangles
        glBegin(GL_TRIANGLES)
        glVertex2f(*top)
        glVertex2f(*top_right)
        glVertex2f(*top_left)
        
        # Right triangle
        glVertex2f(*top_right)
        glVertex2f(*right)
        glVertex2f(*bottom)
        
        # Left triangle
        glVertex2f(*top_left)
        glVertex2f(*bottom)
        glVertex2f(*left)
        
        # Middle triangle
        glVertex2f(*top_left)
        glVertex2f(*top_right)
        glVertex2f(*bottom)
        glEnd()
        
        # Add facet lines for more diamond-like appearance
        glColor3f(1.0, 1.0, 1.0)  
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex2f(*top)
        glVertex2f(*bottom)
        glVertex2f(*left)
        glVertex2f(*right)
        glVertex2f(*top_left)
        glVertex2f(*top_right)
        glEnd()
        
        # Add sparkles at the facet intersections
        if self.sparkle_timer < 5:
            glPointSize(3)
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_POINTS)
            glVertex2f(*top)
            glVertex2f(*bottom)
            glVertex2f(0, 0) 
            glEnd()
        
        glPopMatrix()

class Basket:
    def __init__(self):
        self.pos_x = 0
        self.color_rgb = WHITE
        self.width = 140
        self.height = 40
        self.curve_segments = 16
    
    def update(self, game_state):
        if game_state.move_right and not game_state.is_paused:
            self.pos_x = min(180, self.pos_x + BASKET_SPEED)
        if game_state.move_left and not game_state.is_paused:
            self.pos_x = max(-180, self.pos_x - BASKET_SPEED)
    
    def draw(self):
        glColor3f(*self.color_rgb)
        
        # Draw basket with curved bottom
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(self.curve_segments + 1):
            t = i / self.curve_segments
            x = self.pos_x - self.width/2 + self.width * t
            y = -365 - self.height * sin(t * pi)
            glVertex2f(x, y)
            glVertex2f(x, -365)
        glEnd()
        
        # Draw basket edges
        glPointSize(3)
        glBegin(GL_LINES)
        glVertex2f(self.pos_x - self.width/2, -365)
        glVertex2f(self.pos_x + self.width/2, -365)
        glEnd()

class UI:
    @staticmethod
    def draw_restart_button():
        glPointSize(4)
        glColor3f(*BLUE)
        # Draw restart symbol
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            angle = i * (2 * pi / 32)
            x = -185 + 20 * cos(angle)
            y = 350 + 20 * sin(angle)
            glVertex2f(x, y)
        glEnd()
        # Draw arrow
        glBegin(GL_TRIANGLES)
        glVertex2f(-195, 350)
        glVertex2f(-175, 340)
        glVertex2f(-175, 360)
        glEnd()
    
    @staticmethod
    def draw_exit_button():
        glPointSize(3)
        glColor3f(*RED)
        glBegin(GL_LINES)
        glVertex2f(170, 335)
        glVertex2f(200, 365)
        glVertex2f(170, 365)
        glVertex2f(200, 335)
        glEnd()
    
    @staticmethod
    def draw_pause_button(is_paused):
        glPointSize(4)
        glColor3f(*ORANGE)
        if is_paused:
            glBegin(GL_TRIANGLES)
            glVertex2f(-15, 370)
            glVertex2f(15, 350)
            glVertex2f(-15, 330)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glVertex2f(-15, 370)
            glVertex2f(-5, 370)
            glVertex2f(-5, 330)
            glVertex2f(-15, 330)
            glVertex2f(5, 370)
            glVertex2f(15, 370)
            glVertex2f(15, 330)
            glVertex2f(5, 330)
            glEnd()

class Game:
    def __init__(self):
        self.state = GameState()
        self.diamond = Diamond()
        self.basket = Basket()
        self.ui = UI()
    
    def init_gl(self):
        glClearColor(*BLACK, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(104, (SCREEN_WIDTH / SCREEN_HEIGHT), 1, 1000.0)
    
    def check_collision(self):
        if (self.diamond.pos_y <= -365 and 
            self.basket.pos_x - self.basket.width/2 <= self.diamond.pos_x <= self.basket.pos_x + self.basket.width/2):
            self.diamond.reset()
            self.diamond.score += 1
            print("Score:", self.diamond.score)
            return True
        return False
    
    def check_game_over(self):
        if self.diamond.pos_y < -400:
            self.diamond.reset()
            self.basket.color_rgb = RED
            print("Game Over! Final Score:", self.diamond.score)
            self.diamond.score = 0
            self.state.is_paused = True
            self.state.is_game_over = True
    
    def convert_mouse_coords(self, x, y):
        return x - (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - y
    
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 314, 0, 0, 0, 0, 1, 0)
        
        # Draw game elements
        self.basket.draw()
        self.diamond.draw()
        
        # Draw UI elements
        self.ui.draw_restart_button()
        self.ui.draw_exit_button()
        self.ui.draw_pause_button(self.state.is_paused)
        
        glutSwapBuffers()
    
    def update(self):
        if not self.state.is_paused and not self.state.is_game_over:
            self.diamond.update(self.state)
            self.basket.update(self.state)
            if not self.check_collision():
                self.check_game_over()
    
    def handle_keyboard(self, key, x, y):
        if key == b' ':
            self.state.is_paused = not self.state.is_paused
        glutPostRedisplay()
    
    def handle_special_key(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            self.state.move_right = True
        if key == GLUT_KEY_LEFT:
            self.state.move_left = True
    
    def handle_special_key_up(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            self.state.move_right = False
        if key == GLUT_KEY_LEFT:
            self.state.move_left = False
    
    def handle_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            click_x, click_y = self.convert_mouse_coords(x, y)
            
            # Restart button
            if -209 < click_x < -170 and 325 < click_y < 375:
                print('Restarting Game')
                self.basket.color_rgb = WHITE
                self.diamond.reset()
                self.state.is_game_over = False
                self.state.is_paused = False
                self.diamond.score = 0
            
            # Exit button
            elif 170 < click_x < 216 and 330 < click_y < 370:
                print('Exiting Game. Final Score:', self.diamond.score)
                sys.stdout.flush()
                time.sleep(0.1)
                os._exit(0)
            
            # Pause button
            elif -25 < click_x < 25 and 325 < click_y < 375:
                self.state.is_paused = not self.state.is_paused
        
        glutPostRedisplay()
    
    def animate(self, value):
        self.update()
        glutPostRedisplay()
        glutTimerFunc(FRAME_TIME, self.animate, 0)

def main():
    game = Game()
    
    glutInit()
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"Diamond Catcher!")
    
    game.init_gl()
    
    glutDisplayFunc(game.display)
    glutTimerFunc(FRAME_TIME, game.animate, 0)
    glutKeyboardFunc(game.handle_keyboard)
    glutSpecialFunc(game.handle_special_key)
    glutMouseFunc(game.handle_mouse)
    glutSpecialUpFunc(game.handle_special_key_up)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
