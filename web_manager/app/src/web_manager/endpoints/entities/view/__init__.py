import dataclasses

from flask import render_template

from data_lib import model

from web_manager import app, repo


@app.route('/entities/<entity_code>/view/page/<int:page_num>', methods=['GET'])
def entity_view_page(entity_code: str, page_num: int):

    entity_type = getattr(model, entity_code)

    return render_template(
        'entity_view_page.html',
        entity_code=entity_code,
        data_keys=[attr.name for attr in dataclasses.fields(entity_type)],
        data_rows=list(map(dataclasses.asdict, repo.manager.select_any(getattr(model, entity_code), {})))
    )
