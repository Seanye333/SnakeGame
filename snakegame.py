#!/usr/bin/env python3
"""
Snake Game
A classic snake game with graphical interface.
Use arrow keys to control the snake!
"""

import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        # Game settings
        self.grid_size = 20
        self.cell_size = 25
        self.game_width = self.grid_size * self.cell_size
        self.game_height = self.grid_size * self.cell_size
        self.speed = 150  # milliseconds between moves
        
        # Game state
        self.snake = [(10, 10), (10, 11), (10, 12)]  # Start with 3 segments
        self.direction = 'Up'
        self.next_direction = 'Up'
        self.food = self.spawn_food()
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.game_over = False
        
        # Create UI
        self.create_widgets()
        
        # Bind keys
        self.root.bind('<Up>', lambda e: self.change_direction('Up'))
        self.root.bind('<Down>', lambda e: self.change_direction('Down'))
        self.root.bind('<Left>', lambda e: self.change_direction('Left'))
        self.root.bind('<Right>', lambda e: self.change_direction('Right'))
        self.root.bind('<space>', lambda e: self.toggle_pause())
        
    def create_widgets(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x')
        
        title = tk.Label(title_frame, text="🐍 SNAKE GAME 🐍", 
                        font=('Arial', 24, 'bold'), 
                        bg='#2c3e50', fg='#2ecc71')
        title.pack(pady=10)
        
        # Score frame
        score_frame = tk.Frame(self.root, bg='#34495e')
        score_frame.pack(fill='x')
        
        self.score_label = tk.Label(score_frame, 
                                    text=f"Score: {self.score}  |  High Score: {self.high_score}", 
                                    font=('Arial', 14, 'bold'),
                                    bg='#34495e', fg='white')
        self.score_label.pack(pady=5)
        
        # Game canvas
        self.canvas = tk.Canvas(self.root, 
                               width=self.game_width, 
                               height=self.game_height,
                               bg='#1a1a1a',
                               highlightthickness=0)
        self.canvas.pack()
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#ecf0f1')
        control_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(control_frame, text='Start Game', 
                                   font=('Arial', 12, 'bold'),
                                   bg='#2ecc71', fg='white',
                                   padx=20, pady=10,
                                   command=self.start_game)
        self.start_btn.pack(side='left', padx=10)
        
        self.pause_btn = tk.Button(control_frame, text='Pause', 
                                   font=('Arial', 12, 'bold'),
                                   bg='#f39c12', fg='white',
                                   padx=20, pady=10,
                                   state='disabled',
                                   command=self.toggle_pause)
        self.pause_btn.pack(side='left', padx=10)
        
        reset_btn = tk.Button(control_frame, text='Reset', 
                             font=('Arial', 12, 'bold'),
                             bg='#e74c3c', fg='white',
                             padx=20, pady=10,
                             command=self.reset_game)
        reset_btn.pack(side='left', padx=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Use Arrow Keys to move  |  SPACE to pause", 
                               font=('Arial', 10),
                               bg='#ecf0f1', fg='#7f8c8d')
        instructions.pack(pady=5)
        
        # Draw initial state
        self.draw_game()
        
    def spawn_food(self):
        """Generate food at a random empty position."""
        while True:
            food = (random.randint(0, self.grid_size - 1), 
                   random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        """Change snake direction, preventing 180-degree turns."""
        opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_direction != opposites.get(self.direction):
            self.next_direction = new_direction
    
    def move_snake(self):
        """Move the snake one step in the current direction."""
        if not self.game_running or self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)
        
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake):
            self.game_over = True
            self.game_running = False
            self.show_game_over()
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.food = self.spawn_food()
            
            # Speed up slightly
            if self.speed > 50:
                self.speed -= 2
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        # Draw and schedule next move
        self.draw_game()
        self.root.after(self.speed, self.move_snake)
    
    def draw_game(self):
        """Draw the snake and food on the canvas."""
        self.canvas.delete('all')
        
        # Draw grid (optional, for visual effect)
        for i in range(self.grid_size + 1):
            # Vertical lines
            self.canvas.create_line(i * self.cell_size, 0, 
                                   i * self.cell_size, self.game_height,
                                   fill='#2d2d2d', width=1)
            # Horizontal lines
            self.canvas.create_line(0, i * self.cell_size, 
                                   self.game_width, i * self.cell_size,
                                   fill='#2d2d2d', width=1)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            # Head is brighter
            if i == 0:
                color = '#2ecc71'
                outline = '#27ae60'
            else:
                color = '#45b566'
                outline = '#27ae60'
            
            self.canvas.create_rectangle(
                x * self.cell_size + 2, y * self.cell_size + 2,
                (x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
                fill=color, outline=outline, width=2
            )
        
        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(
            fx * self.cell_size + 4, fy * self.cell_size + 4,
            (fx + 1) * self.cell_size - 4, (fy + 1) * self.cell_size - 4,
            fill='#e74c3c', outline='#c0392b', width=2
        )
        
        # Draw eyes on snake head
        head_x, head_y = self.snake[0]
        eye_offset = 8
        eye_size = 3
        
        if self.direction == 'Up':
            eye1_x, eye1_y = head_x * self.cell_size + eye_offset, head_y * self.cell_size + 8
            eye2_x, eye2_y = head_x * self.cell_size + self.cell_size - eye_offset, head_y * self.cell_size + 8
        elif self.direction == 'Down':
            eye1_x, eye1_y = head_x * self.cell_size + eye_offset, (head_y + 1) * self.cell_size - 8
            eye2_x, eye2_y = head_x * self.cell_size + self.cell_size - eye_offset, (head_y + 1) * self.cell_size - 8
        elif self.direction == 'Left':
            eye1_x, eye1_y = head_x * self.cell_size + 8, head_y * self.cell_size + eye_offset
            eye2_x, eye2_y = head_x * self.cell_size + 8, head_y * self.cell_size + self.cell_size - eye_offset
        else:  # Right
            eye1_x, eye1_y = (head_x + 1) * self.cell_size - 8, head_y * self.cell_size + eye_offset
            eye2_x, eye2_y = (head_x + 1) * self.cell_size - 8, head_y * self.cell_size + self.cell_size - eye_offset
        
        self.canvas.create_oval(eye1_x - eye_size, eye1_y - eye_size,
                               eye1_x + eye_size, eye1_y + eye_size,
                               fill='white', outline='black')
        self.canvas.create_oval(eye2_x - eye_size, eye2_y - eye_size,
                               eye2_x + eye_size, eye2_y + eye_size,
                               fill='white', outline='black')
    
    def start_game(self):
        """Start the game."""
        if not self.game_running:
            self.game_running = True
            self.game_over = False
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            self.move_snake()
    
    def toggle_pause(self):
        """Pause or resume the game."""
        if self.game_over:
            return
        
        self.game_running = not self.game_running
        
        if self.game_running:
            self.pause_btn.config(text='Pause')
            self.move_snake()
        else:
            self.pause_btn.config(text='Resume')
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.direction = 'Up'
        self.next_direction = 'Up'
        self.food = self.spawn_food()
        self.score = 0
        self.speed = 150
        self.game_running = False
        self.game_over = False
        
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text='Pause')
        self.update_score()
        self.draw_game()
    
    def update_score(self):
        """Update the score display."""
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.score_label.config(
            text=f"Score: {self.score}  |  High Score: {self.high_score}"
        )
    
    def show_game_over(self):
        """Show game over message."""
        self.draw_game()
        
        # Draw game over text on canvas
        self.canvas.create_text(
            self.game_width // 2, self.game_height // 2 - 30,
            text="GAME OVER!", 
            font=('Arial', 36, 'bold'),
            fill='#e74c3c'
        )
        self.canvas.create_text(
            self.game_width // 2, self.game_height // 2 + 20,
            text=f"Final Score: {self.score}", 
            font=('Arial', 20),
            fill='white'
        )
        
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
        
        # Show popup
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")

def main():
    root = tk.Tk()
    
    # Center the window on screen
    window_width = 520
    window_height = 680
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()