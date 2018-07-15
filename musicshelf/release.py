from flask import Blueprint, flash, g, redirect, render_template, request, url_for, Markup
from werkzeug.exceptions import abort
import markdown, re

from musicshelf.user import login_required
from musicshelf.db import get_db

bp = Blueprint('release', __name__, url_prefix='/release')

@bp.route('/new/<int:mid>', methods=('GET', 'POST'))
@login_required
def new(mid):
    """
    Add release to master with top_id=mid.
    """
    #QUESTION what happens if mid isn't given?
    # set up the mysql connection
    cursor = get_db().cursor()

    if request.method == 'POST':
        error = None
        # gather variables
        top_id = int(request.form['top_id'])
        cat_no = request.form['cat_no']
        label = request.form['label']
        ryear = int(request.form['ryear'])
        rcover_designer = request.form['rcover_designer']
        discogs_rid = request.form['discogs_rid']
        mtype = request.form['mtype']
        # assemble stype based on mtype
        if mtype == "vinyl":
            stype = request.form['num']+request.form['diameter']+', '+request.form['speed']
        elif mtype == "tape":
            stype = request.form['num']+request.form['tapetype']
        elif mtype == "optical":
            stype = request.form['num']+request.form['opticaltype']
        else:
            error = "Invalid item type: " + mtype
        notes = request.form['notes']

        if error is None:
            ret = cursor.execute(
                'INSERT INTO msrelease'
                ' (top_id, cat_no, label, ryear, rcover_designer, discogs_rid, mtype, stype, notes)'
                ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (top_id, cat_no, label, ryear, rcover_designer, discogs_rid, mtype, stype, notes)
            )
            return redirect(url_for('master.masterdetail', id=top_id))
        flash(error)

    # load the pre-existing master data
    cursor.execute(
        'SELECT *'
        ' FROM msmaster WHERE top_id=%s',
        (mid)
    )
    master = cursor.fetchone()
    return render_template('release/new.html', master=master)

@bp.route('/edit/<int:rid>', methods=('GET', 'POST'))
@login_required
def edit(rid):
    """
    Edit an existing release entry.
    """
    # get what data we have to send to the form
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * FROM msrelease WHERE rid=%s',
        (rid)
    )
    release = cursor.fetchone()
    # TODO: process the values that go to radio buttons
    return render_template('release/edit.html', release=release)


@bp.route('/delete/<int:rid>', methods=('GET', 'POST'))
@login_required
def delete(rid):
    return "STUB: Deleting release "+str(rid)

@bp.route('/<int:rid>')
def detail(rid):
    """
    Show release details.
    """
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT * FROM msrelease WHERE rid=%s',
        (rid)
    )
    release = cursor.fetchone()
    return render_template('release/detail.html', release=release)
