import bpy


class TABLETH_OT_manage_commands(bpy.types.Operator):
    bl_idname = "tableth.manage_commands"
    bl_label = "Manage Commands"

    action : bpy.props.EnumProperty(items=(
        ('UP', 'Up', ""),
        ('DOWN', 'Down', ""),
        ('ADD', 'Add', ""),
        ('REMOVE', 'Remove', ""),
        ))

    def execute(self, context):
        props = context.window_manager.tableth_properties
        active_action = props.actions[props.action_index]
        commands = active_action.commands

        if self.action=="ADD":
            commands.add()
            active_action.command_index=len(commands)-1

        elif self.action=="REMOVE":
            if active_action.command_index<=len(commands)-1:
                commands.remove(active_action.command_index)
                if active_action.command_index>len(commands)-1:
                    active_action.command_index-=1
                elif len(commands)==0:
                    active_action.command_index=-1

        elif self.action in {"UP", "DOWN"}:
            if self.action=="UP":
                target = active_action.command_index-1
            else:
                target = active_action.command_index+1
            if target!=-1 and target<len(commands):
                commands.move(active_action.command_index, target)
                active_action.command_index=target

        return{'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_OT_manage_commands)

def unregister():
    bpy.utils.unregister_class(TABLETH_OT_manage_commands)