from ..embedding import DataframeEmbedding
from ..simple_types import SimpleTypePredictor, NameSurnameType
from random import randint, uniform, choice
import numpy as np
from tqdm.auto import trange, tqdm
import pandas as pd
from random_csv_generator import random_csv
from ..datasets import (
    load_nan, load_names, load_regions, load_countries, load_country_codes,
    load_municipalities, load_surnames, load_provinces_codes, load_caps,
    load_codice_fiscale, load_iva, load_strings, load_email, load_phone,
    load_date, load_address, load_biological_sex, load_boolean,
    load_document_types, load_plate, load_codice_catasto, load_tax
)


class SimpleDatasetGenerator:

    def __init__(self, verbose: bool = False, combinatorial_strings_number: int = 10000):
        self._verbose = verbose
        self._separators = NameSurnameType()._separators
        self._combinatorial_strings_number = combinatorial_strings_number
        self._datasets = self._load_types_datasets()
        self._embedding = DataframeEmbedding()

    def _load_types_datasets(self):
        integers = np.random.randint(0, 10000, size=10000)
        string_integers = integers.astype(str)
        float_integers = integers.astype(float)

        all_integers = integers.tolist() + string_integers.tolist() + \
            float_integers.tolist()

        floats = np.random.uniform(0, 10000, size=10000)
        string_floats = floats.astype(str)

        all_floats = floats.tolist() + string_floats.tolist() + all_integers

        years = np.random.randint(1990, 2030, size=1000)
        string_years = years.astype(str)
        float_years = years.astype(float)

        all_years = years.tolist() + string_years.tolist() + \
            float_years.tolist()

        names = load_names()
        surnames = load_surnames()
        self._nans = load_nan()

        datasets = {
            "ItalianFiscalCode": load_codice_fiscale(),
            "ItalianVAT": load_iva(),
            "CadastreCode": load_codice_catasto(),
            "Document": load_document_types(),
            "Tax": load_tax(),
            "Plate": load_plate(),
            "Address": load_address(),
            "ItalianZIPCode": load_caps(),
            "ProvinceCode": load_provinces_codes(),
            "Region": load_regions(),
            "Municipality": load_municipalities(),
            "Year": all_years,
            "Integer": all_integers,
            "Float": all_floats,
            "Country": load_countries(),
            "CountryCode": load_country_codes(),
            "Name": names,
            "NameSurname": [
                "{name}{sep}{surname}".format(
                    name=choice(names),
                    sep=choice(self._separators),
                    surname=choice(surnames)
                )
                for _ in range(10000)
            ],
            "SurnameName": [
                "{surname}{sep}{name}".format(
                    name=choice(names),
                    sep=choice(self._separators),
                    surname=choice(surnames)
                )
                for _ in range(10000)
            ],
            "Surname": surnames,
            "String": load_strings(),
            "EMail": load_email(),
            "PhoneNumber": load_phone(),
            "Date": load_date(),
            "BiologicalSex": load_biological_sex(),
            "Boolean": load_boolean()
        }

        columns = set(list(datasets.keys())) - \
            set(("Name", "Surname", "NameSurname", "SurnameName"))
        all_strings = sum([
            datasets[col]
            for col in columns
        ], [])
        separator = (", ", "; ", ". ", "-", "/")

        strings = [
            np.random.choice(all_strings, size=(
                self._combinatorial_strings_number, number))
            for number in (2, 3, 4, 5)
        ]

        datasets["String"] += [
            choice(separator).join(phrase)
            for phrases in tqdm(strings, desc="Building string dataset", disable=not self._verbose)
            for phrase in phrases
        ]

        return {
            key: np.array(value)
            for key, value in datasets.items()
        }

    def get_dataset(self, predictor: SimpleTypePredictor) -> np.ndarray:
        """Return dataset for given predictor."""
        if predictor.name == "NaN":
            return self._nans
        return self._datasets[predictor.name]

    def random_nan(self, df):
        return np.random.choice(self._nans, size=df.shape)

    def generate_simple_dataframe(
        self,
        nan_percentage: float = 0.2,
        error_percentage: float = 0.1,
        min_rows: int = 5,
        max_rows: int = 50,
        mix_codes: bool = True
    ):
        rows = randint(min_rows, max_rows)
        df = pd.DataFrame({
            key: np.random.choice(values, size=rows, replace=True)
            for key, values in self._datasets.items()
        })

        rnd = random_csv(rows)

        df["Name"] = rnd["name"]
        df["Surname"] = rnd["surname"]
        df["SurnameName"] = rnd["surname"].str.cat(
            rnd["name"], sep=choice(self._separators)
        )
        df["NameSurname"] = rnd["name"].str.cat(
            rnd["surname"], sep=choice(self._separators)
        )
        df["ItalianFiscalCode"] = rnd["codice_fiscale"]

        types = pd.DataFrame(
            np.tile(np.array(df.columns), (len(df), 1)),
            columns=df.columns,
            index=df.index
        )

        overlaps = {
            "Region": ["Name", "Surname", "Municipality", "Country"],
            "Municipality": ["Name", "Surname", "Region", "Country"],
            "Country": ["Name", "Surname", "Region", "Municipality"],
            "Integer": ["Float", "Year", "ItalianVAT", "ItalianZIPCode"],
            "Float": ["Integer", "Year", "ItalianVAT", "ItalianZIPCode"],
            "CountryCode": ["ProvinceCode"],
            "ProvinceCode": ["CountryCode"]
        }

        for column in df.columns:
            if column in ("String", "Name", "Surname", "Address"):
                continue

            datasets = list(self._datasets.keys())
            to_remove = [column]
            to_remove += overlaps.get(column, [])
            for remove in to_remove:
                if remove in datasets:
                    datasets.remove(remove)

            for i in df[column].index:
                if np.random.uniform(0, 1) < error_percentage:
                    df.loc[i, column] = choice(
                        self._datasets[choice(datasets)])
                    types.loc[i, column] = "Error"

        if mix_codes:
            for column_a, column_b in (
                ("ItalianFiscalCode", "ItalianVAT"),
                ("SurnameName", "NameSurname")
            ):
                if choice([True, False]):
                    mask = np.random.randint(
                        0, 2, size=df.shape[0], dtype=bool)
                    swap_column_a = df[column_a][mask].values
                    swap_column_b = df[column_b][mask].values
                    df.loc[mask, column_a] = swap_column_b
                    df.loc[mask, column_b] = swap_column_a
                    backup_fiscal_codes = types.loc[mask, column_a]
                    types.loc[mask, column_a] = types.loc[mask, column_b]
                    types.loc[mask, column_b] = backup_fiscal_codes
                    column_to_drop = choice([column_a, column_b])
                    df = df.drop(columns=column_to_drop)
                    types = types.drop(columns=column_to_drop)

        if nan_percentage > 0:
            mask = np.random.choice([False, True], size=df.shape, p=[
                nan_percentage, 1-nan_percentage])
            types[np.logical_not(mask)] = "NaN"
            df = df.where(mask, other=self.random_nan)
        return df, types

    def _build(self):
        df, types = self.generate_simple_dataframe()
        return self._embedding.transform(df, types)

    def build(self, number: int = 1000):
        """Creates and encodes a number of dataframe samples for training"""
        X, y = list(zip(*[
            self._build()
            for _ in trange(number, desc="Rendering dataset", disable=not self._verbose)
        ]))

        return np.vstack(X), np.concatenate(y)
