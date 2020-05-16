"""
Spinning nodes.
"""

from util import *
import math

X = 0
Y = 0
WIDTH = 1920
HEIGHT = 1080

LINE_WIDTH = 150
RADIUS = 120

CENTER = (960, 540)

pencil = get_pencil("Stroke")
layer = pencil.layers.get("Lines")

layer.clear()

mat_name = "Node"
node_mat_index = pencil.materials.find(mat_name)
if node_mat_index == -1:
    node_mat = create_material(
        "Node",
        pencil=pencil,
        color=(36, 62, 237),
        fill=(255, 255, 255)
    )
    node_mat_index = pencil.materials.find(node_mat.name)

def draw_at(p1, p2, frame):
    line = draw_line(frame, pt(*p1), pt(*p2), line_width=LINE_WIDTH)
    c1 = draw_circle(frame, p1, RADIUS, line_width=LINE_WIDTH)
    c2 = draw_circle(frame, p2, RADIUS, line_width=LINE_WIDTH)
    line.material_index = node_mat_index
    c1.material_index = node_mat_index
    c2.material_index = node_mat_index

def draw(radius, angle, frame):
    CENTER_X, CENTER_Y = CENTER
    p1 = (
        radius * math.cos(angle) + CENTER_X,
        radius * math.sin(angle) + CENTER_Y
    )
    p2 = (
        radius * math.cos(angle + math.pi) + CENTER_X,
        radius * math.sin(angle + math.pi) + CENTER_Y
    )
    draw_at(p1, p2, frame)

frame_counter = 1
cur_radius = 300
cur_angle = 0

# Animation 1: contraction
A1_FRAMES = 10
A1_SPEED = 15

for i, frame_no in enumerate(range(frame_counter, frame_counter + A1_FRAMES)):
    frame = get_frame(layer, frame_no)
    draw(cur_radius, cur_angle, frame)
    cur_radius -= A1_SPEED
frame_counter += A1_FRAMES

A2_FRAMES = 30
A2_SPEED = (math.tau / 2) / (A2_FRAMES - 1)
for i, frame_no in enumerate(range(frame_counter, frame_counter + A2_FRAMES)):
    frame = get_frame(layer, frame_no)
    draw(cur_radius, cur_angle, frame)
    cur_angle -= A2_SPEED
    if i < A2_FRAMES / 2:
        cur_radius += A1_SPEED
    else:
        cur_radius -= A1_SPEED
