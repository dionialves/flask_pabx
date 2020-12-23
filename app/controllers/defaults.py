from flask import render_template, flash, redirect, url_for

from app.forms.extension_form import ExtensionForm
from app.models.extension import Extension
from app import app, db


# Index
@app.route('/')
def index():
    title = 'Pagina Inicial'
    return render_template('index.html', title=title)


# Extension
@app.route('/extension/list')
def extension_list():
    title = 'Lista de Ramais'
    ext = Extension.query.all()
    return render_template('extension/extension_list.html', title=title, object=ext)


@app.route('/extension/add', methods=['GET', 'POST'])
def extension_add():
    title = 'Novo Ramal'
    form = ExtensionForm()
    if form.validate_on_submit():
        ext = Extension(
            name=form.name.data,
            extension=form.extension.data,
            password=form.password.data
        )
        db.session.add(ext)
        db.session.commit()
        flash("Ramal cadastrado com Sucesso")
        return redirect(url_for('extension_list'))
    return render_template('extension/extension.html',
                           title=title,
                           form=form)


@app.route('/extension/<int:extension_id>', methods=['GET', 'POST'])
def extension(extension_id):
    ext = Extension.query.get(extension_id)
    title = 'Editar Ramal: ' + str(ext.extension)
    form = ExtensionForm(obj=ext)
    if form.validate_on_submit():
        ext.name = form.name.data
        ext.extension = form.extension.data
        ext.password = form.password.data

        db.session.add(ext)
        db.session.commit()
        flash("Ramal atualizado com Sucesso")
        return redirect(url_for('extension_list'))
    return render_template('extension/extension.html',
                           title=title,
                           extension_id=extension_id,
                           form=form,
                           obj=ext)


@app.route('/extension/<int:extension_id>/delete')
def extension_delete(extension_id):
    ext = Extension.query.get(extension_id)
    db.session.delete(ext)
    db.session.commit()

    flash("Ramal deletado com Sucesso")
    return redirect(url_for('extension_list'))