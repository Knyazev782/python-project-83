from page_analyzer import app
from flask import request, flash, render_template, redirect, url_for
from validators import url as validate_url
from page_analyzer.requests import (check_url_exists,
                                    add_url, get_url_id,
                                    get_url_by_id, get_urls)


def validate_url_input(url):
    if len(url) > 255 or not validate_url(url):
        flash("Некорректный URL")
        return False
    return True


def process_url(url):
    if check_url_exists(url):
        flash('Страница уже существует')
        return None

    if add_url(url):
        url_id = get_url_id(url)
        if url_id is not None:
            flash('Страница успешно добавлена')
            return url_id
        else:
            flash('Произошла ошибка при получении ID')
            return None
    else:
        flash('Произошла ошибка при добавлении')
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        url = request.form['url']
        if not validate_url_input(url):
            return render_template('index.html')

        url_id = process_url(url)
        if url_id is not None:
            return redirect(url_for('show_url', url_id=url_id))
        return render_template('index.html')


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    url_data = get_url_by_id(url_id)
    if url_data is not None:
        return render_template('url.html', url=url_data)
    flash('Страница не найдена')
    return redirect(url_for('list_urls'))


@app.route('/urls')
def list_urls():
    urls = get_urls()
    return render_template('urls.html', urls=urls)
