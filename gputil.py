import bpy
import math

UNIT_SCALE = 0.0045 # number of Blender units in a pixel

"""
Materials
"""

def rgb(r, g, b, alpha=1):
    """Converts colors on [0, 255] scale to [0, 1] scale."""
    return (r / 255, g / 255, b / 255, 1)

def create_material(name, pencil=None, color=None, fill=None, stroke=True):
    material = bpy.data.materials.new(name)
    bpy.data.materials.create_gpencil_data(material)
    if pencil is not None:
        pencil.materials.append(material)
    if color is not None:
        material.grease_pencil.color = rgb(*color)
    material.grease_pencil.show_stroke = stroke
    if fill is not None:
        material.grease_pencil.show_fill = True
        material.grease_pencil.fill_color = rgb(*fill)
    else:
        material.grease_pencil.show_fill = False
    return material

def create_or_get_material(name, **kwargs):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = create_material(name, **kwargs)
    return mat

def create_material_3d(name, color=(0, 0, 0)):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgb(*color)
    return mat

def create_or_get_material_3d(name, **kwargs):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = create_material_3d(name, **kwargs)
    return mat

"""
Drawing
"""

def pt(x, y, x_offset=4.32, y_offset=2.43, scale=UNIT_SCALE):
    """
    Translates a point into space, given offsets and scale amount.
    """
    return (x * scale - x_offset, 0, y * scale - y_offset)

def from_pt(point, x_offset=4.32, y_offset=2.43, scale=UNIT_SCALE):
    return ((point[0] + x_offset) / scale, (point[2] + y_offset) / scale)

def create_pencil(name="GPencil", data_name="GPencilData"):
    pencil = bpy.data.grease_pencils.new(data_name)
    pencil_obj = bpy.data.objects.new(name, object_data=pencil)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(pencil_obj)
    return pencil

def get_pencil(name):
    pencil = bpy.data.grease_pencils.get(name)
    return pencil

def get_frame(layer, n):
    try:
        frame = layer.frames.new(n)
        return frame
    except RuntimeError:
        for frame in layer.frames:
            if frame.frame_number == n:
                return frame
    return None

def draw_line(frame, p0, p1, line_width=5):
    stroke = frame.strokes.new()
    stroke.display_mode = "3DSPACE"
    stroke.points.add(count=2)
    stroke.points[0].co = p0
    stroke.points[1].co = p1
    stroke.line_width = line_width
    return stroke

def draw_rect(frame, origin, width, height, line_width=5):
    x, y = origin
    stroke = frame.strokes.new()
    stroke.display_mode = "3DSPACE"
    stroke.points.add(count=5)
    stroke.points[0].co = pt(x, y)
    stroke.points[1].co = pt(x + width, y)
    stroke.points[2].co = pt(x + width, y + height)
    stroke.points[3].co = pt(x, y + height)
    stroke.points[4].co = pt(x, y)
    stroke.line_width = 5
    return stroke

def draw_circle(frame, origin, radius, samples=100, line_width=5):
    x, y = origin
    stroke = frame.strokes.new()
    stroke.display_mode = "3DSPACE"
    stroke.points.add(count=samples)
    for i in range(samples):
        theta = (math.tau / (samples - 1)) * i
        stroke.points[i].co = pt(
            radius * math.cos(theta) + x,
            radius * math.sin(theta) + y
        )
    stroke.line_width = line_width
    return stroke

"""
Text
"""

def get_font(path):
    for font in bpy.data.fonts:
        if font.filepath == path:
            return font
    bpy.ops.font.open(filepath=path, relative_path=True)
    for font in bpy.data.fonts:
        if font.filepath == path:
            return font
    return None


def add_text(name, content, origin=(0, 0), color=(0, 0, 0), size=60, font=None, show_at=None):
    curve = bpy.data.curves.new(type="FONT",name=name)
    text = bpy.data.objects.new(name, curve)
    text.data.body = content
    bpy.context.collection.objects.link(text)
    text.rotation_euler[0] = math.tau / 4 # rotate to face front
    # Set up material
    mat = create_material_3d(f"{name}_mat", color=color)
    mat.blend_method = "BLEND"
    mat.use_nodes = True
    mat.show_transparent_back = False
    text.data.materials.append(mat)
    text.location = pt(*origin)
    set_text_size(text, size)
    if font is not None:
        text.data.font = font
    alpha = mat.node_tree.nodes["Principled BSDF"].inputs["Alpha"]
    if show_at is None:
        show_at = 1 # show starting from first frame
    elif show_at > 1:
        alpha.default_value = 0
        alpha.keyframe_insert("default_value", frame=1)
        alpha.default_value = 0
        alpha.keyframe_insert("default_value", frame=show_at - 1)
    alpha.default_value = 1
    alpha.keyframe_insert("default_value", frame=show_at)
    return text

def hide_text_at(text, hide_at):
    mat = text.data.materials[0]
    alpha = mat.node_tree.nodes["Principled BSDF"].inputs["Alpha"]
    alpha.default_value = 1
    alpha.keyframe_insert("default_value", frame=hide_at - 1)
    alpha.default_value = 0
    alpha.keyframe_insert("default_value", frame=hide_at)

def set_text_size(text, size):
    scale = 0.0066113763385348846 * size
    text.scale = (scale, scale, scale)

"""
3D Objects
"""

def to_units(pixels):
    return pixels * UNIT_SCALE

def from_units(units):
    return units / UNIT_SCALE

"""
Test code
"""

def test0():
    """test drawing a line"""
    # pencil = create_pencil()
    pencil = get_pencil("Stroke")
    layer = pencil.layers.new("NewLayer", set_active=True)
    frame = get_frame(layer, 1)
    draw_line(frame, pt(100, 100), pt(400, 400))

def test1():
    """test drawing rectangles over frames"""
    pencil = get_pencil("Stroke")
    layer = pencil.layers.get("Lines")
    x, y = 200, 200
    for i in range(30):
        frame = get_frame(layer, i + 1)
        draw_rect(frame, (200 + i * 30, 200), 500, 500)

def test2():
    """test drawing rectangles over frames"""
    pencil = get_pencil("Stroke")
    layer = pencil.layers.get("Lines")
    x, y = 200, 200
    for i in range(30):
        frame = get_frame(layer, i + 1)
        draw_rect(frame, (200 + i * 10, 200 + i * 10), 500, 500)
    for i in range(30):
        frame = get_frame(layer, i + 31)
        draw_rect(frame, (500 + i * 10, 500 - i * 10), 500, 500)

def test3():
    """Testing with fonts."""
    font = get_font("/Users/brian/Library/Fonts/Barlow-Regular.otf")
    text = add_text("Foo", "Hello!", origin=(400, 400), color=(255, 0, 0), size=80, font=font)
