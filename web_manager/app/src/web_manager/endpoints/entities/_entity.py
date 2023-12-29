from data_lib import model

from web_manager import app, repo


@app.route('/entities/<entity_code>/<entity_identity>', methods=['DELETE'])
def entity_by_id(entity_code, entity_identity):

    entity_type = getattr(model, entity_code)

    repo.manager.delete(entity_type, id=entity_identity)

    return "Success", 200
