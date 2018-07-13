from flask import Blueprint, flash, g, redirect, render_template, request, url_for, Markup
from werkzeug.exceptions import abort
import markdown, re

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
    # parse Markdown in the comments
    master['comments'] = Markup(markdown.markdown(master['comments']))

    # get release data
    cursor.execute(
        'SELECT * FROM msrelease R'
        ' WHERE top_id='+str(id)
    )
    releases = cursor.fetchall()

    return render_template('master/masterdetail.html', master=master, releases=releases)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def masteredit(id):
    """
    Edit the master details.
    """
    cursor = get_db().cursor()
    # check whether we're processing the submitted form
    if request.method == 'POST':
        # gather variables
        title = request.form['title']
        artist = request.form['artist']
        cert = request.form['cert']
        year = request.form['year']
        genres = request.form['genres']
        producer = request.form['producer']
        cover_designer = request.form['cover_designer']
        discogs_mid = request.form['discogs_mid']
        comments = request.form['comments']

        # attempt to filter out <script> tags
        comments = re.sub('<(\/?)script', '<\\1code', comments)

        error = None

        # a little validation
        if cert not in ['none', 'gold', 'platinum', 'multi-platinum', 'diamond']:
            error = 'Invalid certification.'
        elif int(year) < 1900:
            error = 'Invalid year.'
        #TODO think of more, maybe?

        if error is None:
            ret = cursor.execute(
                'UPDATE msmaster'
                ' SET title=%s, artist=%s, cert=%s, year=%s, genres=%s, producer=%s, cover_designer=%s, discogs_mid=%s, comments=%s'
                ' WHERE top_id=%s',
                (title, artist, cert, year, genres, producer, cover_designer, discogs_mid, comments, id)
            )

            return redirect(url_for('master.masterdetail', id=id))
        flash(error)

    # get the current data to stick into the form
    cursor.execute(
        'SELECT * FROM msmaster M'
        ' WHERE M.top_id='+str(id)
    )
    master = cursor.fetchone()
    return render_template('master/masteredit.html', master=master)

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    """
    Add new master entry.
    """
    cursor = get_db().cursor()
    # check whether we're processing the submitted form
    if request.method == 'POST':
        # gather variables
        title = request.form['title']
        artist = request.form['artist']
        cert = request.form['cert']
        year = request.form['year']
        genres = request.form['genres']
        producer = request.form['producer']
        cover_designer = request.form['cover_designer']
        discogs_mid = request.form['discogs_mid']
        comments = request.form['comments']

        # attempt to filter out <script> tags
        comments = re.sub('<(\/?)script', '<\\1code', comments)

        error = None

        # a little validation
        if cert not in ['none', 'gold', 'platinum', 'multi-platinum', 'diamond']:
            error = 'Invalid certification.'
        elif int(year) < 1900:
            error = 'Invalid year.'
        #TODO think of more, maybe?

        if error is None:
            ret = cursor.execute(
                'INSERT INTO msmaster'
                ' (title, artist, cert, year, genres, producer, cover_designer, discogs_mid, comments)'
                ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (title, artist, cert, year, genres, producer, cover_designer, discogs_mid, comments)
            )
            cursor.execute('SELECT LAST_INSERT_ID() AS id')
            res = cursor.fetchone()

            return redirect(url_for('master.masterdetail', id=res['id']))
        flash(error)


    return render_template('master/new.html')
