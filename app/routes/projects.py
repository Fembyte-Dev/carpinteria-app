from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.project import Project
from app.models.client import Client
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
@login_required
def index():
    """Lista todos los proyectos activos con filtro opcional por mes y año."""
    # Obtener mes y año de los parámetros o usar fecha actual
    try:
        month = int(request.args.get('month', datetime.now().month))
        year = int(request.args.get('year', datetime.now().year))
    except ValueError:
        flash('Parámetros de fecha inválidos.', 'danger')
        month = datetime.now().month
        year = datetime.now().year

    # Filtrar proyectos por mes y año
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    projects = Project.objects(active=True,
                             created_at__gte=start_date,
                             created_at__lt=end_date)
    
    return render_template('projects/index.html', 
                          projects=projects, 
                          current_month=month, 
                          current_year=year)

@projects_bp.route('/projects/create', methods=['GET'])
@login_required
def create_project_form():
    """Renderiza el formulario para crear un nuevo proyecto."""
    clients = Client.objects(active=True)
    return render_template('projects/create.html', clients=clients)

@projects_bp.route('/projects/create', methods=['POST'])
@login_required
def create_project():
    """Procesa el formulario de creación y guarda el nuevo proyecto."""
    try:
        project = Project(
            name=request.form.get('name'),
            description=request.form.get('description'),
            client=request.form.get('client_id'),
            estimated_cost=float(request.form.get('estimated_cost', 0)),
            status=request.form.get('status', 'pending'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d') if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d') if request.form.get('end_date') else None
        )
        project.save()
        flash('Proyecto creado exitosamente.', 'success')
        return redirect(url_for('projects.index'))
    except Exception as e:
        flash(f'Error al crear proyecto: {str(e)}', 'danger')
        return redirect(url_for('projects.create_project_form'))

@projects_bp.route('/projects/edit/<project_id>', methods=['GET'])
@login_required
def edit_project_form(project_id):
    """Renderiza el formulario para editar un proyecto existente."""
    project = Project.objects(id=project_id, active=True).first()
    if not project:
        flash('Proyecto no encontrado.', 'danger')
        return redirect(url_for('projects.index'))
    return render_template('projects/edit.html', project=project)

@projects_bp.route('/projects/edit/<project_id>', methods=['POST'])
@login_required
def edit_project(project_id):
    """Procesa el formulario de edición y actualiza el proyecto."""
    project = Project.objects(id=project_id, active=True).first()
    if not project:
        flash('Proyecto no encontrado.', 'danger')
        return redirect(url_for('projects.index'))

    try:
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        project.client = request.form.get('client_id')
        project.estimated_cost = float(request.form.get('estimated_cost', 0))
        project.status = request.form.get('status')
        project.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d') if request.form.get('start_date') else None
        project.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d') if request.form.get('end_date') else None

        project.save()
        flash('Proyecto actualizado exitosamente.', 'success')
        return redirect(url_for('projects.index'))
    except Exception as e:
        flash(f'Error al actualizar proyecto: {str(e)}', 'danger')
        return redirect(url_for('projects.edit_project_form', project_id=project_id))

@projects_bp.route('/projects/delete/<project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    """Marca un proyecto como inactivo en lugar de eliminarlo físicamente."""
    project = Project.objects(id=project_id, active=True).first()
    if not project:
        flash('Proyecto no encontrado.', 'danger')
    else:
        try:
            project.active = False
            project.save()
            flash('Proyecto eliminado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al eliminar proyecto: {str(e)}', 'danger')
    return redirect(url_for('projects.index'))

@projects_bp.route('/projects/view/<project_id>', methods=['GET'])
@login_required
def view_project(project_id):
    """Muestra los detalles de un proyecto específico."""
    project = Project.objects(id=project_id, active=True).first()
    if not project:
        flash('Proyecto no encontrado.', 'danger')
        return redirect(url_for('projects.index'))
    return render_template('projects/view.html', project=project)

