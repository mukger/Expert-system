from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
from es import Es

app = Flask(__name__)
app.config['SECRET_KEY'] = "MYSECRET"
Bootstrap5(app)


class CheckForm(FlaskForm):
    offside_check_system = SelectField(u'Offside check system:',
                                       choices=[(1, 'false'), (2, 'true')],
                                       default=1, validators=[DataRequired()])
    var_tip = SelectField(u'Availability of var tip:',
                          choices=[(1, 'false'), (2, 'true')],
                          default=1, validators=[DataRequired()])
    refereeing_style = SelectField(u'Refereeing style:',
                                   choices=[(1, 'liberal'), (2, 'objective'), (3, 'rigorous')],
                                   default=2, validators=[DataRequired()])
    game_density = SelectField(u'Game density:',
                               choices=[(1, 'affiliated'), (2, 'intensive'), (3, 'variable')],
                               default=1, validators=[DataRequired()])
    violation = SelectField(u'Violation type:',
                                 choices=[(1, 'none'), (2, 'foul'), (3, 'offside')],
                                 default=1, validators=[DataRequired()])
    submit = SubmitField(label="Process")


@app.route('/', methods=['GET', 'POST'])
def get_all_posts():
    form = CheckForm()
    if form.validate_on_submit():
        es = Es()
        es.assert_facts(form)

        return render_template("index.html", form=form, showDecision=True, decision=es.get_result())
    return render_template("index.html", form=form, showDecision=False)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
