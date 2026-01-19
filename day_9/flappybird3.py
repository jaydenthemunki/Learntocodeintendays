import tkinter as tk
import random
import math

class FlappyBird:
    def __init__(self):
        # Create window
        self.window = tk.Tk()
        self.window.title("🐦 Flappy Bird 🐦")
        self.window.resizable(False, False)
        self.window.configure(bg='#4ec0ca')
        
        # Game constants
        self.WIDTH = 500
        self.HEIGHT = 700
        self.GRAVITY = 0.6
        self.FLAP_STRENGTH = -11
        self.PIPE_SPEED = 4
        self.PIPE_GAP = 180
        self.PIPE_WIDTH = 70
        
        # Create canvas with gradient-like background
        self.canvas = tk.Canvas(
            self.window, 
            width=self.WIDTH, 
            height=self.HEIGHT, 
            bg='#87CEEB',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Draw background elements
        self.draw_background()
        
        # Game state
        self.bird_x = 100
        self.bird_y = self.HEIGHT // 2
        self.bird_vel = 0
        self.bird_radius = 18
        self.bird_angle = 0
        
        self.pipes = []
        self.score = 0
        self.high_score = 0
        self.frame_count = 0
        self.game_over = False
        self.game_started = False
        self.animation_offset = 0
        
        # Create first pipe
        self.add_pipe()
        
        # Draw bird with more detail
        self.create_bird()
        
        # Score display with shadow
        self.score_shadow = self.canvas.create_text(
            self.WIDTH // 2 + 3,
            53,
            text=str(self.score),
            font=('Arial', 56, 'bold'),
            fill='#333333'
        )
        self.score_text = self.canvas.create_text(
            self.WIDTH // 2,
            50,
            text=str(self.score),
            font=('Arial', 56, 'bold'),
            fill='white'
        )
        
        # High score display
        self.high_score_text = self.canvas.create_text(
            self.WIDTH // 2,
            100,
            text=f'Best: {self.high_score}',
            font=('Arial', 20, 'bold'),
            fill='#FFD700'
        )
        
        # Start message with background
        self.start_bg = self.canvas.create_rectangle(
            50, self.HEIGHT // 2 - 80,
            self.WIDTH - 50, self.HEIGHT // 2 + 20,
            fill='#2C3E50',
            outline='#ECF0F1',
            width=4
        )
        self.start_msg = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 40,
            text='🐦 FLAPPY BIRD 🐦',
            font=('Arial', 28, 'bold'),
            fill='#FFD700'
        )
        self.start_instruction = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 5,
            text='Click or Press SPACE to Fly!',
            font=('Arial', 18),
            fill='white'
        )
        
        # Bind controls
        self.canvas.bind_all('<space>', self.flap)
        self.canvas.bind_all('<Button-1>', self.flap)
        
        # Start game loop
        self.update()
        self.window.mainloop()
    
    def draw_background(self):
        # Sky gradient simulation with rectangles
        colors = ['#87CEEB', '#98D8E8', '#A9E2F3', '#BAF3FF']
        section_height = self.HEIGHT // len(colors)
        for i, color in enumerate(colors):
            self.canvas.create_rectangle(
                0, i * section_height,
                self.WIDTH, (i + 1) * section_height,
                fill=color, outline=''
            )
        
        # Draw clouds
        self.draw_cloud(80, 100, 50)
        self.draw_cloud(320, 150, 60)
        self.draw_cloud(180, 220, 45)
        self.draw_cloud(400, 80, 55)
        
        # Draw sun
        self.canvas.create_oval(
            self.WIDTH - 120, 40,
            self.WIDTH - 40, 120,
            fill='#FFD700',
            outline='#FFA500',
            width=3
        )
        
        # Ground/grass at bottom
        self.canvas.create_rectangle(
            0, self.HEIGHT - 100,
            self.WIDTH, self.HEIGHT,
            fill='#7CB342',
            outline=''
        )
        self.canvas.create_rectangle(
            0, self.HEIGHT - 100,
            self.WIDTH, self.HEIGHT - 95,
            fill='#558B2F',
            outline=''
        )
    
    def draw_cloud(self, x, y, size):
        # Draw fluffy cloud
        self.canvas.create_oval(
            x, y,
            x + size, y + size * 0.6,
            fill='white',
            outline='#E0E0E0',
            width=1
        )
        self.canvas.create_oval(
            x + size * 0.3, y - size * 0.2,
            x + size * 0.8, y + size * 0.5,
            fill='white',
            outline='#E0E0E0',
            width=1
        )
        self.canvas.create_oval(
            x + size * 0.5, y,
            x + size * 1.2, y + size * 0.6,
            fill='white',
            outline='#E0E0E0',
            width=1
        )
    
    def create_bird(self):
        # Bird body (main circle)
        self.bird_body = self.canvas.create_oval(
            self.bird_x - self.bird_radius,
            self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius,
            self.bird_y + self.bird_radius,
            fill='#FFD700',
            outline='#FFA500',
            width=3
        )
        
        # Bird belly (lighter shade)
        self.bird_belly = self.canvas.create_oval(
            self.bird_x - self.bird_radius // 2,
            self.bird_y - self.bird_radius // 3,
            self.bird_x + self.bird_radius // 2,
            self.bird_y + self.bird_radius // 2,
            fill='#FFEB3B',
            outline=''
        )
        
        # Wing
        self.bird_wing = self.canvas.create_oval(
            self.bird_x - 8,
            self.bird_y - 3,
            self.bird_x + 10,
            self.bird_y + 12,
            fill='#FFA500',
            outline='#FF8C00',
            width=2
        )
        
        # Eye white
        self.bird_eye_white = self.canvas.create_oval(
            self.bird_x + 3,
            self.bird_y - 8,
            self.bird_x + 13,
            self.bird_y + 2,
            fill='white',
            outline='black',
            width=2
        )
        
        # Eye pupil
        self.bird_eye = self.canvas.create_oval(
            self.bird_x + 7,
            self.bird_y - 5,
            self.bird_x + 11,
            self.bird_y - 1,
            fill='black'
        )
        
        # Beak
        beak_points = [
            self.bird_x + self.bird_radius,
            self.bird_y,
            self.bird_x + self.bird_radius + 12,
            self.bird_y - 5,
            self.bird_x + self.bird_radius + 12,
            self.bird_y + 5
        ]
        self.bird_beak = self.canvas.create_polygon(
            beak_points,
            fill='#FF6347',
            outline='#CC4125',
            width=2
        )
    
    def add_pipe(self):
        height = random.randint(120, self.HEIGHT - self.PIPE_GAP - 220)
        
        # Top pipe main body
        top_pipe = self.canvas.create_rectangle(
            self.WIDTH,
            0,
            self.WIDTH + self.PIPE_WIDTH,
            height,
            fill='#4CAF50',
            outline='#2E7D32',
            width=3
        )
        
        # Top pipe highlight (3D effect)
        top_highlight = self.canvas.create_rectangle(
            self.WIDTH + 5,
            5,
            self.WIDTH + 15,
            height - 35,
            fill='#66BB6A',
            outline=''
        )
        
        # Top pipe cap
        top_cap = self.canvas.create_rectangle(
            self.WIDTH - 8,
            height - 35,
            self.WIDTH + self.PIPE_WIDTH + 8,
            height,
            fill='#66BB6A',
            outline='#2E7D32',
            width=3
        )
        
        # Bottom pipe main body
        bottom_pipe = self.canvas.create_rectangle(
            self.WIDTH,
            height + self.PIPE_GAP,
            self.WIDTH + self.PIPE_WIDTH,
            self.HEIGHT - 100,
            fill='#4CAF50',
            outline='#2E7D32',
            width=3
        )
        
        # Bottom pipe highlight
        bottom_highlight = self.canvas.create_rectangle(
            self.WIDTH + 5,
            height + self.PIPE_GAP + 35,
            self.WIDTH + 15,
            self.HEIGHT - 105,
            fill='#66BB6A',
            outline=''
        )
        
        # Bottom pipe cap
        bottom_cap = self.canvas.create_rectangle(
            self.WIDTH - 8,
            height + self.PIPE_GAP,
            self.WIDTH + self.PIPE_WIDTH + 8,
            height + self.PIPE_GAP + 35,
            fill='#66BB6A',
            outline='#2E7D32',
            width=3
        )
        
        self.pipes.append({
            'top': top_pipe,
            'top_highlight': top_highlight,
            'top_cap': top_cap,
            'bottom': bottom_pipe,
            'bottom_highlight': bottom_highlight,
            'bottom_cap': bottom_cap,
            'x': self.WIDTH,
            'height': height,
            'passed': False
        })
    
    def flap(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.canvas.delete(self.start_msg)
            self.canvas.delete(self.start_bg)
            self.canvas.delete(self.start_instruction)
        
        if not self.game_over:
            self.bird_vel = self.FLAP_STRENGTH
        else:
            self.restart()
    
    def restart(self):
        # Reset bird
        self.bird_y = self.HEIGHT // 2
        self.bird_vel = 0
        self.bird_angle = 0
        self.update_bird_position()
        
        # Remove all pipes
        for pipe in self.pipes:
            self.canvas.delete(pipe['top'])
            self.canvas.delete(pipe['top_highlight'])
            self.canvas.delete(pipe['top_cap'])
            self.canvas.delete(pipe['bottom'])
            self.canvas.delete(pipe['bottom_highlight'])
            self.canvas.delete(pipe['bottom_cap'])
        self.pipes = []
        self.add_pipe()
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(self.high_score_text, text=f'Best: {self.high_score}')
        
        # Reset game state
        self.score = 0
        self.frame_count = 0
        self.game_over = False
        self.game_started = False
        
        # Update score
        self.canvas.itemconfig(self.score_text, text=str(self.score))
        self.canvas.itemconfig(self.score_shadow, text=str(self.score))
        
        # Remove game over message
        if hasattr(self, 'game_over_text'):
            self.canvas.delete(self.game_over_text)
            self.canvas.delete(self.game_over_bg)
            self.canvas.delete(self.final_score_text)
            self.canvas.delete(self.restart_text)
            self.canvas.delete(self.game_over_title)
        
        # Show start message
        self.start_bg = self.canvas.create_rectangle(
            50, self.HEIGHT // 2 - 80,
            self.WIDTH - 50, self.HEIGHT // 2 + 20,
            fill='#2C3E50',
            outline='#ECF0F1',
            width=4
        )
        self.start_msg = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 40,
            text='🐦 FLAPPY BIRD 🐦',
            font=('Arial', 28, 'bold'),
            fill='#FFD700'
        )
        self.start_instruction = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 5,
            text='Click or Press SPACE to Fly!',
            font=('Arial', 18),
            fill='white'
        )
    
    def check_collision(self, pipe):
        bird_left = self.bird_x - self.bird_radius
        bird_right = self.bird_x + self.bird_radius
        bird_top = self.bird_y - self.bird_radius
        bird_bottom = self.bird_y + self.bird_radius
        
        pipe_left = pipe['x']
        pipe_right = pipe['x'] + self.PIPE_WIDTH
        
        if bird_right > pipe_left and bird_left < pipe_right:
            if bird_top < pipe['height'] or bird_bottom > pipe['height'] + self.PIPE_GAP:
                return True
        return False
    
    def update_bird_position(self):
        # Update all bird parts
        self.canvas.coords(
            self.bird_body,
            self.bird_x - self.bird_radius,
            self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius,
            self.bird_y + self.bird_radius
        )
        self.canvas.coords(
            self.bird_belly,
            self.bird_x - self.bird_radius // 2,
            self.bird_y - self.bird_radius // 3,
            self.bird_x + self.bird_radius // 2,
            self.bird_y + self.bird_radius // 2
        )
        self.canvas.coords(
            self.bird_wing,
            self.bird_x - 8,
            self.bird_y - 3,
            self.bird_x + 10,
            self.bird_y + 12
        )
        self.canvas.coords(
            self.bird_eye_white,
            self.bird_x + 3,
            self.bird_y - 8,
            self.bird_x + 13,
            self.bird_y + 2
        )
        self.canvas.coords(
            self.bird_eye,
            self.bird_x + 7,
            self.bird_y - 5,
            self.bird_x + 11,
            self.bird_y - 1
        )
        
        # Update beak
        beak_points = [
            self.bird_x + self.bird_radius,
            self.bird_y,
            self.bird_x + self.bird_radius + 12,
            self.bird_y - 5,
            self.bird_x + self.bird_radius + 12,
            self.bird_y + 5
        ]
        self.canvas.coords(self.bird_beak, *beak_points)
    
    def update(self):
        if self.game_started and not self.game_over:
            # Update bird physics
            self.bird_vel += self.GRAVITY
            self.bird_y += self.bird_vel
            
            # Update bird position
            self.update_bird_position()
            
            # Animate wing flap
            self.animation_offset += 1
            wing_y_offset = math.sin(self.animation_offset * 0.3) * 3
            self.canvas.move(self.bird_wing, 0, wing_y_offset - (math.sin((self.animation_offset - 1) * 0.3) * 3))
            
            # Check ceiling and floor collision
            if self.bird_y - self.bird_radius <= 0 or self.bird_y + self.bird_radius >= self.HEIGHT - 100:
                self.end_game()
            
            # Update pipes
            self.frame_count += 1
            if self.frame_count % 85 == 0:
                self.add_pipe()
            
            for pipe in self.pipes[:]:
                # Move pipe
                pipe['x'] -= self.PIPE_SPEED
                self.canvas.move(pipe['top'], -self.PIPE_SPEED, 0)
                self.canvas.move(pipe['top_highlight'], -self.PIPE_SPEED, 0)
                self.canvas.move(pipe['top_cap'], -self.PIPE_SPEED, 0)
                self.canvas.move(pipe['bottom'], -self.PIPE_SPEED, 0)
                self.canvas.move(pipe['bottom_highlight'], -self.PIPE_SPEED, 0)
                self.canvas.move(pipe['bottom_cap'], -self.PIPE_SPEED, 0)
                
                # Check collision
                if self.check_collision(pipe):
                    self.end_game()
                
                # Update score
                if not pipe['passed'] and pipe['x'] + self.PIPE_WIDTH < self.bird_x:
                    pipe['passed'] = True
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=str(self.score))
                    self.canvas.itemconfig(self.score_shadow, text=str(self.score))
                
                # Remove off-screen pipes
                if pipe['x'] + self.PIPE_WIDTH < 0:
                    self.canvas.delete(pipe['top'])
                    self.canvas.delete(pipe['top_highlight'])
                    self.canvas.delete(pipe['top_cap'])
                    self.canvas.delete(pipe['bottom'])
                    self.canvas.delete(pipe['bottom_highlight'])
                    self.canvas.delete(pipe['bottom_cap'])
                    self.pipes.remove(pipe)
        
        # Continue game loop
        self.window.after(16, self.update)
    
    def end_game(self):
        self.game_over = True
        
        # Create game over overlay
        self.game_over_bg = self.canvas.create_rectangle(
            60, self.HEIGHT // 2 - 140,
            self.WIDTH - 60, self.HEIGHT // 2 + 120,
            fill='#34495E',
            outline='#ECF0F1',
            width=5
        )
        
        self.game_over_title = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 90,
            text='💀 GAME OVER 💀',
            font=('Arial', 38, 'bold'),
            fill='#E74C3C'
        )
        
        self.game_over_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 30,
            text=f'Score: {self.score}',
            font=('Arial', 32, 'bold'),
            fill='#FFD700'
        )
        
        self.final_score_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 20,
            text=f'Best: {max(self.score, self.high_score)}',
            font=('Arial', 26, 'bold'),
            fill='#3498DB'
        )
        
        self.restart_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 75,
            text='🔄 Click or Press SPACE to Restart',
            font=('Arial', 18, 'bold'),
            fill='#2ECC71'
        )

# Run the game
if __name__ == "__main__":
    game = FlappyBird()