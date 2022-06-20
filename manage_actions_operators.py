import bpy


class TABLETH_OT_manage_actions(bpy.types.Operator):
    bl_idname = "tableth.manage_actions"
    bl_label = "Create Command"

    action : bpy.props.EnumProperty(items=(
        ('UP', 'Up', ""),
        ('DOWN', 'Down', ""),
        ('ADD', 'Add', ""),
        ('REMOVE', 'Remove', ""),
        ))

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = context.window_manager.tableth_properties
        actions = props.actions

        if self.action=="ADD":
            new_action=actions.add()
            new_action.name="New Action"
            props.action_index=len(actions)-1

        elif self.action=="REMOVE":
            if props.action_index<=len(actions)-1:
                actions.remove(props.action_index)
                if props.action_index>len(actions)-1:
                    props.action_index-=1
                elif len(actions)==0:
                    props.action_index=-1

        elif self.action in {"UP", "DOWN"}:
            if self.action=="UP":
                target = props.action_index-1
            else:
                target = props.action_index+1
            if target!=-1 and target<len(actions):
                actions.move(props.action_index, target)
                props.action_index=target

        # redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_OT_manage_actions)

def unregister():
    bpy.utils.unregister_class(TABLETH_OT_manage_actions)