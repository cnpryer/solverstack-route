from .utils import timestamp

from app import db

def create_fk(identifier:str, nullable:bool=False):
    return db.Column(db.Integer, db.ForeignKey(identifier), nullable=nullable)

class Model(db.Model):
    """
    Models are solution design instances. These consist of:
      - model identifiers
      - data chassis identifiers
    """
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))

class Scenario(db.Model):
    """
    Scenarios are subsets of models meant to abstract any representation of model configurations.
      - scenario identifier (pk)
      - scenario name string
      - model identifier (fk)
    """
    __tablename__ = 'scenario'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    model_id = create_fk('model.id')

class Unit(db.Model):
    """
    Units are unit of measure resources. For example, 'pallets', 'pounds', 'haversine miles', etc.
      - unit of measure identifier (pk)
      - unit of measure string
    """
    __tablename__ = 'unit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

class Origin(db.Model):
    """
    Origins defined by users. 
      - origin_id
      - latitude
      - longitude
    """
    __tablename__ = 'origin'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Demand(db.Model):
    """
    Demand is a destination node to be routed.
      - demand identifier (pk)
      - geocodes (latitude & longitude)
      - units for capacity constraint
      - unit identifier (fk)
      - cluster identifier for sub-problem spaces
      - model identifier (fk)
    """
    __tablename__ = 'demand'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    units = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.id')
    cluster_id = db.Column(db.Integer)
    model_id = create_fk('model.id')

class AssetClass(db.Model):
    """
    AssetClass identifies available assets to use.
      - asset class identifier (pk)
    """
    __tablename__ = 'asset_class'

    id = db.Column(db.Integer, primary_key=True)

class Vehicle(db.Model):
    """
    Vehicle is defined by capacity and other configurables to be used.
      - vehicle identifier (pk)
      - max capacity constraint
      - unit identifier (fk)
      - asset class identifier (fk)
    """
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    max_capacity_units = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.id')
    asset_class_id = create_fk('asset_class.id')

class Stop(db.Model):
    """
    Stops are extensions of vehicles (desired output for vrp solutions).
      - scenario identifier (fk)
      - vehicle identifer (fk)
      - stop number
      - travel distance
      - unit identifier (fk)
      - demand identifier (fk)
    """
    __tablename__ = 'stop'

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = create_fk('scenario.id')
    vehicle_id = create_fk('vehicle.id')
    stop_num = db.Column(db.Integer, nullable=False)
    stop_distance = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.id')
    demand_id = create_fk('demand.id')