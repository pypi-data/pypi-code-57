from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import AssetTrade, FundTrade, FundPosition, FundWeight
from ...data.struct import AssetTradeParam, FundTradeParam
from . import Helper
import numpy as np

class AssetTrader(Helper):

    def __init__(self, asset_param: AssetTradeParam=None):
        self.asset_param = asset_param or AssetTradeParam()

    def calc_asset_trade(self, dt, 
                               cur_position: AssetPosition, 
                               cur_price: AssetPrice, 
                               target_allocation: AssetWeight):
        cur_mv = AssetValue(prices=cur_price, positions=cur_position)
        tot_mv = cur_mv.sum()

        trades = []
        launch_trade = False
        for index_id, target_weight in target_allocation.__dict__.items():
            if index_id != 'cash':
                target_amt = tot_mv * target_weight
                p = cur_price.__dict__[index_id]
                cur_amt = cur_mv.__dict__[index_id]
                if abs(target_amt - cur_amt) > tot_mv * self.asset_param.MinCountAmtDiff:
                    amount = abs(target_amt - cur_amt)
                    is_buy = target_amt > cur_amt
                    if is_buy:
                        trades.append(AssetTrade(
                            index_id=index_id, 
                            mark_price=p, 
                            amount=amount, 
                            is_buy=is_buy,
                            submit_date=dt
                        ))
                    else:
                        trades.append(AssetTrade(
                            index_id=index_id, 
                            mark_price=p, 
                            volume=amount/p, 
                            is_buy=is_buy,
                            submit_date=dt
                        ))
                launch_trade = launch_trade or abs(target_amt - cur_amt) > tot_mv * self.asset_param.MinActionAmtDiff

        if not launch_trade:
            return cur_position, None
        else:
            trades.sort(key=lambda x: x.is_buy)       
            new_position = cur_position.copy()
            for trd in trades:
                new_position.update(trd)
            return new_position, trades

    def finalize_trade(self, dt, trades: list, 
                            t1_price: AssetPrice, 
                            bt_position: AssetPosition):
        pendings = []
        traded_list = []
        if trades is None or len(trades) == 0:
            return pendings, traded_list
        # TODO: if some trades needs more time
        for trd in trades:
            # TODO: commision calculate
            #trd.commission = ?
            # update position
            trd.trade_price = t1_price.__dict__[trd.index_id]
            trd.volume = trd.volume if trd.volume else (trd.amount / trd.trade_price)
            trd.trade_date = dt
            if not trd.is_buy:
                if not(bt_position.__dict__[trd.index_id] - trd.volume > -1e-8):
                    print(f'trade volume exceeds, adjusted to pos (index_id){trd.index_id} (vol){trd.volume} (is_buy){trd.is_buy} (pos){bt_position.__dict__[trd.index_id]}')
                    trd.volume = bt_position.__dict__[trd.index_id]
                    trd.amount = trd.volume * trd.trade_price
            if self.asset_param.EnableCommission:
                amount = trd.amount if trd.amount else trd.volume * trd.trade_price
                trd.commission = amount * (self.asset_param.PurchaseDiscount * self.asset_param.AssetPurchaseRate[trd.index_id] if trd.is_buy 
                                                else self.asset_param.RedeemDiscount * self.asset_param.AssetRedeemRate[trd.index_id])
            bt_position.update(trd)
            traded_list.append(trd)
        return pendings, traded_list

