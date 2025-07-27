# app/forms.py
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, FloatField, IntegerField, SelectField,
                     SubmitField, PasswordField)
from wtforms.validators import DataRequired, Email, NumberRange, Length, EqualTo
from flask_babel import lazy_gettext as _


class ProposalForm(FlaskForm):

    project_name = StringField((_('Project Name')), validators=[DataRequired(), Length(min=2, max=100)])
    project_type = SelectField(_('Project Type'), choices=[
        ('Agriculture', _('Agriculture')),
        ('Livestock', _('Livestock')),
        ('Fishing', _('Fishing')),
        ('Transportation', _('Transportation')),
        ('Food and Beverage', _('Food and Beverage')),
        ('Culture and Arts', _('Culture and Arts')),
        ('Other Business', _('Other Business')),
    ], validators=[DataRequired()])
    description = TextAreaField((_('Brief Description')), validators=[DataRequired(), Length(min=20, max=500)])
    budget = FloatField((_('Estimated Budget (Tsh)')), validators=[DataRequired(), NumberRange(min=0.01)])
    duration_weeks = IntegerField((_('Estimated Duration (weeks)')), validators=[DataRequired(), NumberRange(min=1)])
    writing_style = SelectField((_('Writing Style')), choices=[
        ('Professional', _('Professional')),
        ('Concise', _('Concise')),
        ('Detailed', _('Detailed')),
        ('Creative', _('Creative'))
    ], validators=[DataRequired()])
    complexity = SelectField((_('Complexity Level')), choices=[
        ('Low', _('Low')),
        ('Medium', _('Medium')),
        ('High', _('High'))
    ], validators=[DataRequired()])
    audience = StringField((_('Target Audience')), validators=[DataRequired(), Length(min=2, max=100)])
    contact_email = StringField((_('Contact Email for Proposal')), validators=[DataRequired(), Email()])
    mobile_number = StringField((_('Contact Mobile Number ')), validators=[DataRequired(),Length(min=11, max=12)])
    submit = SubmitField(_('Generate Proposal'))



