import bpy
import math

def toggle_object_visibility(obj, frame, show, children=True):
    if isinstance(obj, str):
        obj = bpy.data.objects.get(obj)
    obj.hide_viewport = show
    obj.hide_render = show
    obj.keyframe_insert("hide_viewport", frame=frame - 1)
    obj.keyframe_insert("hide_render", frame=frame - 1)
    obj.hide_viewport = not show
    obj.hide_render = not show
    obj.keyframe_insert("hide_viewport", frame=frame)
    obj.keyframe_insert("hide_render", frame=frame)
    if children:
        for child in obj.children:
            toggle_object_visibility(child, frame, show)

def show_at(obj, frame, children=True):
    toggle_object_visibility(obj, frame, True, children=children)

def hide_at(obj, frame, children=True):
    toggle_object_visibility(obj, frame, False, children=children)

def create_object_from_template(template_name, name=None, collection=None, scale=None):
    template_obj = bpy.data.objects.get(template_name)
    obj = template_obj.copy()
    obj.data = template_obj.data.copy()
    coll = resolve_coll(collection)
    coll.objects.link(obj)
    if name is not None:
        obj.name = name
        obj.data.name = obj.name
    for template_child in template_obj.children:
        child = template_child.copy()
        child.data = template_child.data.copy()
        child.parent = obj
        coll.objects.link(child)
    if scale is not None:
        obj.scale = (scale, scale, scale)
    return obj

def resolve_object(obj):
    if isinstance(obj, str):
        return bpy.data.objects[obj]
    return obj

def resolve_coll(coll):
    if coll is None:
        return bpy.context.scene.collection
    elif isinstance(coll, str):
        return bpy.data.collections[coll]
    else:
        return coll

def selected():
    return list(bpy.context.selected_objects)
