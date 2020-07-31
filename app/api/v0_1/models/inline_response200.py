# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from app import util
from app.api.models.base_model_ import Model
from app.api.v0_1.models.origin import Origin  # noqa: F401,E501
from app.api.v0_1.models.solution import Solution  # noqa: F401,E501
from app.api.v0_1.models.unit import Unit  # noqa: F401,E501


class InlineResponse200(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        origin: Origin = None,
        solutions: List[Solution] = None,
        unit: Unit = None,
        vehicle_capacity: int = None,
    ):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger

        :param origin: The origin of this InlineResponse200.  # noqa: E501
        :type origin: Origin
        :param solutions: The solutions of this InlineResponse200.  # noqa: E501
        :type solutions: List[Solution]
        :param unit: The unit of this InlineResponse200.  # noqa: E501
        :type unit: Unit
        :param vehicle_capacity: The vehicle_capacity of this InlineResponse200.  # noqa: E501
        :type vehicle_capacity: int
        """
        self.swagger_types = {
            "origin": Origin,
            "solutions": List[Solution],
            "unit": Unit,
            "vehicle_capacity": int,
        }

        self.attribute_map = {
            "origin": "origin",
            "solutions": "solutions",
            "unit": "unit",
            "vehicle_capacity": "vehicle_capacity",
        }
        self._origin = origin
        self._solutions = solutions
        self._unit = unit
        self._vehicle_capacity = vehicle_capacity

    @classmethod
    def from_dict(cls, dikt) -> "InlineResponse200":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200 of this InlineResponse200.  # noqa: E501
        :rtype: InlineResponse200
        """
        return util.deserialize_model(dikt, cls)

    @property
    def origin(self) -> Origin:
        """Gets the origin of this InlineResponse200.


        :return: The origin of this InlineResponse200.
        :rtype: Origin
        """
        return self._origin

    @origin.setter
    def origin(self, origin: Origin):
        """Sets the origin of this InlineResponse200.


        :param origin: The origin of this InlineResponse200.
        :type origin: Origin
        """

        self._origin = origin

    @property
    def solutions(self) -> List[Solution]:
        """Gets the solutions of this InlineResponse200.


        :return: The solutions of this InlineResponse200.
        :rtype: List[Solution]
        """
        return self._solutions

    @solutions.setter
    def solutions(self, solutions: List[Solution]):
        """Sets the solutions of this InlineResponse200.


        :param solutions: The solutions of this InlineResponse200.
        :type solutions: List[Solution]
        """

        self._solutions = solutions

    @property
    def unit(self) -> Unit:
        """Gets the unit of this InlineResponse200.


        :return: The unit of this InlineResponse200.
        :rtype: Unit
        """
        return self._unit

    @unit.setter
    def unit(self, unit: Unit):
        """Sets the unit of this InlineResponse200.


        :param unit: The unit of this InlineResponse200.
        :type unit: Unit
        """

        self._unit = unit

    @property
    def vehicle_capacity(self) -> int:
        """Gets the vehicle_capacity of this InlineResponse200.


        :return: The vehicle_capacity of this InlineResponse200.
        :rtype: int
        """
        return self._vehicle_capacity

    @vehicle_capacity.setter
    def vehicle_capacity(self, vehicle_capacity: int):
        """Sets the vehicle_capacity of this InlineResponse200.


        :param vehicle_capacity: The vehicle_capacity of this InlineResponse200.
        :type vehicle_capacity: int
        """

        self._vehicle_capacity = vehicle_capacity
