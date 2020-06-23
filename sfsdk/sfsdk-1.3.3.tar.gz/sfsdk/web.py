# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, jsonify, render_template
from sfsdk import exrsettings, log, stacksettings, kbsettings, frameworksettings
import random
import uuid
import shutil
import os

get_remote_technologies_func = None
get_remote_technology_func = None
get_remote_vulnerabilities_func = None
get_remote_vulnerability_func = None
get_remote_frameworks_func = None

ctoken = ''.join([ str(random.randint(0, 9)) for _ in range(19) ])

class FlaskWithDifferentDelimeters(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = FlaskWithDifferentDelimeters(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path): 
    return send_from_directory('static', path)

@app.route("/handler", methods = [ "POST" ])
def handler():

    req_data = request.get_json()
    
    action = req_data.get('action')
    if not action:
        return jsonify({'error': 'action required'})

    if action == 'getUserCToken':
        return jsonify({ 'ctoken': ctoken })

    # Anti-csrf token
    token = req_data.get('ctoken')
    if token != ctoken:
        return jsonify({ 'result': 'error', 'msg': 'Missing or wrong ctoken' })

    if action == 'getExercises':
        # Add local names
        return jsonify(
            [
                {**{ 'localName': n }, **e } for n, e in exrsettings.get_exercises(raw=True).items() 
            ]
        )
    elif action == 'getExerciseDetails':
        # Add local names
        req_uuid = req_data.get('uuid') 
        exercise_data = exrsettings.get_exercise_by_uuid(req_uuid)
        exercise_local_name = exrsettings.get_standard_name(exercise_data)
        exercise_data['localName'] = exercise_local_name
        return jsonify(exercise_data)
    elif action == 'addExercise':
        del req_data['ctoken']
        del req_data['action']

        req_data['uuid'] = f'sfsdk-{str(uuid.uuid4())}'

        exrsettings.save_exercise_meta(req_data)

        return jsonify({
            'result': 'success',
            'uuid': req_data['uuid']
        })
    elif action == 'updateExercise':
        req_uuid = req_data.get('uuid') 

        # Make sure uuid exists already
        old_exercise_data = exrsettings.get_exercise_by_uuid(req_uuid)
        if not old_exercise_data:
            return jsonify({
                'result': 'error',
                'uuid': 'unknown uuid'
            })

        del req_data['ctoken']
        del req_data['action']

        old_exercise_dir = os.path.join(
            exrsettings.workspace_dir,
            exrsettings.get_standard_name(old_exercise_data)
        )

        exrsettings.update_exercise_folder(old_exercise_dir, req_data)

        return jsonify({
            'result': 'success',
            'uuid': req_data['uuid']
        })
    elif action == "addTechnology":

        req_data['obj']['uuid'] = f'sfsdk-{str(uuid.uuid4())}'

        stack_folder = stacksettings.save_stack_meta(req_data['obj'])

        print(f"Saved to {stack_folder}")
        
        return jsonify({
            'result': 'success'
        })
    elif action == "updateTechnology":

        req_uuid = req_data["obj"].get('uuid') 

        # Make sure uuid exists already
        old_stack_data = stacksettings.get_stack_by_uuid(req_uuid)
        if not old_stack_data:
            return jsonify({
                'result': 'error',
                'uuid': 'unknown uuid'
            })

        old_stack_dir = os.path.join(
            stacksettings.workspace_dir,
            stacksettings.get_standard_stack_name(old_stack_data)
        )

        stacksettings.update_stack_folder(old_stack_dir, req_data["obj"])

        return jsonify({
            'result': 'success',
            'uuid': req_uuid
        })
    elif action == "deleteTechnology":
    
        req_uuid = req_data.get('uuid')

        stacksettings.delete_stack_by_uuid(req_uuid)

        return jsonify({
            'result': 'success'
        })

    elif action == "addVulnerability":
    
        req_data['obj']['uuid'] = f'sfsdk-{str(uuid.uuid4())}'

        kb_folder = kbsettings.save_kb_meta(req_data['obj'])

        print(f"Saved to {kb_folder}")

        return jsonify({
            'result': 'success'
        })
    elif action == "updateVulnerability":

        req_uuid = req_data["obj"].get('uuid') 

        # Make sure uuid exists already
        old_kb_data = kbsettings.get_kb_by_uuid(req_uuid)
        if not old_kb_data:
            return jsonify({
                'result': 'error',
                'uuid': 'unknown uuid'
            })

        old_kb_dir = os.path.join(
            kbsettings.workspace_dir,
            kbsettings.get_standard_kb_name(old_kb_data)
        )

        kbsettings.update_kb_folder(old_kb_dir, req_data["obj"])

        return jsonify({
            'result': 'success',
            'uuid': req_uuid
        })
    elif action == "deleteVulnerability":
        
        req_uuid = req_data.get('uuid')

        kbsettings.delete_kb_by_uuid(req_uuid)

        return jsonify({
            'result': 'success'
        })

    elif action in ("addFramework", "updateFramework"):
        frameworksettings.save_framework(req_data['name'])
        return jsonify({"result": "success"})
    elif action == 'removeFramework':
        frameworksettings.delete_framework_by_name(req_data['name'])
        return jsonify({"result": "success"})
    elif action == 'getAllKbs':
        local_kbs = [ k for k in kbsettings.get_kbs().values() ]
        return jsonify(get_remote_vulnerabilities_func() + local_kbs)
    elif action == 'getFrameworks':
        local_frameworks = frameworksettings.get_frameworks()
        return jsonify(get_remote_frameworks_func() + local_frameworks)
    elif action == 'getKBItem':
        kb_item = {}

        if req_data['uuid'] in [ k['uuid'] for k in kbsettings.get_kbs().values() ]:
            kb_item = kbsettings.get_kb_by_uuid(req_data['uuid'])

        elif req_data['uuid'] in [ k['uuid'] for k in get_remote_vulnerabilities_func() ]:
            kb_item = get_remote_vulnerability_func(req_data['uuid'])

        return jsonify(kb_item)
    elif action == 'getAllStacks':
        local_stacks = [ s for s in stacksettings.get_stacks().values() ]
        return jsonify(get_remote_technologies_func() + local_stacks)
    elif action == 'getStackItem':

        stack_item = {}

        if req_data['uuid'] in [ k['uuid'] for k in stacksettings.get_stacks().values() ]:
            stack_item = stacksettings.get_stack_by_uuid(req_data['uuid'])
            
        elif req_data['uuid'] in [ k['uuid'] for k in get_remote_technologies_func() ]:
            stack_item = get_remote_technology_func(req_data['uuid'])

        return jsonify(stack_item)

    else:
        return jsonify({ 'result': 'error', 'message': 'unknown action'})

def run_editor():

    app.run(host= '127.0.0.1')
