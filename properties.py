import bpy

class TABLETH_PR_command_collection(bpy.types.PropertyGroup):
    command: bpy.props.StringProperty(name='Command')
    description: bpy.props.StringProperty(name="Description")
    context: bpy.props.StringProperty(name="Context")
    icon: bpy.props.StringProperty(name="Icon")


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PR_command_collection)
    bpy.types.Scene.tableth_commands = \
        bpy.props.CollectionProperty(type=TABLETH_PR_command_collection, name="Tablet Helper Commands")

def unregister():
    bpy.utils.unregister_class(TABLETH_PR_command_collection)
    del bpy.types.Scene.tableth_commands