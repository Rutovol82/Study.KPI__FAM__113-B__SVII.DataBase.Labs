from .entities import *
from .stats import *

from web_manager import app


@app.route('/', methods=['GET'])
def welcome():
    return render_template('base.html')
