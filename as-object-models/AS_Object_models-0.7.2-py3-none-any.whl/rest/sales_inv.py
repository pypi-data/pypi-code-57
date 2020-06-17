from .. import GrowWeek
from .. import ItemReserve
from .. import DataNumberLookup

class SalesInventoryAPI(object):

    def __init__(self, logger):
        self.logger = logger

    def createReserveAPI(self,reserveDate, customer_id, location_id, product_id, reserved):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        newReserve = gw.create_reserve(customer_id,location_id, product_id,reserved,reserveDate)
        summ = gw.getSummary()
        return summ.add_reserve(newReserve)

    def updateReserveAPI(self,reserve_id, customer_id, location_id, product_id, reserved, reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        updReserve = gw.update_reserve(reserve_id, customer_id, location_id, product_id, reserved, reserveDate)
        summ = gw.getSummary()
        return summ.update_reserve(updReserve)

    def deleteReserveAPI(self,reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        if ir.exists:
            gw = ir._growWeekParent
            summ = gw.getSummary()
            summ.delete_reserve(ir)
            ir.delete_resp()
            return {"status":"success"}
        else:
            path = DataNumberLookup.get_path_for_dnl(reserve_id)
            docRef = ir._fsClient.document(path)
            gw_id = docRef.parent.parent.id
            gw = GrowWeek.getGrowWeekInstance(gw_id)
            summ = gw.getSummary()
            newSumm = [x for x in summ.summary if x.get('id','') != reserve_id]
            summ.summary = newSumm
            summ.update_ndb()
            return {"status":"success"}

    def getAllReservesAPI(self,reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        irList = gw.reserves
        return [resv.get_dict() for resv in irList]

    def getSummReservesAPI(self,reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        irList = gw.getSummary().summary
        return irList

    def getReserveAPI(self,reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.get_dict()