import bpy


class TABLETH_execute_action(bpy.types.Operator):
    bl_idname = "tableth.execute_action"
    bl_label = "Execute Command"

    index : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        props = context.window_manager.tableth_properties
        actions = props.actions
        return actions

    def execute(self, context):
        action=context.window_manager.tableth_properties.actions[self.index]
        commands=action.commands

        for c in commands:
            try:
                exec(c.command)
            except SyntaxError:
                print("SyntaxError, Avoiding command - %s" % c)

        self.report({'INFO'}, "%s Executed" % action.name)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_execute_action)

def unregister():
    bpy.utils.unregister_class(TABLETH_execute_action)