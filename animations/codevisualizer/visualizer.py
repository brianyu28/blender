"""
CodeVisualizer
Blender script to generate slides
"""

from util import *

ORIGIN_X = 0
ORIGIN_Y = 0
WIDTH = 1920
HEIGHT = 1080

BOXES_X = WIDTH / 2
PADDING = 50

BELOW_BASELINE = 20 # pixels below baseline to draw

pencil = get_pencil("Stroke")
layer = pencil.layers.get("Lines")
layer.clear()

font = get_font("/Users/brian/Library/Fonts/Consolas.ttf")

highlight_mat = create_or_get_material("Highlight",
    pencil=pencil,
    fill=(224, 235, 157),
    stroke=False
)
highlight_mat_index = pencil.materials.find(highlight_mat.name)

class Action():

    ASSIGN = "assign"

    def __init__(self, action, *args):
        self.action = action
        self.args = list(args)

class Var():
    """Class for representing a variable."""
    def __init__(self, name, size=1, location="", show_always=False):
        self.name = name
        self.size = size
        self.location = location
        self.show_always = show_always

def draw_code(lines, size=None):
    texts = []

    # Ignore if no lines
    if not lines:
        return

    # Determine scale by using longest line
    if size is None:
        length = len(max(lines, key=len).replace("\t", "...."))
        longest = "|" * max(length, 22)
        tmp_size = 60
        tmp_longest = add_text("tmp_longest", longest, font=font, size=tmp_size)
        bpy.context.view_layer.update()
        goal_size = to_units(ORIGIN_X + BOXES_X - PADDING * 2)
        scale = tmp_longest.scale[0] * goal_size / (tmp_longest.dimensions[0])
        size = tmp_size * scale / tmp_longest.scale[0] # font size
        set_text_size(tmp_longest, size)
        bpy.context.view_layer.update()
        line_height = from_units(tmp_longest.dimensions[1]) + 10
        char_width = from_units(tmp_longest.dimensions[0]) / len(longest)
        bpy.data.objects.remove(tmp_longest)

    print(line_height)
    total_height = len(lines) * line_height
    print(total_height)
    start_height = HEIGHT - ((HEIGHT - total_height) / 2)

    for i, line in enumerate(lines):
        text = add_text(f"Line{i + 1}", line, font=font, size=size)
        text.location = pt(PADDING, start_height - line_height * (i + 1))
        text["codevisualizer"] = {
            "indentation": char_width * (len(line) - len(line.strip())),
            "width": char_width * len(line.lstrip())
        }
        if text["codevisualizer"]["indentation"] > 0:
            text["codevisualizer"]["indentation"] += 7
        texts.append(text)

    bpy.context.view_layer.update()
    return texts

def draw_frame(frame, code, variables, line=None):
    pass

def draw(config, code, actions):
    frame_no = 1
    texts = draw_code(code)
    for i, (text, line) in enumerate(zip(texts, code)):
        line_no = i + 1

        # Skip empty slides
        if not len(line.strip()) and not actions.get(line_no):
            continue

        # Generate slide
        frame = get_frame(layer, frame_no)
        origin = from_pt(text.location)
        rect = draw_rect(frame,
            origin=(origin[0] + text["codevisualizer"]["indentation"], origin[1] - BELOW_BASELINE),
            width=(text["codevisualizer"]["width"]),
            height=from_units(text.dimensions[1]) + BELOW_BASELINE
        )
        rect.material_index = highlight_mat_index
        frame_no += 1

def read_file(filename):
    return open(filename).read().strip().splitlines()

def sample():
    x = Var("x")
    y = Var("y")
    config = [
        [x, y]
    ]

    actions = {
        5: [Action(Action.ASSIGN, x, 2)],
    }

    lines = read_file("/Users/brian/Development/blender/animations/codevisualizer/test2.c")
    draw(config, lines, actions)


def main():
    sample()

if __name__ == "__main__":
    main()
