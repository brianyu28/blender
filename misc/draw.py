import bpy

def pt(x, y, x_offset=4.32, y_offset=2.43, scale=0.0045):
    """
    Translates a point into space, given offsets and scale amount.
    """
    return (x * scale - x_offset, 0, y * scale - y_offset)

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

def draw_line(frame, p0, p1):
    stroke = frame.strokes.new()
    stroke.display_mode = "3DSPACE"
    stroke.points.add(count=2)
    stroke.points[0].co = p0
    stroke.points[1].co = p1
    return stroke

def draw_rect(frame, origin, width, height):
    x, y = origin
    stroke = frame.strokes.new()
    stroke.display_mode = "3DSPACE"
    stroke.points.add(count=5)
    stroke.points[0].co = pt(x, y)
    stroke.points[1].co = pt(x + width, y)
    stroke.points[2].co = pt(x + width, y + height)
    stroke.points[3].co = pt(x, y + height)
    stroke.points[4].co = pt(x, y)

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
