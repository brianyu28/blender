import bpy

# Add GPencil stroke
pencil = bpy.data.grease_pencils.new("GPencilData")
pencil_obj = bpy.data.objects.new("GPencil", object_data=pencil)
bpy.context.view_layer.active_layer_collection.collection.objects.link(pencil_obj)

# Add layer
layer = pencil.layers.new("NewLayer", set_active=True)
frame = layer.frames.new(0)

# Draw line
stroke = frame.strokes.new()
stroke.display_mode = "3DSPACE"
stroke.points.add(count=2)
stroke.points[0].co = (-0.23, 0, -0.23)
stroke.points[1].co = (0.5, 0, 0.5)

