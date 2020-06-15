# -*- coding: utf-8 -*-
#
# Copyright 2019 Ricequant, Inc
#
# * Commercial Usage: please contact public@ricequant.com
# * Non-Commercial Usage:
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from enum import Enum


class CustomEnum(Enum):
    def __repr__(self):
        return "%s.%s" % (
            self.__class__.__name__, self._name_)



class STOP_PROFIT_LOSS_ORDER_STATUS(CustomEnum):

    WAITING_TARGET_ORDER_FILLED = "WAITING_TARGET_ORDER_FILLED" #目标委托已经全部成交了
    ACTIVE = "ACTIVE"# 表示止盈止损指令已经开始盯着行情，撮合中了。

    # 表示止盈止损单的条件到达后，平仓委托发出去了。即比如你回测20块，止损，那么这个状态表示，你回调20块达到了，并且平仓委托已经下出去了。
    ORDER_SENDED="ORDER_SENDED"

    #这种描述，止盈止损单，挂着。然后没触发，但是由于平仓信号，导致改止盈止损单对应的持仓被平仓了。那么止盈止损单当然是失效了。
    ORDER_CANCELED = "ORDER_CANCELED"

    #这种描述跟踪止损单。表示处于追踪状态，此时并不是随时可以下单的，追踪状态满足后，会开启回落下单状态（active）此时会随时会下单，所以叫做active状态
    TRAILING="TRAILING"


class ORDER_TYPE(CustomEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

# noinspection PyPep8Naming
class ORDER_STATUS(CustomEnum):
    PENDING_NEW = "PENDING_NEW"
    ACTIVE = "ACTIVE"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    PENDING_CANCEL = "PENDING_CANCEL"
    CANCELLED = "CANCELLED"

class POSITION_SIDE(CustomEnum):
    UN_KNOWN = "UN_KNOWN"
    LONG = "LONG"
    SHORT = "SHORT"
