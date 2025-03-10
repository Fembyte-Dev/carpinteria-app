from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from app.models.project import Project, Advance
from app.models.client import Client
from datetime import datetime
from bson import ObjectId, json_util


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
        client_id = request.form.get('client_id')
        if not ObjectId.is_valid(client_id):
            flash('ID de cliente inválido', 'danger')
            return redirect(url_for('projects.create_project_form'))
        
        client = Client.objects(id=ObjectId(client_id)).first()
        if not client:
            flash('Cliente no encontrado', 'danger')
            return redirect(url_for('projects.create_project_form'))
        
        project = Project(
            name=request.form.get('name'),
            description=request.form.get('description'),
            client=client,
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
    clients = Client.objects(active=True)
    return render_template('projects/edit.html', project=project, clients=clients)

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
        client_id = request.form.get('client_id')
        if not ObjectId.is_valid(client_id):
            flash('ID de cliente inválido', 'danger')
            return redirect(url_for('projects.edit_project_form', project_id=project_id))
        
        client = Client.objects(id=ObjectId(client_id)).first()
        if not client:
            flash('Cliente no encontrado', 'danger')
            return redirect(url_for('projects.edit_project_form', project_id=project_id))
        
        project.client = client
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

@projects_bp.route('/projects/<project_id>/advances', methods=['GET'])
@login_required
def get_advances(project_id):
    project = Project.objects(id=project_id, active=True).first()

    if not project:
        return Response(
            json_util.dumps({'error': 'Project not found'}),
            status=404,
            mimetype='application/json'
        )

    advances_list = [advance.to_mongo() for advance in project.advances]
    data = json_util.dumps({'advances': advances_list}, default=json_util.default)
    return Response(data, mimetype='application/json')

@projects_bp.route('/projects/<project_id>/advances/<advance_id>', methods=['GET'])
@login_required
def get_advance(project_id, advance_id):
    """Get a single advance by ID"""
    project = Project.objects(id=project_id, active=True).first()
    if not project:
        return {'error': 'Project not found'}, 404

    advance = next((a for a in project.advances if str(a.id) == advance_id), None)
    data = json_util.dumps(advance.to_mongo(), default=json_util.default)
    if not advance:
        return {'error': 'Advance not found'}, 404
    return Response(data, mimetype='application/json')

@projects_bp.route('/projects/<project_id>/advances', methods=['POST'])
@login_required
def add_advance(project_id):
    if not ObjectId.is_valid(project_id):
        return {'error': 'ID de proyecto inválido'}, 400

    data = request.get_json()
    required = ['concept', 'amount', 'date']
    
    if not all(field in data for field in required):
        return {'error': 'Faltan campos obligatorios'}, 400
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return {'error': 'Monto inválido'}, 400
            
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        if date > datetime.now():
            return {'error': 'Fecha futura no permitida'}, 400
            
        project = Project.objects(id=project_id, active=True).first()
        if not project:
            return {'error': 'Proyecto no encontrado'}, 404
            
        advance = Advance(
            id=ObjectId(),
            concept=data['concept'],
            amount=amount,
            date=date
        )
        project.advances.append(advance)
        project.save()
        
        return {'message': 'Anticipo agregado'}, 201
    except ValueError:
        return {'error': 'Formato de fecha o monto incorrecto'}, 400
    except Exception as e:
        return {'error': f'Error inesperado: {str(e)}'}, 500

@projects_bp.route('/projects/<project_id>/advances/<advance_id>', methods=['PUT'])
@login_required
def update_advance(project_id, advance_id):
    """Update an existing advance"""
    data = request.get_json()
    print(data)
    if not data or 'amount' not in data or 'date' not in data:
        return {'error': 'Missing required fields'}, 400

    try:
        # First check if the project and advance exist
        project = Project.objects(id=project_id, active=True).first()
        if not project:
            return {'error': 'Project not found'}, 404
            
        # Find the advance in the project's advances list
        advance = next((a for a in project.advances if str(a.id) == advance_id), None)
        if not advance:
            return {'error': 'Advance not found'}, 404
            
        # Update the advance directly
        update_data = {
            f'set__advances__S__amount': float(data['amount']),
            f'set__advances__S__date': datetime.strptime(data['date'], '%Y-%m-%d')
        }
        
        # Use the positional operator $ to update the matched element
        Project.objects(id=project_id, advances__id=advance_id).update_one(
            **{k.replace('S', '$'): v for k, v in update_data.items()}
        )
        
        return {'message': 'Advance updated successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 400

@projects_bp.route('/projects/<project_id>/advances/<advance_id>', methods=['DELETE'])
@login_required
def delete_advance(project_id, advance_id):
    """Delete an advance from a project"""
    try:
        print(f"Deleting advance {advance_id} from project {project_id}")
        result = Project.objects(id=project_id).update_one(pull__advances__id=advance_id)
        if result == 0:
            return {'error': 'Advance not found'}, 404
        return {'message': 'Advance deleted successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 400

