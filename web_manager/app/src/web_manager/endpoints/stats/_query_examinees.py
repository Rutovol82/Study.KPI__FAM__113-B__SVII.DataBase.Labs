import dataclasses

from flask import render_template, url_for, request

from data_lib.model import ExamineeData, Sex
from web_manager import app, repo
from web_manager.forms.stats._examinees_query import ExamineesQueryForm


@app.route('/stats/query/examinees/filter', methods=['GET', 'POST'])
def query_examinees():

    data_keys = [attr.name for attr in dataclasses.fields(ExamineeData)]

    if request.method == 'GET':
        return render_template(
            'query_examinees.html',
            data_keys=data_keys,
            data_rows=[],
            query_form=ExamineesQueryForm(),
            query_action=url_for('query_examinees'),
            query_method='POST'
        ), 200

    else:
        form = ExamineesQueryForm(request.form)

        if form.validate():

            return render_template(
                'query_table.html',
                keys=data_keys,
                rows=repo.manager.select_any(ExamineeData, {'birth_year': form.data['birth_year'], 'sex': Sex.FEMALE if 'FEMALE' in form.data['sex'] else Sex.MALE})
            ), 200

        return render_template(
            'query_form.html',
            form=form,
            method='POST',
            action=url_for('query_examinees')
        ), 403
