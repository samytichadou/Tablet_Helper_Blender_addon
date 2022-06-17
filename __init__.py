'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Tablet Helper",
    "description": "",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "",
    "wiki_url": "https://github.com/samytichadou/modifier_helper/blob/master/README.md",
    "tracker_url": "https://github.com/samytichadou/modifier_helper/issues/new",
    "category": "Interface" }


# IMPORT SPECIFICS
##################################

from . import   (
    addons_prefs,
    gui,
    properties,
    manage_actions_operators,
    execute_action_operator,
    ui_lists,
    manage_commands_operator,
)


# register
##################################

def register():
    addons_prefs.register()
    gui.register()
    properties.register()
    manage_actions_operators.register()
    execute_action_operator.register()
    ui_lists.register()
    manage_commands_operator.register()

def unregister():
    addons_prefs.unregister()
    gui.unregister()
    properties.unregister()
    manage_actions_operators.unregister()
    execute_action_operator.unregister()
    ui_lists.unregister()
    manage_commands_operator.unregister()