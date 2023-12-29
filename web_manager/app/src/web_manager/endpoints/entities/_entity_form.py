from flask import render_template, url_for, request
from flask_wtf import FlaskForm

from data_lib import model
from data_lib.repo_abc import RepoDataError, RepoArgumentError, RepoIntegrityError
from web_manager import app, repo

from web_manager import forms


@app.route('/entities/<entity_code>/<entity_identity>/form', methods=['GET', 'POST'])
def entity_by_id_form(entity_code: str, entity_identity):

    entity_type = getattr(model, entity_code)
    entity_form = getattr(forms, entity_code + 'Form')

    if request.method == "GET":
        form = entity_form(obj=repo.manager.select(entity_type, id=entity_identity))
        response_code = 200

    else:
        form = entity_form(request.form)

        if form.validate():
            try:
                repo.manager.update(entity_type, form.data)

            except (RepoDataError, RepoArgumentError, RepoIntegrityError):
                return 'Fail', 200

            return 'Success', 200

        response_code = 403

    return render_template(
        'entity_form.html',
        form=form,
        action=url_for('entity_by_id_form', entity_code=entity_code, entity_identity=entity_identity),
        method='POST'
    ), response_code


@app.route('/entities/<entity_code>/new/form', methods=['GET', 'POST'])
def entity_new_form(entity_code: str):

    entity_type = getattr(model, entity_code)
    entity_form = getattr(forms, entity_code + 'Form')

    if request.method == 'GET':

        form: FlaskForm = entity_form()
        response_code = 200

    else:

        form: FlaskForm = entity_form(request.form)

        if form.validate():
            try:
                repo.manager.insert(entity_type, form.data)

            except (RepoDataError, RepoArgumentError, RepoIntegrityError):
                return 'Fail', 200

            return 'Success', 200

        response_code = 403

    return render_template(
        'entity_form.html',
        form=form,
        action=url_for('entity_new_form', entity_code=entity_code),
        method='POST'
    ), response_code
