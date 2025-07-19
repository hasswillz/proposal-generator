# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class ProposalForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=100)])
    project_type = SelectField('Project Type', choices=[
        ('Software Development', 'Software Development'),
        ('Research & Development', 'Research & Development'),
        ('Consulting', 'Consulting'),
        ('Marketing Campaign', 'Marketing Campaign'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Brief Description', validators=[DataRequired(), Length(min=20, max=500)])
    budget = FloatField('Estimated Budget (Tsh)', validators=[DataRequired(), NumberRange(min=0.01)])
    duration_weeks = IntegerField('Estimated Duration (weeks)', validators=[DataRequired(), NumberRange(min=1)])
    writing_style = SelectField('Writing Style', choices=[
        ('Professional', 'Professional'),
        ('Concise', 'Concise'),
        ('Detailed', 'Detailed'),
        ('Creative', 'Creative')
    ], validators=[DataRequired()])
    complexity = SelectField('Complexity Level', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ], validators=[DataRequired()])
    audience = StringField('Target Audience', validators=[DataRequired(), Length(min=2, max=100)])
    contact_email = StringField('Contact Email for Proposal', validators=[DataRequired(), Email()])
    submit = SubmitField('Generate Proposal')