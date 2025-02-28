from flask import Blueprint, render_template, redirect, url_for, flash, request

clients_bp = Blueprint('clients', __name__)