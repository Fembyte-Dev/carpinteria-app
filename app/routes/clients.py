from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.client import Client, Contact, Address, FiscalData, Notes

clients_bp = Blueprint('clients', __name__)

# Ruta para listar todos los clientes
@clients_bp.route('/clients', methods=['GET'])
@login_required
def index():
    """
    Muestra una lista de todos los clientes activos.
    """
    clients = Client.objects(active=True)  # Filtra solo clientes activos
    return render_template('clients/index.html', clients=clients)

# Ruta para mostrar el formulario de creación de un cliente
@clients_bp.route('/clients/create', methods=['GET'])
@login_required
def create_client_form():
    """
    Renderiza el formulario para crear un nuevo cliente.
    """
    return render_template('clients/create.html')

# Ruta para procesar la creación de un cliente
@clients_bp.route('/clients/create', methods=['POST'])
@login_required
def create_client():
    """
    Procesa el formulario de creación y guarda el nuevo cliente en la base de datos.
    """
    try:
        # Obtener datos del formulario
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        second_last_name = request.form.get('second_last_name', '')  # Opcional

        # Datos embebidos (pueden ser opcionales)
        contact = Contact(
            phone_mobile=request.form.get('phone_mobile', ''),
            phone_landline=request.form.get('phone_landline', ''),
            email=request.form.get('email', '')
        ) if any([request.form.get('phone_mobile'), request.form.get('phone_landline'), request.form.get('email')]) else None

        address = Address(
            street=request.form.get('street', ''),
            city=request.form.get('city', ''),
            state=request.form.get('state', ''),
            zip=request.form.get('zip', '')
        ) if any([request.form.get('street'), request.form.get('city'), request.form.get('state'), request.form.get('zip')]) else None

        fiscal_data = FiscalData(
            rfc=request.form.get('rfc', ''),
            fiscal_name=request.form.get('fiscal_name', ''),
            regimen=request.form.get('regimen', ''),
            fiscal_zip=request.form.get('fiscal_zip', ''),
            requires_invoice=request.form.get('requires_invoice') == 'on'
        ) if any([request.form.get('rfc'), request.form.get('fiscal_name'), request.form.get('regimen'), request.form.get('fiscal_zip')]) else None

        notes = Notes(
            preferences=request.form.get('preferences', ''),
            observations=request.form.get('observations', '')
        ) if any([request.form.get('preferences'), request.form.get('observations')]) else None

        # Crear el nuevo cliente
        client = Client(
            first_name=first_name,
            last_name=last_name,
            second_last_name=second_last_name,
            contact=contact,
            address=address,
            fiscal_data=fiscal_data,
            notes=notes
        )
        client.save()
        flash('Cliente creado exitosamente.', 'success')
        return redirect(url_for('clients.index'))
    except Exception as e:
        flash(f'Error al crear cliente: {str(e)}', 'danger')
        return redirect(url_for('clients.create_client_form'))

# Ruta para mostrar el formulario de edición de un cliente
@clients_bp.route('/clients/edit/<client_id>', methods=['GET'])
@login_required
def edit_client_form(client_id):
    """
    Renderiza el formulario para editar un cliente existente.
    """
    client = Client.objects(id=client_id, active=True).first()
    if not client:
        flash('Cliente no encontrado.', 'danger')
        return redirect(url_for('clients.index'))
    return render_template('clients/edit.html', client=client)

# Ruta para procesar la actualización de un cliente
@clients_bp.route('/clients/edit/<client_id>', methods=['POST'])
@login_required
def edit_client(client_id):
    """
    Procesa el formulario de edición y actualiza el cliente en la base de datos.
    """
    client = Client.objects(id=client_id, active=True).first()
    if not client:
        flash('Cliente no encontrado.', 'danger')
        return redirect(url_for('clients.index'))

    try:
        # Actualizar datos básicos
        client.first_name = request.form.get('first_name')
        client.last_name = request.form.get('last_name')
        client.second_last_name = request.form.get('second_last_name', '')

        # Actualizar o crear datos embebidos
        client.contact = client.contact or Contact()
        client.contact.phone_mobile = request.form.get('phone_mobile', '')
        client.contact.phone_landline = request.form.get('phone_landline', '')
        client.contact.email = request.form.get('email', '')

        client.address = client.address or Address()
        client.address.street = request.form.get('street', '')
        client.address.city = request.form.get('city', '')
        client.address.state = request.form.get('state', '')
        client.address.zip = request.form.get('zip', '')

        client.fiscal_data = client.fiscal_data or FiscalData()
        client.fiscal_data.rfc = request.form.get('rfc', '')
        client.fiscal_data.fiscal_name = request.form.get('fiscal_name', '')
        client.fiscal_data.regimen = request.form.get('regimen', '')
        client.fiscal_data.fiscal_zip = request.form.get('fiscal_zip', '')
        client.fiscal_data.requires_invoice = request.form.get('requires_invoice') == 'on'

        client.notes = client.notes or Notes()
        client.notes.preferences = request.form.get('preferences', '')
        client.notes.observations = request.form.get('observations', '')

        client.save()
        flash('Cliente actualizado exitosamente.', 'success')
        return redirect(url_for('clients.index'))
    except Exception as e:
        flash(f'Error al actualizar cliente: {str(e)}', 'danger')
        return redirect(url_for('clients.edit_client_form', client_id=client_id))

# Ruta para eliminar un cliente (cambio de estado a inactivo)
@clients_bp.route('/clients/delete/<client_id>', methods=['POST'])
@login_required
def delete_client(client_id):
    """
    Marca un cliente como inactivo en lugar de eliminarlo físicamente.
    """
    client = Client.objects(id=client_id, active=True).first()
    if not client:
        flash('Cliente no encontrado.', 'danger')
    else:
        try:
            client.active = False
            client.save()
            flash('Cliente eliminado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al eliminar cliente: {str(e)}', 'danger')
    return redirect(url_for('clients.index'))