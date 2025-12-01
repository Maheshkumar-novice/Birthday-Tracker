from datetime import datetime, date
from app import db

class Birthday(db.Model):
    """Birthday model for storing birthday information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), default='Other')
    notes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Birthday {self.name} - {self.date}>'
    
    def has_year(self):
        """Check if birth year is known (not sentinel value 1900)"""
        return self.date.year != 1900
    
    def days_until_birthday(self):
        """Calculate days until next birthday"""
        today = datetime.today().date()
        # Use the actual month/day but current or next year
        this_year_birthday = self.date.replace(year=today.year)
        
        if this_year_birthday < today:
            this_year_birthday = self.date.replace(year=today.year + 1)
        
        return (this_year_birthday - today).days
    
    def age_on_next_birthday(self):
        """Calculate age on next birthday (returns None if year unknown)"""
        if not self.has_year():
            return None
            
        today = datetime.today().date()
        this_year_birthday = self.date.replace(year=today.year)
        
        if this_year_birthday >= today:
            return today.year - self.date.year
        else:
            return today.year - self.date.year + 1
    
    @staticmethod
    def get_categories():
        """Return list of available categories"""
        return ['Family', 'Friends', 'Work', 'Other']
