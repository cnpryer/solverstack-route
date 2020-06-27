from .utils import timestamp

from app import db

def create_fk(identifier:str, nullable:bool=False):
    return db.Column(db.Integer, db.ForeignKey(identifier), nullable=nullable)

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
      - origin identifier
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
    """
    __tablename__ = 'demand'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    units = db.Column(db.Float, nullable=False)
    unit_id = create_fk('unit.id')
    cluster_id = db.Column(db.Integer)

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

class Solution(db.Model):
  """
  Solutions are results along with their mappings to resources used
  to produce them.
    - demand identifier
    - origin identifier
    - stop identifier
    - output data
  """
  __tablename__ = 'solution'

  id = db.Column(db.Integer, primary_key=True)
  demand_id = create_fk('demand.id')
  origin_id = create_fk('origin.id')
  vehicle_id = create_fk('vehicle.id')
  stop_num = db.Column(db.Integer, nullable=False)
  stop_distance_units = db.Column(db.Float, nullable=False)
  unit_id = create_fk('unit.id')
