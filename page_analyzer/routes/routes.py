from page_analyzer.app import app
from flask import request, flash, render_template, redirect, url_for, make_response
from validators import url as validate_url
from page_analyzer.prompts import (check_url_exists, add_url, get_url_id,
                                   get_url_by_id, get_urls, create_check,
                                   get_checks_by_url_id, get_last_check_date,
                                   check_website)
from urllib.parse import urlparse


def validate_url_input(url):
    if len(url) > 255 or not validate_url(url):
        flash("Некорректный URL")
        return False
    return True


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"


def process_url(url):
    normalized_url = normalize_url(url)
    if check_url_exists(normalized_url):
        flash('Страница уже существует')
        return get_url_id(normalized_url)
    if add_url(normalized_url):
        url_id = get_url_id(normalized_url)
        if url_id is not None:
            flash('Страница успешно добавлена')
            return url_id
        else:
            flash('Произошла ошибка при получении ID')
            return None
    else:
        flash('Произошла ошибка при добавлении')
        return None


@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        url = request.form['url']
        if not validate_url_input(url):
            flash("Некорректный URL")
            return redirect(url_for('list_urls'), code=302)

        url_id = process_url(url)
        if url_id is not None:
            return redirect(url_for('show_url', url_id=url_id))
    return render_template('index.html')


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    url_data = get_url_by_id(url_id)
    if url_data is not None:
        checks = get_checks_by_url_id(url_id)
        return render_template('url.html', url=url_data, checks=checks)
    flash('Страница не найдена')
    return redirect(url_for('index'))


@app.route('/urls')
def list_urls():
    urls_data = get_urls()
    if urls_data is None:
        return render_template('urls.html', urls=[])

    last_checks = []
    for url in urls_data:
        last_check = get_last_check_date(url[0])
        last_checks.append({
            'id': url[0],
            'name': url[1],
            'created_at': url[2],
            'last_check': last_check[0] if last_check else None,
            'status_code': last_check[1] if last_check else None
        })
    return render_template('urls.html', urls=last_checks)


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def check_url(url_id):
    url_data = get_url_by_id(url_id)
    if url_data is None:
        flash('URL не найден')
        return redirect(url_for('index'))
    status_code, h1, title, description = check_website(url_data[1])
    if status_code is None:
        flash("Произошла ошибка при проверке")
        return redirect(url_for('show_url', url_id=url_id))
    if create_check(url_id, status_code, h1, title, description):
        flash("Страница успешно проверена")
    else:
        flash("Не удалось создать проверку.")
    return redirect(url_for('show_url', url_id=url_id))
