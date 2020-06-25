import json
import numpy as np
import datetime as dt

from .cdc_rules import civilstate, residence


class CDCParser:
    def __init__(self, raw_data):
        # str raw_data to json dict data
        self.dict_data = json.loads(raw_data)
        # getting fields
        self.features = {}
        self.persona()
        self.scores()
        self.empleos()
        self.consultas()
        self.credits()

    def dt_from_str(self, strng):
        return dt.datetime.strptime(strng, '%Y-%m-%d')

    # parsers
    def persona(self):
        data = self.dict_data["persona"]
        self.features["lastname1"] = data["apellidoPaterno"]
        self.features["lastname2"] = data["apellidoMaterno"]
        self.features["name"] = data["nombres"]
        self.features["fullname"] = " ".join([data["nombres"], data["apellidoPaterno"], data["apellidoMaterno"]])
        self.features["alive"] = 0 if "fechaDefuncion" in data and data["fechaDefuncion"] != "9999-01-01" else 1
        bdt = self.dt_from_str(data["fechaNacimiento"])
        self.features["age"] = (dt.datetime.now() - bdt) / 365
        self.features["mbirth"] = bdt.month
        self.features["dependents"] = data["numeroDependientes"]
        self.features["residence"] = residence[data.get("residencia", 0)]
        self.features["civilstate"] = civilstate[data.get("estadoCivil", "N")]
        self.features["rfc"] = data["RFC"]
        self.features["curp"] = data["CURP"]
        self.features["nationaity"] = data["nacionalidad"] if "nacionalidad" in data else None
        self.features["socialsecnum"] = data["numeroSeguridadSocial"] if "numeroSeguridadSocial" in data else None
        self.features["gender"] = data["sexo"] if "sexo" in data else None

    def scores(self):
        data = self.dict_data["scores"]
        self.features["fico"] = -1
        self.features["ficoreasons"] = ""
        for sc in data:
            if sc["nombreScore"] != "FICO": continue
            self.features["fico"] = data[0]["valor"]
            self.features["ficoreasons"] = ",".join(str(v) for v in data[0]["razones"])
            break

    def empleos(self):
        data = self.dict_data["empleos"]
        self.features["emp_num"] = len(data)
        self.features["emp_states"] = [v["estado"] if "estado" in v else None for v in data]
        self.features["emp_salaries"] = [v["salarioMensual"] for v in data]
        self.features["emp_postc"] = [v["CP"] for v in data]
        self.features["emp_positions"] = [v["puesto"].lower() if "puesto" in v else None for v in data]
        self.features["emp_durations"] = [
            (self.dt_from_str(v["fechaUltimoDiaEmpleo"]) - self.dt_from_str(v["fechaContratacion"])).days \
            for v in data]

    def consultas(self):
        data = self.dict_data["consultas"]
        self.features["cons_num"] = len(data)
        self.features["cons_dates"] = sorted([self.dt_from_str(v["fechaConsulta"]) for v in data])
        self.features["cons_difftimes"] = np.diff(self.features["cons_dates"])
        self.features["cons_services"] = [v["servicios"] if "servicios" in v else None for v in data]
        self.features["cons_responsabilities"] = [v["tipoResponsabilidad"] if "ipoResponsabilidad" in v else None for v in data]
        self.features["cons_creditype"] = [v["tipoCredito"] for v in data]
        self.features["cons_amount"] = [v["importeCredito"] for v in data]

    def credits(self):
        data = self.dict_data['creditos']
        self.features["creds_num"] = len(data)
        self.features["creds_debt_amts"] = [v["montoPagar"] for v in data]
        self.features["creds_pay_amts"] = [v["montoUltimoPago"] if "montoUltimoPago" in v else None for v in data]
        self.features["creds_pay_delay"] = [v["saldoVencidoPeorAtraso"] for v in data]
        self.features["creds_pay_done"] = [v["numeroPagos"] for v in data] if "numeroPagos" in data else None
        self.features["creds_pay_report"] = [v["totalPagosReportados"] for v in data] if "totalPagosReportados" in data else None
        self.features["creds_pay_exp"] = [v["numeroPagosVencidos"] for v in data]
        self.features["creds_pay_frec"] = [v["frecuenciaPagos"] for v in data]
        self.features["creds_pay_str"] = [
            v["historicoPagos"].replace(" ", "").replace("-", "").replace("0", "").replace("V", "0") \
            if "historicoPagos" in v else "0" \
            for v in data]
        self.features["creds_debt_amt"] = [v["saldoActual"] for v in data]
        self.features["creds_debt_exp"] = [v["saldoVencido"] for v in data]
        self.features["creds_curr_delay"] = [int(v["pagoActual"].replace("V", "0")) for v in data if v != "-"]
        self.features["creds_total_delay"] = np.sum(
            [np.sum([int(w) for w in v.split()]) for v in self.features["creds_pay_str"]])
        self.features["creds_total_debt"] = np.sum([v for v in self.features["creds_debt_amt"]])
        self.features["creds_exp_debt"] = np.sum([v for v in self.features["creds_debt_exp"]])
        self.features["creds_acc_type"] = [v["tipoCuenta"] for v in data]
        self.features["creds_gen_delays"] = [v["peorAtraso"] for v in data] if "peorAtraso" in data else None
        self.features["creds_pago_delta"] = [
            self.dt_from_str(v["fechaUltimoPago"]) - self.dt_from_str(v["fechaAperturaCuenta"]) \
            if "fechaUltimoPago" in v and "fechaAperturaCuenta" in v else None \
            for v in data]
        self.features["creds_compra_delta"] = [
            self.dt_from_str(v["fechaUltimaCompra"]) - self.dt_from_str(v["fechaAperturaCuenta"]) \
            if "fechaUltimaCompra" in v and "fechaAperturaCuenta" in v else None \
            for v in data]

    def get_features(self):
        return self.features
