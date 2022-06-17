import bpy


class TABLETH_UL_action_slots(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text=item.name)

class TABLETH_UL_command_slots(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text=item.command)


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_UL_action_slots)
    bpy.utils.register_class(TABLETH_UL_command_slots)

def unregister():
    bpy.utils.unregister_class(TABLETH_UL_action_slots)
    bpy.utils.unregister_class(TABLETH_UL_command_slots)