from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models import ConfTemplate, Service, ServiceHasConfTemplate
from app.forms import ConfTemplateForm
from app.security import validate_form_fields

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/create_template', methods=['GET', 'POST'])
@login_required
def create_template():
    form = ConfTemplateForm()
    if form.validate_on_submit():
        validate_form_fields(request.form)

        template = ConfTemplate(
            name=form.name.data,
            os=form.os.data,
            description=form.description.data,
            photo=form.photo.data,
            cores=form.cores.data,
            cpu_freq=form.cpu_freq.data,
            gpu_cores=form.gpu_cores.data,
            cuda=form.cuda.data,
            gpu_freq=form.gpu_freq.data,
            ram_mem=form.ram_mem.data,
            ram_freq=form.ram_freq.data,
            memory=form.memory.data,
            price=form.price.data,
            discount=form.discount.data
        )
        db.session.add(template)
        db.session.commit()

        service_names = request.form.getlist('services')
        for service_name in service_names:
            service_name = service_name.strip()
            if not service_name:
                continue
            service = Service.query.filter_by(service_name=service_name).first()
            if not service:
                service = Service(service_name=service_name)
                db.session.add(service)
                db.session.commit()
            link = ServiceHasConfTemplate(service_id=service.id, conf_template_id=template.id)
            db.session.add(link)
        db.session.commit()

        flash('Шаблон успешно создан!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_vm.html', form=form)

@bp.route('/edit_template', methods=['POST'])
@login_required
def edit_template():
    if not current_user.is_admin:
        abort(403)

    validate_form_fields(request.form)

    template_id = request.form.get('id')
    template = ConfTemplate.query.get_or_404(template_id)

    template.name = request.form.get('name')
    template.os = request.form.get('os')
    template.description = request.form.get('description')
    template.photo = request.form.get('photo')
    template.cores = int(request.form.get('cores'))
    template.cpu_freq = float(request.form.get('cpu_freq'))
    template.gpu_cores = int(request.form.get('gpu_cores'))
    template.cuda = int(request.form.get('cuda'))
    template.gpu_freq = float(request.form.get('gpu_freq'))
    template.ram_mem = int(request.form.get('ram_mem'))
    template.ram_freq = int(request.form.get('ram_freq'))
    template.memory = int(request.form.get('memory'))
    template.price = int(request.form.get('price'))
    template.discount = int(request.form.get('discount'))

    db.session.commit()
    flash('Шаблон обновлен!', 'success')
    return redirect(url_for('main.index'))
