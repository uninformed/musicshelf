from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from musicshelf.user import login_required
from musicshelf.db import get_db

bp = Blueprint('master', __name__, url_prefix='/master')

@bp.route('/<int:id>')
def masterdetail(id):
    """
    Show master detail page.
    """
    cursor = get_db().cursor()
    # get master data
    cursor.execute(
        'SELECT * FROM msmaster M'
        ' WHERE top_id = ' + str(id)
    )
    master = cursor.fetchone()
    cursor.execute(
        'SELECT * FROM msrelease R'
        ' WHERE top_id='+str(id)
    )
    # get release data
    releases = cursor.fetchall()
    return render_template('master/masterdetail.html', master=master, releases=releases)
