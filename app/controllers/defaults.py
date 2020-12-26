from flask import render_template, flash, redirect, url_for
import os

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
        update_file_pjsip()

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
        update_file_pjsip()

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
    update_file_pjsip()

    flash("Ramal deletado com Sucesso")
    return redirect(url_for('extension_list'))


def update_file_pjsip():
    extensions = Extension.query.all()
    list_extension = list
    text_extension = """
[simpletrans]
type=transport
protocol=udp
bind=0.0.0.0
"""

    for ext in extensions:
        text_extension = text_extension + f"""
;--------EXTENSION {ext.extension}--------

[{ext.extension}]
type=endpoint
context=internal
disallow=all
allow=ulaw
auth=auth{ext.extension}
aors={ext.extension}

[auth{ext.extension}]
type=auth
auth_type=userpass
password={ext.password}
username={ext.extension}

[{ext.extension}]
type=aor
max_contacts=1

;------END EXTENSION {ext.extension}------
"""

    file = open('/etc/asterisk/pjsip.conf', 'w')
    file.truncate(0)
    file.writelines(text_extension)
    file.close()

    os.popen("sudo asterisk -x 'core reload'", 'w').write('ranaeu21')