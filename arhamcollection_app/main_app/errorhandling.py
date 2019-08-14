from flask import render_template


def page_not_found_404(e):
    return render_template('main_app/404.html'), 404


def page_not_found_403(e):
    return render_template('main_app/403.html'), 403


def page_not_found_500(e):
    return render_template('main_app/500.html'), 500