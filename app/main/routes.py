from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
#from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm
from app.models import User, Demand
from app.main import bp
from io import TextIOWrapper
import csv

from ..utils import timestamp

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            user_id = current_user.get_id()
            current_time = timestamp()
            Demand.query.filter_by(user_id=user_id).delete()
            csv_file = TextIOWrapper(file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            columns = []
            for row in csv_reader: # assmes first row is field names
                columns = list(row)
                break
            positions = {col: i for i, col in enumerate(columns)}
            for i, row in enumerate(csv_reader):
                if i > 0:
                    demand = Demand(
                        latitude=row[positions['latitude']],
                        longitude=row[positions['longitude']],
                        weight=row[positions['weight']],
                        pallets=row[positions['pallets']],
                        upload_date=timestamp(),
                        user_id=user_id
                    )
                    db.session.add(demand)
                    db.session.commit()
            return redirect('/cvrp')
    return render_template('upload.html')

@bp.route('/cvrp', methods=['GET', 'POST'])
@login_required
def cvrp():
    if request.method == 'GET':
        user = current_user.get_id()
        demand = db.engine.execute(
            'select * from demand where demand.user_id = %s' % user).fetchall()
        data = [dict(row) for row in demand]
    return render_template('cvrp.html', data=data)
