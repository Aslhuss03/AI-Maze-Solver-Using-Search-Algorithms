import tkinter as tk
import random
import heapq
from collections import deque

CELL_SIZE = 40
GRID_ROWS = 10
GRID_COLS = 10
WALL_PROB = 0.25  # 25% chance of wall

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Maze Game")
        self.canvas = tk.Canvas(root, width=GRID_COLS*CELL_SIZE, height=GRID_ROWS*CELL_SIZE, bg="white")
        self.canvas.pack()

        # Maze variables
        self.grid = []
        self.start = (0, 0)
        self.goal = (GRID_ROWS-1, GRID_COLS-1)
        self.path = []

        # Modes and flags
        self.edit_mode = False
        self.running = False
        self.paused = False
        self.goal_locked = False  # new flag to lock goal after start

        # Bind click
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        # Row 0: Path / Maze / Edit / Restart buttons
        tk.Button(control_frame, text="Find Path", command=self.start_pathfinding).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Regenerate Maze", command=self.generate_random_maze).grid(row=0, column=1, padx=5)
        self.edit_button = tk.Button(control_frame, text="Add/Remove Obstacles", command=self.toggle_edit_mode)
        self.edit_button.grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Restart", command=self.restart).grid(row=0, column=3, padx=5)

        # Row 1: Speed slider + Pause button
        tk.Label(control_frame, text="Speed:").grid(row=1, column=0, padx=5)
        self.speed_scale = tk.Scale(control_frame, from_=1, to=100, orient="horizontal", length=150)
        self.speed_scale.set(50)
        self.speed_scale.grid(row=1, column=1, padx=5)
        self.pause_button = tk.Button(control_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=1, column=2, padx=5)

        # Row 2: Algorithm selection
        tk.Label(control_frame, text="Algorithm:").grid(row=2, column=0, padx=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("A*")
        tk.OptionMenu(control_frame, self.algorithm_var, "A*", "BFS", "DFS").grid(row=2, column=1, padx=5)
        self.algorithm_var.trace_add("write", self.on_algorithm_change)

        self.generate_random_maze()

    # ---------------- Maze ----------------
    def generate_random_maze(self):
        self.running = False
        self.paused = False
        self.goal_locked = False
        self.grid = [['#' if random.random() < WALL_PROB else '.' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.start = (0,0)
        self.goal = (GRID_ROWS-1, GRID_COLS-1)
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'
        self.path = []
        self.draw_grid()

    def clear_path_marks(self):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if self.grid[r][c] in ['+', '*']:
                    self.grid[r][c] = '.'
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.goal[0]][self.goal[1]] = 'G'

    def restart(self):
        self.running = False
        self.paused = False
        self.goal_locked = False
        self.clear_path_marks()
        self.path = []
        self.draw_grid()

    def toggle_edit_mode(self):
        self.running = False
        self.paused = False
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.edit_button.config(relief="sunken", text="Editing Obstacles")
        else:
            self.edit_button.config(relief="raised", text="Add/Remove Obstacles")

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            algo = self.algorithm_var.get()
            if algo == "A*":
                self.step_astar()
            elif algo == "BFS":
                self.step_bfs()
            elif algo == "DFS":
                self.step_dfs()

    def on_canvas_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if row<0 or row>=GRID_ROWS or col<0 or col>=GRID_COLS:
            return
        if self.edit_mode:
            self.running = False
            self.paused = False
            if (row,col) != self.start and (row,col) != self.goal:
                self.grid[row][col] = '#' if self.grid[row][col]=='.' else '.'
        else:
            if not self.goal_locked:
                if self.grid[row][col] != '#' and (row,col)!=self.start:
                    self.grid[self.goal[0]][self.goal[1]] = '.'
                    self.goal = (row,col)
                    self.grid[row][col]='G'
        self.draw_grid()

    def draw_grid(self, highlight=None):
        self.canvas.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
                cell = self.grid[r][c]
                color = "white"
                if cell=='#': color='black'
                elif cell=='S': color='green'
                elif cell=='G': color='red'
                elif cell=='*': color='yellow'
                elif cell=='+': color='lightblue'
                if highlight and (r,c)==highlight: color='orange'
                self.canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline='gray')
                if cell=='S' or cell=='G':
                    self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2, text=cell, font=("Arial", 16, "bold"))
        self.root.update_idletasks()

    def heuristic(self,a,b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_delay(self):
        speed = self.speed_scale.get()
        return max(1, 200 - speed*2)

    # ---------------- Pathfinding ----------------
    def start_pathfinding(self):
        if self.running: return
        self.running = True
        self.paused = False
        self.goal_locked = True  # lock goal as soon as pathfinding starts
        algo = self.algorithm_var.get()
        self.visited = set()
        self.came_from = {}
        self.open_set = None
        self.stack_queue = None

        if algo=="A*":
            self.open_set = []
            heapq.heappush(self.open_set, (0, self.start))
            self.g_score = {self.start:0}
            self.f_score = {self.start:self.heuristic(self.start,self.goal)}
            self.step_astar()
        elif algo=="BFS":
            self.stack_queue = deque([self.start])
            self.visited.add(self.start)
            self.step_bfs()
        elif algo=="DFS":
            self.stack_queue = [self.start]
            self.visited.add(self.start)
            self.step_dfs()

    def step_astar(self):
        if not self.running or self.paused: return
        if not self.open_set:
            self.show_message("No path found!")
            self.running=False
            return
        _, current = heapq.heappop(self.open_set)
        if current in self.visited:
            self.root.after(self.get_delay(), self.step_astar)
            return
        self.visited.add(current)
        if current not in [self.start, self.goal]: self.grid[current[0]][current[1]]='+'
        self.draw_grid(current)
        if current==self.goal:
            self.reconstruct_path()
            return
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor=(current[0]+dx,current[1]+dy)
            if 0<=neighbor[0]<GRID_ROWS and 0<=neighbor[1]<GRID_COLS:
                if self.grid[neighbor[0]][neighbor[1]]=='#': continue
                tentative_g=self.g_score[current]+1
                if tentative_g < self.g_score.get(neighbor,float('inf')):
                    self.came_from[neighbor]=current
                    self.g_score[neighbor]=tentative_g
                    self.f_score[neighbor]=tentative_g+self.heuristic(neighbor,self.goal)
                    heapq.heappush(self.open_set,(self.f_score[neighbor],neighbor))
        self.root.after(self.get_delay(), self.step_astar)

    def step_bfs(self):
        if not self.running or self.paused: return
        if not self.stack_queue:
            self.show_message("No path found!")
            self.running=False
            return
        current=self.stack_queue.popleft()
        if current not in [self.start,self.goal]: self.grid[current[0]][current[1]]='+'
        self.draw_grid(current)
        if current==self.goal:
            self.reconstruct_path()
            return
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor=(current[0]+dx,current[1]+dy)
            if 0<=neighbor[0]<GRID_ROWS and 0<=neighbor[1]<GRID_COLS:
                if self.grid[neighbor[0]][neighbor[1]]=='#': continue
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.came_from[neighbor]=current
                    self.stack_queue.append(neighbor)
        self.root.after(self.get_delay(), self.step_bfs)

    def step_dfs(self):
        if not self.running or self.paused: return
        if not self.stack_queue:
            self.show_message("No path found!")
            self.running=False
            return
        current=self.stack_queue.pop()
        if current not in [self.start,self.goal]: self.grid[current[0]][current[1]]='+'
        self.draw_grid(current)
        if current==self.goal:
            self.reconstruct_path()
            return
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor=(current[0]+dx,current[1]+dy)
            if 0<=neighbor[0]<GRID_ROWS and 0<=neighbor[1]<GRID_COLS:
                if self.grid[neighbor[0]][neighbor[1]]=='#': continue
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.came_from[neighbor]=current
                    self.stack_queue.append(neighbor)
        self.root.after(self.get_delay(), self.step_dfs)

    # ---- Path Reconstruction ----
    def reconstruct_path(self):
        node=self.goal
        path=[]
        while node in self.came_from:
            path.append(node)
            node=self.came_from[node]
        path.append(self.start)
        path.reverse()
        for r,c in path:
            if self.grid[r][c] not in ['S','G']:
                self.grid[r][c]='*'
            self.draw_grid((r,c))
        self.running=False
        self.show_message(f"Path found! Length: {len(path)}")

    # ---- Algorithm change callback ----
    def on_algorithm_change(self, *args):
        self.running = False
        self.paused = False
        self.goal_locked = False
        self.clear_path_marks()
        self.path = []
        self.draw_grid()
        self.start_pathfinding()

    # ---- Message Popup ----
    def show_message(self,text):
        popup=tk.Toplevel()
        popup.title("Message")
        tk.Label(popup,text=text,padx=20,pady=10).pack()
        tk.Button(popup,text="OK",command=popup.destroy).pack(pady=5)

if __name__=="__main__":
    root=tk.Tk()
    game=MazeGame(root)
    root.mainloop()