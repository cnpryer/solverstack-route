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

    model_id = db.Column(db.Integer, primary_key=True)
    data_chassis_id = create_fk('data_chassis.data_chassis_id')

class DataChassis(db.Model):
    """
    DataChassis is configuration to formulate a problem definition.
      - data chassis identifier (pk)
      - origin identifier (fk)
      - demand idendifier (fk)
      - asset class identifier (fk)
    """
    __tablename__ = 'data_chassis'

    data_chassis_id = db.Column(db.Integer, primary_key=True)
    origin_id = create_fk('origin.origin_id')
    demand_id = create_fk('demand.demand_id')
    asset_class_id = create_fk('asset_class.asset_class_id')

class Scenario(db.Model):
    """
    Scenarios are subsets of models meant to abstract any representation of model configurations.
      - scenario identifier (pk)
      - scenario name string
      - model identifier (fk)
    """
    __tablename__ = 'scenario'

    scenario_id = db.Column(db.Integer, primary_key=True)
    scenario_name = db.Column(db.String(16))
    model_id = create_fk('model.model_id')

class Unit(db.Model):
    """
    Units are unit of measure resources. For example, 'pallets', 'pounds', 'haversine miles', etc.
      - unit of measure identifier (pk)
      - unit of measure string
    """
    __tablename__ = 'unit'

    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(10))

class Demand(db.Model):
    """
    Demand is a destination node to be routed.
      - demand identifier (pk)
      - geocodes (latitude & longitude)
      - units for capacity constraint
      - unit identifier (fk)
      - cluster identifier for sub-problem spaces
    """
    __tablename__ = 'demand'

    demand_id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    units = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.unit_id')
    cluster_id = db.Column(db.Integer)

class AssetClass(db.Model):
    """
    AssetClass identifies available assets to use.
      - asset class identifier (pk)
    """
    __tablename__ = 'asset_class'

    asset_class_id = db.Column(db.Integer, primary_key=True)

class Vehicle(db.Model):
    """
    Vehicle is defined by capacity and other configurables to be used.
      - vehicle identifier (pk)
      - max capacity constraint
      - unit identifier (fk)
      - asset class identifier (fk)
    """
    __tablename__ = 'vehicle'

    vehicle_id = db.Column(db.Integer, primary_key=True)
    max_capacity = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.unit_id')
    asset_class_id = create_fk('asset_class.asset_class_id')

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

    stop_id = db.Column(db.Integer, primary_key=True)
    scenario_id = create_fk('scenario.scenario_id')
    vehicle_id = create_fk('vehicle.vehicle_id')
    stop_num = db.Column(db.Integer, nullable=False)
    stop_distance = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.unit_id')
    demand_id = create_fk('demand.demand_id')

class Origin(db.Model):
    """
    Origins defined by users. 
      - origin_id
      - latitude
      - longitude
    """
    __tablename__ = 'origin'

    origin_id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)