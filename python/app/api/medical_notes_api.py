from app.api import application
from flask import request
from flask import jsonify
import logging
from ..resolvers.medical_notes_resolver import load_medical_note

LOG = logging.getLogger(__name__)


@application.route('/api/medical_notes/load', methods=['GET'])
def api_medical_notes_load():
    print("calling api/medical_notes/load")
    # TODO implemenet security after hackathon prototype
    mn_id = request.args.get('mn_id', None)
    if mn_id is None or len(mn_id) < 1:
        print("Bad request missing md_id")
        return {}, 400

    mn = load_medical_note(mn_id)

    return jsonify({'data': mn.as_dict()}), 200