from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

import attr

from betfairstreamer.models.betfair_api import BetfairOrder, OrderStatus, OrderType, PersistenceType, Side
from betfairstreamer.utils import parse_utc_timestamp


@attr.s(slots=True, auto_attribs=True)
class Order:
    market_id: str
    selection_id: int
    bet_id: str
    bsp_liability: float
    status: OrderStatus
    side: Side
    persistence_type: PersistenceType
    order_type: OrderType
    price: float
    regulator_code: str
    size: float
    placed_date: Optional[datetime]
    matched_date: Optional[datetime]
    lapsed_date: Optional[datetime]
    regulator_auth_code: Optional[str]
    lapse_status_reason_code: Optional[str]
    handicap: Optional[float]
    size_cancelled: float
    size_voided: float
    size_lapsed: float
    average_price_matched: float
    size_matched: float
    size_remaining: float
    customer_strategy_reference: Optional[str]
    customer_order_reference: Optional[str]

    @classmethod
    def from_stream(cls, market_id: str, selection_id: int, order: BetfairOrder) -> Order:
        return cls(
            market_id=market_id,
            selection_id=selection_id,
            side=Side[order["side"]],
            size_voided=order["sv"],
            persistence_type=PersistenceType[str(order.get("pt"))],
            order_type=OrderType[order["ot"]],
            lapse_status_reason_code=order.get("lsrc"),
            handicap=None,
            price=order["p"],
            size_cancelled=order["sc"],
            regulator_code=order["rc"],
            size=order["s"],
            placed_date=parse_utc_timestamp(order["pd"]),
            regulator_auth_code=order["rac"],
            matched_date=parse_utc_timestamp(order.get("md")),
            lapsed_date=parse_utc_timestamp(order.get("ld")),
            size_lapsed=order["sl"],
            average_price_matched=order.get("avp", 0),
            size_matched=order["sm"],
            bet_id=order["id"],
            bsp_liability=order.get("bsp", 0),
            customer_strategy_reference=order["rfs"],
            customer_order_reference=order["rfo"],
            status=OrderStatus[order["status"]],
            size_remaining=order["sr"],
        )

    def serialize(self) -> Dict[Any, Any]:
        out = {}
        for k, v in attr.asdict(self).items():

            if isinstance(v, Enum):
                v = v.value

            if isinstance(v, datetime):
                v = v.isoformat()

            camel_case_key = [word.title() for word in k.split("_")]
            camel_case_key[0] = camel_case_key[0].lower()
            out["".join(camel_case_key)] = v

        return out
