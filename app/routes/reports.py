# app/routes/expenses.py

from flask import Blueprint, render_template, redirect, url_for, flash, request

reports_bp = Blueprint('reports', __name__)