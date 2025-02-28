from flask import Blueprint, render_template, redirect, url_for, flash, request

projects_bp = Blueprint('projects', __name__)