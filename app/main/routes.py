from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, make_response
from flask_login import current_user, login_required
from app import db
#from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm
from app.models import User, Demand
from app.main import bp
from io import TextIOWrapper, StringIO
import csv

from ..utils import timestamp

from pyords.cluster.implementations import create_dbscan_expanded_clusters
from pyords.distance.haversine import create_haversine_matrix
import pyords as pyr
import pandas as pd
import numpy as np


ALLOWED_EXTENSIONS = {'csv'}

def init_vrp_w_df(dataframe:pd.DataFrame):
    lats, lons = dataframe.latitude, dataframe.longitude
    origins = [(41.4191, -87.7748)]
    matrix = create_haversine_matrix(origins, lats, lons)
    # unit is load for each node with demand (in this case
    # only destinations). inserting 0 at the front of the array
    demand = np.insert(dataframe.pallets.values, 0, 0)

    return matrix, demand

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
            for row in csv_reader: # assumes first row is field names
                columns = list(row)
                break
            # get position of uploaded fields for more dynamic storage population
            positions = {col: i for i, col in enumerate(columns)}
            for i, row in enumerate(csv_reader):
                if i > 0:  # upload values only (field names are first row)
                    demand = Demand(
                        latitude=row[positions['latitude']],
                        longitude=row[positions['longitude']],
                        weight=row[positions['weight']],
                        pallets=row[positions['pallets']],
                        upload_date=timestamp(),
                        user_id=user_id)
                    db.session.add(demand)
                    db.session.commit()

            flash('upload successful!')
            return redirect(url_for('main.index'))
    return render_template('upload.html')

@bp.route('/cvrp', methods=['GET', 'POST'])
@login_required
def cvrp():
    if request.method == 'GET':
        user_id = current_user.get_id()
        demand = db.engine.execute('select * from demand '
            ' where demand.user_id = %s' % user_id).fetchall()
        data = [dict(row) for row in demand]
        
        df = pd.DataFrame(data)
        if df.empty:
            flash('upload data')
            return redirect(url_for('main.upload'))

        # simplify euclidean distance calculation by projecting to positive vals
        x = df.latitude.values + 90
        y = df.longitude.values + 180
        df['cluster'] = create_dbscan_expanded_clusters(x, y)

        results = pd.DataFrame(columns=df.columns.tolist())
        for cluster in df.cluster.unique():
            clustered_df = df[df.cluster == cluster].copy().reset_index(drop=True)
            
            matrix, demand = init_vrp_w_df(clustered_df)
            bndl = pyr.VrpBundle(matrix=matrix, demand=demand)
            clustered_df = bndl.run().cast_solution_to_df(clustered_df)
            clustered_df.vehicle = str(int(cluster)) + '-' + clustered_df.vehicle.astype(int)\
                .astype(str)
            results = results.append(clustered_df, sort=False)

        df = results.copy()
        
        df = df.sort_values(by='vehicle')
        solution = df.to_json(orient='records')

    return render_template('cvrp.html', data=data, solution=solution)

@bp.route('/download')
@login_required
def download():
    user_id = current_user.get_id()
    si = StringIO()
    csv_writer = csv.writer(si)
    cursor = db.engine.execute('select * from demand '
        ' where user_id = %s' % user_id)
    columns = cursor.keys()
    rows = cursor.fetchall()
    csv_writer.writerow(columns)
    csv_writer.writerows(rows)
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = \
        'attachment; filename=solution.csv'
    response.headers['Content-type'] = 'text/csv'
    return response
