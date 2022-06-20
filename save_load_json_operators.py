from asyncore import read
import bpy
import json
import os
import pathlib

from bpy.app.handlers import persistent

from .addons_prefs import get_addon_preferences


# check if serializable
def isSerializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset

def dataset_from_properties(datasetin, avoid_list=()):
    datasetout = {}
    for p in datasetin.bl_rna.properties:
        if p.identifier not in avoid_list:
            if not p.is_readonly:
                if isSerializable(getattr(datasetin, p.identifier)):
                    datasetout[p.identifier] = getattr(datasetin, p.identifier)
    return datasetout

def set_properties_from_dataset(datasetin, dataset, avoid_list=()):
    for prop in datasetin:
        if prop not in avoid_list:
            try:
                setattr(dataset, '%s' % prop, datasetin[prop])
            except (KeyError, AttributeError, TypeError):
                pass

def return_action_dataset(action):
    datasetout=dataset_from_properties(action)
    datasetout["commands"]=[]
    for c in action.commands:
        json_command=dataset_from_properties(c)
        datasetout["commands"].append(json_command)
    return datasetout

def return_action_filename(name, index):
    return "action%s_%s.json" % (str(index).zfill(3), name)

def create_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

def empty_directory(directory, include_pattern=None):
    for file in os.listdir(directory):
        if include_pattern is not None:
            if include_pattern in file:
                os.remove(os.path.join(directory, file))
        else:
            os.remove(os.path.join(directory, file))

def return_files_with_pattern(directory, pattern):
    list=[]
    for filename in os.listdir(directory):
        if pattern in filename:
            list.append(os.path.join(directory, filename))
    return list

@persistent
def reload_startup(scene):
    actions = bpy.data.window_managers[0].tableth_properties.actions
    save_folder = get_addon_preferences().save_folder
    # Create folder if needed
    if not os.path.isdir(save_folder):
        print("Tablet Helper - No Action to load")
        return

    # Clear existings
    actions.clear()

    # Load new
    action_files=return_files_with_pattern(save_folder, "action")
    if action_files:
        for f in action_files:
            dataset=read_json(f)
            new_action=actions.add()
            set_properties_from_dataset(dataset, new_action)
            for c in dataset["commands"]:
                new_command=new_action.commands.add()
                set_properties_from_dataset(c, new_command)


class TABLETH_OT_save_actions(bpy.types.Operator):
    bl_idname = "tableth.save_actions"
    bl_label = "Save Actions"

    @classmethod
    def poll(cls, context):
        props = context.window_manager.tableth_properties
        return props.actions

    def execute(self, context):
        props = context.window_manager.tableth_properties
        actions = props.actions

        save_folder = get_addon_preferences().save_folder
        # Create folder if needed
        if not os.path.isdir(save_folder):
            pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)
        # Empty dir
        else:
            empty_directory(save_folder, "action")

        idx=0
        for a in actions:
            json_datas=return_action_dataset(a)
            file_name=return_action_filename(a.name, idx)
            path = os.path.join(save_folder, file_name)
            create_json_file(json_datas, path)
            idx+=1
        
        self.report({'INFO'}, "Actions Saved")

        return {'FINISHED'}


class TABLETH_OT_load_actions(bpy.types.Operator):
    bl_idname = "tableth.load_actions"
    bl_label = "Load Actions"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = context.window_manager.tableth_properties
        actions = props.actions

        save_folder = get_addon_preferences().save_folder
        # Create folder if needed
        if not os.path.isdir(save_folder):
            self.report({'INFO'}, "No Action to load")
            return {'FINISHED'}

        # Clear existings
        actions.clear()

        # Load new
        action_files=return_files_with_pattern(save_folder, "action")
        if action_files:
            for f in action_files:
                dataset=read_json(f)
                new_action=actions.add()
                set_properties_from_dataset(dataset, new_action)
                for c in dataset["commands"]:
                    new_command=new_action.commands.add()
                    set_properties_from_dataset(c, new_command)
        
            self.report({'INFO'}, "Actions Loaded")
        else:
            self.report({'INFO'}, "No Action to load")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(TABLETH_OT_save_actions)
    bpy.utils.register_class(TABLETH_OT_load_actions)
    bpy.app.handlers.load_post.append(reload_startup)

def unregister():
    bpy.utils.unregister_class(TABLETH_OT_save_actions)
    bpy.utils.unregister_class(TABLETH_OT_load_actions)
    bpy.app.handlers.load_post.remove(reload_startup)