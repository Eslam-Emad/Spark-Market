from flask_wtf import FlaskForm
from wtforms import SubmitField


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
