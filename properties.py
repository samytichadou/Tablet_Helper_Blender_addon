import bpy

class TABLETH_PR_commands(bpy.types.PropertyGroup):
    command: bpy.props.StringProperty(name='Command', default="new command")

class TABLETH_PR_action_collection(bpy.types.PropertyGroup):
    commands: bpy.props.CollectionProperty(type=TABLETH_PR_commands, name='Commands')
    description: bpy.props.StringProperty(name="Description")
    context: bpy.props.StringProperty(name="Context")
    icon: bpy.props.StringProperty(name="Icon")
    command_index : bpy.props.IntProperty(min=-1, default=-1)


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PR_commands)
    bpy.utils.register_class(TABLETH_PR_action_collection)
    bpy.types.Scene.tableth_actions = \
        bpy.props.CollectionProperty(type=TABLETH_PR_action_collection, name="Tablet Helper Commands")
    bpy.types.Scene.tableth_action_index = bpy.props.IntProperty(min=-1, default=-1)
    bpy.types.Scene.tableth_recording = bpy.props.IntProperty(min=-1, default=-1)

def unregister():
    bpy.utils.unregister_class(TABLETH_PR_commands)
    bpy.utils.unregister_class(TABLETH_PR_action_collection)
    del bpy.types.Scene.tableth_actions
    del bpy.types.Scene.tableth_action_index
    del bpy.types.Scene.tableth_recording