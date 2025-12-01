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
        month = request.form.get('month', '')
        day = request.form.get('day', '')
        year = request.form.get('year', '').strip()
        category = request.form.get('category', 'Other')
        notes = request.form.get('notes', '').strip()
        
        if not name or not month or not day:
            flash('Please provide name, month, and day', 'error')
            return redirect(url_for('main.add'))
        
        try:
            # Use 1900 as sentinel year if year not provided
            birth_year = int(year) if year else 1900
            birth_month = int(month)
            birth_day = int(day)
            
            birth_date = datetime(birth_year, birth_month, birth_day).date()
            
            birthday = Birthday(
                name=name, 
                date=birth_date, 
                category=category,
                notes=notes if notes else None
            )
            db.session.add(birthday)
            db.session.commit()
            flash(f'Birthday for {name} added successfully!', 'success')
            return redirect(url_for('main.index'))
        except (ValueError, TypeError) as e:
            flash('Invalid date', 'error')
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
        month = request.form.get('month', '')
        day = request.form.get('day', '')
        year = request.form.get('year', '').strip()
        category = request.form.get('category', 'Other')
        notes = request.form.get('notes', '').strip()
        
        if not name or not month or not day:
            flash('Please provide name, month, and day', 'error')
            return redirect(url_for('main.edit', id=id))
        
        try:
            # Use 1900 as sentinel year if year not provided
            birth_year = int(year) if year else 1900
            birth_month = int(month)
            birth_day = int(day)
            
            birth_date = datetime(birth_year, birth_month, birth_day).date()
            
            birthday.name = name
            birthday.date = birth_date
            birthday.category = category
            birthday.notes = notes if notes else None
            db.session.commit()
            flash(f'Birthday for {name} updated successfully!', 'success')
            return redirect(url_for('main.index'))
        except (ValueError, TypeError) as e:
            flash('Invalid date', 'error')
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

@bp.route('/export')
@login_required
def export_txt():
    """Export birthdays as plain text"""
    from flask import Response
    
    birthdays = Birthday.query.all()
    birthdays.sort(key=lambda x: x.days_until_birthday())
    
    # Create plain text output
    lines = ["BIRTHDAYS\n", "=" * 60, "\n\n"]
    
    for birthday in birthdays:
        # Format date
        if birthday.has_year():
            date_str = birthday.date.strftime('%B %d, %Y')
            age = birthday.age_on_next_birthday()
            age_str = f" (Turns {age})" if age else ""
        else:
            date_str = birthday.date.strftime('%B %d')
            age_str = ""
        
        # Days until
        days = birthday.days_until_birthday()
        if days == 0:
            days_str = "Today!"
        elif days == 1:
            days_str = "Tomorrow"
        else:
            days_str = f"In {days} days"
        
        # Build line
        line = f"{birthday.name:<20} {date_str:<20} {birthday.category:<10} {days_str}{age_str}\n"
        lines.append(line)
    
    lines.append("\n" + "=" * 60 + "\n")
    lines.append(f"Total: {len(birthdays)} birthdays\n")
    
    text_content = "".join(lines)
    
    return Response(
        text_content,
        mimetype='text/plain',
        headers={'Content-Disposition': 'attachment; filename=birthdays.txt'}
    )
