from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length


class AssessmentForm(FlaskForm):
    module_code = StringField('Module Code', validators=[
                              DataRequired(), Length(max=20)])

    assessment_title = StringField('Assessment Title', validators=[
                                   DataRequired(), Length(max=100)])

    description = TextAreaField('Description', validators=[Length(max=500)])

    due_date = DateField('Due Date', validators=[

                         DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Save')


class Button(FlaskForm):
    toggle = SubmitField('toggle complete')
