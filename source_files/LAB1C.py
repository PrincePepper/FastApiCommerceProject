import datetime
import time
from typing import Dict, Any, Optional

import requests
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.schemas import RoadPointCreate, RouteCreate, CargoTypeCreate
from app.schemas.builk_works import BuilkWorkCreate

type_time = ["default", "hour", "our"]


class SOURCE:
    def __init__(self, type_time="default"):
        self.id = "349ec6f2-6b44-4144-bb2c-207dc5f16743"
        self.name = "1CLAB"
        self.address = "где то находиться"
        self.properties = {"login": "АСУ"}
        self.__url = "http://10.0.0.44/dkhsclad/hs/ecc/blkwrk"
        self.__type_time = type_time

    def get_about_me(self):
        return {"id": self.id,
                "name": self.name,
                "address": self.address,
                "properties": self.properties}

    def get_properties(self):
        return self.properties

    def set_properties(self, properties: Dict):
        self.properties = properties

    def time_upload(self):
        list = [""]
        return self.__type_time, list

    def __request(self, begin_date, end_date):
        query_params = {"BeginDate": begin_date, "EndDate": end_date}
        try:
            response = requests.get(self.__url, params=query_params, timeout=10,
                                    auth=(self.properties['login'], ''))
        except Exception as e:
            return {"detail": f"Не работает API, обратитесь к разработчику: {e}"}
        else:
            print("запрос обработан")
        if response.status_code != 200:
            return {"detail": "не верный запрос"}

        result_response = response.json()
        return result_response

    def get_api(self,
                begin_date: str,
                end_date: str,
                db: Session
                ) -> Any:
        result_response = self.__request(begin_date, end_date)

        for i in result_response['road_points']:
            road_point_in = RoadPointCreate(name=i['road_point'], id=i['guid'])
            road_point_res = crud.road_point.get_by_id(db, id=road_point_in.id)
            if not road_point_res:
                crud.road_point.create(db, obj_in=road_point_in)
        for i in result_response['routes']:
            route_in = RouteCreate(name=i['route'], id=i['guid'], from_id=i['from_id'], to_id=i['to_id'])
            route_res = crud.route.get_by_id(db, id=route_in.id)
            if not route_res:
                crud.route.create(db, obj_in=route_in)
        for i in result_response['cargo_types']:
            cargo_types_in = CargoTypeCreate(name=i['cargo_type'], id=i['guid'])
            cargo_types_res = crud.cargo_types.get_by_id(db, id=cargo_types_in.id)
            if not cargo_types_res:
                crud.cargo_types.create(db, obj_in=cargo_types_in)

        crud.builk_works.deleteAll(db)
        builk_works_in = None
        for i in result_response['builk_works']:
            builk_works_in = BuilkWorkCreate(
                data_time=int(time.mktime(datetime.datetime.strptime(i['date_time'], "%Y-%m-%dT%H:%M:%S").timetuple())),
                cargo_type_id=i['cargo_type_id'],
                route_id=i['route_id'],
                weight=i['weight'],
                volume=i['volume'],
                amount=i['amount'],
                source_id=self.id)

            crud.builk_works.create(db, obj_in=builk_works_in)
        return {"detail": "ok"}


class SourceUpdateProperties(BaseModel):
    login: Optional[str] = None


lab_1c = SOURCE()
