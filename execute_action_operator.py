import bpy


class TABLETH_execute_action(bpy.types.Operator):
    bl_idname = "tableth.execute_action"
    bl_label = "Execute Command"

    index : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        action=context.scene.tableth_actions[self.index]
        commands=action.commands

        for c in commands:
            exec(c.command)

        self.report({'INFO'}, "%s Executed" % action.name)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_execute_action)

def unregister():
    bpy.utils.unregister_class(TABLETH_execute_action)