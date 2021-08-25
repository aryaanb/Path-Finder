import tkinter as tk
from tkinter import *
import os
import threading
import pynput
from pynput.keyboard import Key, Controller
from time import sleep


WIDTH = 600
root = tk.Tk()
root.title("Path Finder")
canvas = tk.Canvas(root, height=610, width=800)
canvas.pack(side=LEFT)
embed = tk.Frame(canvas, width=WIDTH, height=WIDTH)
embed.place(relx=0.01, rely=0.01)  
keyboard = Controller()
blank = tk.PhotoImage()


os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

import pygame
import astar
import dfs
import bfs
import dfsrecursive
import ucs
import dijkstra
import greedy


pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))
running = False

def run_astar(fps):
    global running
    if running:
        stop()
    label.configure(text="Running A*")
    running = True
    _, result = astar.main(screen, WIDTH, fps)
    label.configure(text=f"Running A* \n Cost: {result}")
    running = False


def run_ucs(fps):
    global running
    if running:
        stop()
    label.configure(text="Running UCS")
    running = True
    _, result = ucs.main(screen, WIDTH, fps)
    label.configure(text=f"Running UCS \n Cost: {result}")
    running = False


def run_greedy(fps):
    global running
    if running:
        stop()
    label.configure(text="Running Greedy")
    running = True
    _, result = greedy.main(screen, WIDTH, fps)
    label.configure(text=f"Running Greedy \n Cost: {result}")
    running = False


def run_dijkstra(fps):
    global running
    if running:
        stop()
    label.configure(text="Running Dijkstra")
    running = True
    _, result = dijkstra.main(screen, WIDTH, fps)
    label.configure(text=f"Running Dijkstra's \n Cost: {result}")
    running = False


def run_dfsrec(fps):
    global running
    if running:
        stop()
    label.configure(text="Running Recursive DFS")
    running = True
    _, result = dfsrecursive.main(screen, WIDTH, fps)
    label.configure(text=f"Running Recursive DFS \n Cost: {result}")
    running = False

def run_dfs(fps):
    global running
    if running:
        stop()
    running = True
    label.configure(text="Running DFS")
    _, result = dfs.main(screen, WIDTH, fps)
    label.configure(text=f"Running DFS \n Cost: {result}")
    running = False

def run_bfs(fps):
    global running
    if running:
        stop()
    running = True
    label.configure(text="Running BFS")
    _, result = bfs.main(screen, WIDTH, fps)
    label.configure(text=f"Running BFS \n Cost: {result}")
    running = False

def run_program():
    keyboard.press(Key.space)
    sleep(0.1)
    keyboard.release(Key.space)

def clear():
    keyboard.press("r")
    sleep(0.1)
    keyboard.release("r")
    
def helper():
    keyboard.press("x")
    sleep(0.1)
    keyboard.release("x")

def stop():
    global running
    if running:
        running = False
        keyboard.press(Key.esc)
        sleep(0.1)
        keyboard.release(Key.esc)
        label.configure(text="Stopped")


def kill_program():
    root.destroy()
    pygame.quit()


a = tk.Button(canvas, text="A *", width=130, height=20, padx=3, pady=3, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_astar, args=(entry.get(),)).start())
d = tk.Button(canvas, text="DFS", width=130, height=20, padx=3, pady=3, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_dfs, args=(entry.get(),)).start())
dfsrec = tk.Button(canvas, text="DFS Recursive", width=130, height=20, padx=3, pady=3, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_dfsrec, args=(entry.get(),)).start())
b = tk.Button(canvas, text="BFS", width=130, height=20, padx=3, pady=1, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_bfs, args=(entry.get(),)).start())
u = tk.Button(canvas, text="UCS", width=130, height=20, padx=3, pady=1, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_ucs, args=(entry.get(),)).start())
dij = tk.Button(canvas, text="Dijkstra", width=130, height=20, padx=3, pady=1, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=lambda: threading.Thread(target=run_dijkstra, args=(entry.get(),)).start())
g = tk.Button(canvas, text="Greedy", width=130, height=20, padx=3, pady=1, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
                compound=tk.CENTER, command=lambda: threading.Thread(target=run_greedy, args=(entry.get(),)).start())
run_button = tk.Button(canvas, text="Run", bg="#00FF40", width=130, height=20, padx=3, pady=3, relief=RIDGE,
                       image=blank, font=("Helvetica", 10, "bold"), compound=tk.CENTER, command=run_program)
clear_button = tk.Button(canvas, text="Clear", width=130, height=20, padx=3, pady=3, bg="#DBDBDB", relief=RIDGE, image=blank, font=("Helvetica", 10, "bold"),
              compound=tk.CENTER, command=clear)
s = tk.Button(canvas, text="Stop", width=130, height=20, padx=3, pady=3, bg="#DBDBDB", relief=RIDGE,
              image=blank, font=("Helvetica", 10, "bold"), compound=tk.CENTER, command=stop)
kill = tk.Button(canvas, text="Quit", bg="#FC8080", width=130, height=20, padx=3, pady=3, relief=RIDGE,
                 image=blank, font=("Helvetica", 10, "bold"), compound=tk.CENTER, command=kill_program)

# entry = tk.Spinbox(canvas, values=(30, 60, 90, 120, 240),
#                    width=19, relief=RIDGE, font=("Helvetica", 10, "bold"), state="readonly", justify=tk.CENTER)
entry = tk.Scale(canvas, bg="#DBDBDB", font=("Helvetica", 10, "bold"), orient=HORIZONTAL, from_=5, to=240, resolution=5, relief=RIDGE, label="FPS", variable=IntVar())

label_frame = tk.LabelFrame(
    canvas, width=143, height=185, padx=3, pady=3, bg="#DBDBDB")
label_frame.place(relx=0.79, y=365)
label = tk.Message(label_frame, font=("Helvetica", 10, "bold"), width = 130)
label.place(relx=0, rely=0)
a.place(relx=0.79, y=35)
d.place(relx=0.79, y=70)
b.place(relx=0.79, y=105)
g.place(relx=0.79, y=140)
# u.place(relx=0.79, y=175)
dij.place(relx=0.79, y=175)
s.place(relx=0.79, y=280)
entry.place(relx=0.79, y=210, relheight=0.1, relwidth=0.18)
entry.set(240)
# clear_button.place(relx=0.79, y=280)
run_button.place(relx=0.79, y=315)
kill.place(relx=0.79, y=565)
root.protocol("WM_DELETE_WINDOW", kill_program)
root.resizable(0, 0)
root.mainloop()

