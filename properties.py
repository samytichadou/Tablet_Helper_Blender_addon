import bpy

class TABLETH_PR_commands(bpy.types.PropertyGroup):
    command: bpy.props.StringProperty(name='Command', default="new command")

class TABLETH_PR_action_collection(bpy.types.PropertyGroup):
    commands: bpy.props.CollectionProperty(type=TABLETH_PR_commands, name='Commands')
    description: bpy.props.StringProperty(name="Description")
    context_mode: bpy.props.StringProperty(name="Context Mode")
    context_workspace: bpy.props.StringProperty(name="Context Workspace")
    context_active_type: bpy.props.StringProperty(name="Context Active Type")
    context_location: bpy.props.EnumProperty(
        name='Context Location',
        items={
            ('ALL', 'All', 'Available in all locations', 1),
            ('SIDEBAR', 'Sidebar', 'Available in Sidebar Panel', 2),
            ('TOPBAR', 'Topbar', 'Available in Topbar Popover', 3),
            ('POPUP', 'Popup', 'Available in Popup Menu', 4),
            ('TOOL', 'Tool', 'Available in Tool Menu', 5),
            ('SPECIFIC', 'Specific', 'Available in custom locations', 6),
        },
        default='ALL',
    )
    context_specific_location: bpy.props.StringProperty(
        name="Context Specific Locations",
        description="Custom available locations comma separated\n\
        In : sidebar, topbar, popup, tool"
    )
    icon: bpy.props.StringProperty(name="Icon")
    command_index : bpy.props.IntProperty(min=-1, default=-1)

class TABLETH_PR_properties(bpy.types.PropertyGroup):
    action_index: bpy.props.IntProperty(name='Action Index', min=-1, default=-1)
    recording: bpy.props.IntProperty(name='Recording Action', min=-1, default=-1)

    actions: bpy.props.CollectionProperty(type=TABLETH_PR_action_collection, name="Tablet Helper Commands")


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_PR_commands)
    bpy.utils.register_class(TABLETH_PR_action_collection)
    bpy.utils.register_class(TABLETH_PR_properties)

    bpy.types.Scene.tableth_properties = \
        bpy.props.PointerProperty(type = TABLETH_PR_properties, name="Tableth Properties")

def unregister():
    bpy.utils.unregister_class(TABLETH_PR_commands)
    bpy.utils.unregister_class(TABLETH_PR_action_collection)
    bpy.utils.unregister_class(TABLETH_PR_properties)

    del bpy.types.Scene.tableth_properties