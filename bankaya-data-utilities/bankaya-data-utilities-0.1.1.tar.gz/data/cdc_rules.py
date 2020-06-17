"""
Rules for feature engineering of Circulo de Credito data (FICO scored version):
-------------------------------------------------------------------------------

> Main categories of the file:
- Persona
- Scores
- Empleo
- Consultas
- Domicilios
- Creditos
"""

# Persona specs:
residence = {
	0: "na",
	1: "propietarry",
	2: "rent",
	3: "family",
	4: "mortage",
	5: "na"
}

# Civil state specs
civilstate = {
	"N": "na",
	"D": "divorced",
	"L": "partner",
	"C": "married",
	"S": "single",
	"V": "widow",
	"E": "separated"
}


# `Clave de observacion` nomenclature
acc_status = {
	"AD": "dealed",
	"CA": "ok",
	"CC": "closed",
	"CD": "dealed",
	"CL": "ok",
	"CO": "dispute",
	"CP": "dealed",
	"CT": "dealed",
	"CV": "dealed",
	"FD": "fraud",
	"FN": "closed",
	"FP": "dealed",
	"FR": "expired",
	"GP": "expired",
	"IA": "closed",
	"IM": "delayed",
	"IS": "delayed",
	"LC": "dealed",
	"LG": "discount",
	"LO": "expired",
	"LS": "losted",
	"NA": "dealed",
	"NV": "dealed",
	"PC": "expired",
	"PD": "discount",
	"PE": "discount",
	"PI": "discount",
	"PR": "discount",
	"RA": "discount",
	"RI": "closed",
	"RF": "ok"
}


acc_status_vals = {
	"ok": 0,
	"dealed": 1,
	"closed": 1,
	"discount": 1,
	"dispute": 2,
	"delayed": 3,
	"expired": 4,
	"fraud": 6
}


# `Tipo de cuenta` nomenclature
acc_types = {
	"F": "fijos",
	"H": "mortage",
	"Q": "shorttrm",
	"A": "habilt",
	"P": "prend",
	"L": "nolim"
}