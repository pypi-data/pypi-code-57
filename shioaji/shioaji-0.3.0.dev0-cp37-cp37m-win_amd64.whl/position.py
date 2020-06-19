from shioaji.base import BaseModel
from shioaji.contracts import Contract
from shioaji.constant import Action, StockOrderCond
from shioaji.account import Account
from shioaji.data import BaseMapping
import typing


class Position(BaseMapping):
    code: str
    direction: Action
    quantity: int
    price: float
    pnl: float
    yd_quantity: int
    cond: StockOrderCond = StockOrderCond.Cash


class ProfitLoss(BaseMapping):
    code: str
    seqno: str
    quantity: int
    price: float
    pnl: float
    pr_ratio: float
    cond: StockOrderCond = StockOrderCond.Cash
    date: str


class Settlement(BaseMapping):
    t_money: float
    t1_money: float
    t2_money: float
    t_day: str
    t1_day: str
    t2_day: str