class FundTrader(AssetTrader):

    def __init__(self, asset_param: AssetTradeParam=None, fund_param: FundTradeParam=None):
        AssetTrader.__init__(self, asset_param=asset_param)
        self.fund_param = fund_param or FundTradeParam()

    def calc_fund_trade(self, dt, fund_weight: FundWeight, cur_fund_position: FundPosition, 
                            cur_fund_nav: dict, 
                            fund_purchase_fees: dict,
                            fund_redeem_fees: dict) -> list:
        new_fund_position = cur_fund_position.copy()
        fund_trades = []
        # return trade list
        fund_tot_mv, cur_fund_wgts = cur_fund_position.calc_mv_n_w(fund_navs=cur_fund_nav)
        all_funds = {}
        # prepare fund candidates and its index_id
        for fund_id, fund_wgt_item in fund_weight.funds.items():
            all_funds[fund_id] = fund_wgt_item.index_id
        for fund_id, fund_pos_item in cur_fund_position.funds.items():
            all_funds[fund_id] = fund_pos_item.index_id
        # calc trade
        for fund_id, index_id in all_funds.items():
            target_fund_amt = fund_weight.get_wgt(fund_id) * fund_tot_mv
            cur_fund_volume = cur_fund_position.get_volume(fund_id) or 0
            p = cur_fund_nav[fund_id]
            cur_fund_amt = cur_fund_volume * p

            if abs(target_fund_amt - cur_fund_amt) > fund_tot_mv * self.fund_param.MinCountAmtDiff or (target_fund_amt == 0 and cur_fund_amt > 0):
                # TODO: commision and 如果是清某一只基金的逻辑，清空可以执行
                is_buy = target_fund_amt > cur_fund_amt
                if is_buy:
                    _trade = FundTrade(
                        fund_id=fund_id,
                        index_id=index_id, 
                        mark_price=p, 
                        amount=abs(target_fund_amt - cur_fund_amt),
                        is_buy=is_buy,
                        submit_date=dt
                    )
                else:
                    _trade = FundTrade(
                        fund_id=fund_id,
                        index_id=index_id, 
                        mark_price=p, 
                        volume=abs(target_fund_amt - cur_fund_amt)/p,
                        is_buy=is_buy,
                        submit_date=dt
                    )
                fund_trades.append(_trade)
                #print(f'(fund){fund_id} (p){p} (amt0){cur_fund_amt} (amt1){target_fund_amt} (idx){index_id} (amt){abs(target_fund_amt - cur_fund_amt)} (direc) {target_fund_amt > cur_fund_amt} ')

        fund_trades.sort(key=lambda x: x.is_buy)
        for _trade in fund_trades:
            new_fund_position.update(_trade)
        return new_fund_position, fund_trades

    def finalize_trade(self, dt, trades: list, 
                            t1_price: AssetPrice, 
                            bt_position: AssetPosition,
                            cur_fund_position: FundPosition, 
                            cur_fund_nav: dict,
                            cur_fund_unit_nav: dict,
                            fund_purchase_fees: dict,
                            fund_redeem_fees: dict):

        if trades is None or len(trades) == 0:
            return [], []
        
        pendings = []
        traded_list = []
        # TODO: if some trades needs more time
        for trd in trades:
            trd.trade_price = cur_fund_nav[trd.fund_id]
            trd.fund_unit_nav = cur_fund_unit_nav[trd.fund_id]
            trd.volume = trd.volume if trd.volume else (trd.amount / trd.trade_price)
            trd.amount = trd.amount if trd.amount else (trd.volume * trd.trade_price)
            trd.fund_unit_volume = trd.amount / trd.fund_unit_nav
            trd.trade_date = dt
            if not trd.is_buy:
                cur_vol = cur_fund_position.get_volume(trd.fund_id)
                if not((cur_vol or 0) - trd.volume > -1e-8):
                    print(f'trade volume exceeds, adjusted to pos (fund_id){trd.fund_id} (vol){trd.volume} (is_buy){trd.is_buy} (pos){cur_vol}')
                    assert cur_vol is not None, 'sell fund with no current position!'
                    trd.volume = cur_vol
                    trd.amount = trd.volume * trd.trade_price
            if self.fund_param.EnableCommission:
                trd.commission = trd.amount * (self.fund_param.PurchaseDiscount * fund_purchase_fees[trd.fund_id] if trd.is_buy 
                                            else self.fund_param.RedeemDiscount * fund_redeem_fees[trd.fund_id])
                if np.isnan(trd.commission):
                    trd.commission = 0
                #if not np.isnan(trd.commission), f'fund_id {trd.fund_id} fee data not avaiable'
            
            trade_status = cur_fund_position.update(trd)
            if trade_status:
                traded_list.append(trd)
            else:
                print(f'trade failed alert : {trd}')
        # get cur asset weight from fund weight
        cur_mv, cur_fund_weight = cur_fund_position.calc_mv_n_w(cur_fund_nav)
        fund_index_dic = {}
        for fund_id, fund_pos_item in cur_fund_position.funds.items():
            fund_index_dic[fund_id] = fund_pos_item.index_id
        asset_wgt = { _ : 0 for _ in set(fund_index_dic.values())}
        for fund_id, wgt_i in cur_fund_weight.items():
            index_id = fund_index_dic[fund_id]
            asset_wgt[index_id] += wgt_i
        # set index position:
        for index_id in asset_wgt:
            asset_p = t1_price.__dict__[index_id]
            amount = cur_mv * asset_wgt[index_id]    
            bt_position.__dict__[index_id] = amount / asset_p
        # fund cash -> asset cash
        bt_position.cash = cur_fund_position.cash
        return pendings, traded_list
