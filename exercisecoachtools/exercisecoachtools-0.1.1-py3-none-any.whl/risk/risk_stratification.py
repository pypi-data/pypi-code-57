from validation.value_validation import ValidateValue

def risk_classification(patient):
    classification = RiskFactorAssessment(patient).result_risk_classification()
    return classification

def total_risk_factors(patient):
    total = RiskFactorAssessment(patient).net_risk_factors()
    return total

class Patient(object):
    def __init__(self, sex, age, smoker, sedentary, bmi, waist_girth, male_family_death_before_55, female_family_death_before_65, systolic, diastolic, hypertensive, ldl, hdl, using_lipid_lowering_medication, cholesterol, fasting_glucose, oral_glucose_tolerance):
        self._sex = ValidateValue(sex).valueIsMaleFemale()
        self._age = ValidateValue(age).valueIsPositiveInteger()
        self._smoker = ValidateValue(smoker).valueIsYesNo()
        self._sedentary = ValidateValue(sedentary).valueIsYesNo()
        self._bmi = ValidateValue(bmi).valueIsPositiveInteger()
        self._waist_girth = ValidateValue(waist_girth).valueIsPositiveInteger()
        self._male_family_death_before_55 = ValidateValue(male_family_death_before_55).valueIsYesNo()
        self._female_family_death_before_65 = ValidateValue(female_family_death_before_65).valueIsYesNo()
        self._systolic = ValidateValue(systolic).valueIsPositiveInteger()
        self._diastolic = ValidateValue(diastolic).valueIsPositiveInteger()
        self._hypertensive = ValidateValue(hypertensive).valueIsYesNo()
        self._ldl = ValidateValue(ldl).valueIsPositiveInteger()
        self._hdl = ValidateValue(hdl).valueIsPositiveInteger()
        self._using_lipid_lowering_medication = ValidateValue(using_lipid_lowering_medication).valueIsYesNo()
        self._cholesterol = ValidateValue(cholesterol).valueIsPositiveInteger()
        self._fasting_glucose = ValidateValue(fasting_glucose).valueIsPositiveInteger()
        self._oral_glucose_tolerance = ValidateValue(oral_glucose_tolerance).valueIsPositiveInteger()


class RiskFactorAssessment(object):
    def __init__(self, patient):
        self._patient = patient

    def result_risk_classification(self):
        classification = RiskFactorAssessmentClassification().patient_risk_classification(self.net_risk_factors())
        return classification

    def net_risk_factors(self):
        total = self._get_risk_factor_count() - self._get_negative_risk_factor_count()
        return total

    def _get_risk_factor_count(self):
        _count_risk_factors = [
            self._is_age_risk(),
            self._is_obesity_risk(),
            self._patient._smoker,
            self._patient._sedentary,
            self._is_familial_risk(),
            self._is_systolic_risk(),
            self._is_diastolic_risk(),
            self._patient._hypertensive,
            self._is_dyslipidemia_risk(),
            self._is_pre_diabetes_risk()
            ]
        return _count_risk_factors.count(True)

    def _get_negative_risk_factor_count(self):
        _count_negative_risk_factor = [ self._is_hdl_negative_risk() ]
        return _count_negative_risk_factor.count(True)

    def _is_obesity_risk(self):
        if self._patient._bmi and self._patient._waist_girth == 0:
            return False
        elif self._patient._bmi > 30:
            return True
        elif self._patient._waist_girth > 40 and self._patient._sex == 'male' or self._patient._waist_girth > 35 and self._patient._sex == 'female':
            return True
        else:
            return False

    def _is_age_risk(self):
        if (self._patient._sex == "male" and self._patient._age >= 45) or (self._patient._sex == "female" and self._patient._age >=55):
            return True
        else:
            return False

    def _is_familial_risk(self):
        if self._patient._male_family_death_before_55 == True or self._patient._female_family_death_before_65 == True:
            return True
        else:
            return False

    def _is_systolic_risk(self):
        if self._patient._systolic >= 120:
            return True
        else:
            return False

    def _is_diastolic_risk(self):
        if self._patient._diastolic >= 80:
            return True
        else:
            return False

    def _is_dyslipidemia_risk(self):
        if self._patient._ldl > 130 or self._patient._hdl < 40 or self._patient._cholesterol > 200:
            return True
        else:
            return False

    def _is_pre_diabetes_risk(self):
        if self._patient._fasting_glucose >= 100 and self._patient._fasting_glucose <= 126 or self._patient._oral_glucose_tolerance >= 140 and self._patient._oral_glucose_tolerance < 200:
            return True
        else:
            return False

    def _is_hdl_negative_risk(self):
        if self._patient._hdl > 60:
            return True
        else:
            return False

class RiskFactorAssessmentClassification(object):
    def __init__(self):
        pass

    def patient_risk_classification(self, value):
        if value <= 1:
            return self._low_risk_category(value)

        if value == 2:
            return self._moderate_risk_category(value)

        if value >  2:
            return self._high_risk_category(value)

    def _low_risk_category(self, value):
        return("Your risk total is %s. You are at a low risk for cardiovascular disease. Medical check-up no necessary for participation in physical activity." % value)

    def _moderate_risk_category(self, value):
        return("Your risk total is %s. You are at a moderate risk for cardiovascular disease. Medical check-up recommended for participation in vigorous physical activity." % value)

    def _high_risk_category(self, value):
        return("Your risk total is %s. You are at a high risk for cardiovascular disease. Medical check-up highly recommended before any physical activity." % value)
