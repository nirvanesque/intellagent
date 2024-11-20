# Copyright Sierra
from langchain.tools import StructuredTool
import json
from typing import Any, Dict


class GetReservationDetails():
    @staticmethod
    def invoke(data: Dict[str, Any], reservation_id: str) -> str:
        reservations = data["reservations"].set_index('reservation_id', drop=False).to_dict(orient='index')
        if reservation_id in reservations:
            return json.dumps(reservations[reservation_id])
        return "Error: reservation not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reservation_details",
                "description": "Get the details of a reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation id, such as '8JX2WO'.",
                        },
                    },
                    "required": ["reservation_id"],
                },
            },
        }

get_reservation_details_schema = GetReservationDetails.get_info()
get_reservation_details = StructuredTool.from_function(
        func=GetReservationDetails.invoke,
        name=get_reservation_details_schema['function']["name"],
        description=get_reservation_details_schema['function']["description"],
    )
