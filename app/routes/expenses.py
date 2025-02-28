# app/routes/expenses.py

from flask import Blueprint, render_template, redirect, url_for, flash, request

expenses_bp = Blueprint('expenses', __name__)