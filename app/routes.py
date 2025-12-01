from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Birthday
from app.auth import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    """Display all birthdays sorted by upcoming"""
    birthdays = Birthday.query.all()
    # Sort by days until birthday
    birthdays.sort(key=lambda x: x.days_until_birthday())
    categories = Birthday.get_categories()
    return render_template('index.html', birthdays=birthdays, categories=categories)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add a new birthday"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        date_str = request.form.get('date', '')
        category = request.form.get('category', 'Other')
        notes = request.form.get('notes', '').strip()
        
        if not name or not date_str:
            flash('Please provide both name and date', 'error')
            return redirect(url_for('main.add'))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            birthday = Birthday(
                name=name, 
                date=date, 
                category=category,
                notes=notes if notes else None
            )
            db.session.add(birthday)
            db.session.commit()
            flash(f'Birthday for {name} added successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid date format', 'error')
            return redirect(url_for('main.add'))
    
    categories = Birthday.get_categories()
    return render_template('add.html', categories=categories)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing birthday"""
    birthday = Birthday.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        date_str = request.form.get('date', '')
        category = request.form.get('category', 'Other')
        notes = request.form.get('notes', '').strip()
        
        if not name or not date_str:
            flash('Please provide both name and date', 'error')
            return redirect(url_for('main.edit', id=id))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            birthday.name = name
            birthday.date = date
            birthday.category = category
            birthday.notes = notes if notes else None
            db.session.commit()
            flash(f'Birthday for {name} updated successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid date format', 'error')
            return redirect(url_for('main.edit', id=id))
    
    categories = Birthday.get_categories()
    return render_template('edit.html', birthday=birthday, categories=categories)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete a birthday"""
    birthday = Birthday.query.get_or_404(id)
    db.session.delete(birthday)
    db.session.commit()
    flash(f'Birthday for {birthday.name} deleted', 'success')
    return redirect(url_for('main.index'))
