import logging
import pathlib

import numpy as np
import pandas as pd
import pytest
import yaml

import fiddler as fdl

LOG = logging.getLogger(__name__)


class TestUtils:
    def test_try_series_retype(self):
        series = pd.Series([1, 2, 3], dtype='float')
        LOG.info('Recasting floating point array of ints to int.')
        series = fdl.utils._try_series_retype(series, 'int')
        assert series.dtype == 'int'

        series = pd.Series([1, 2, None])
        LOG.info('Recasting floating point array of nullable ints to int.')
        series = fdl.utils._try_series_retype(series, 'int')
        assert series.dtype == 'float'

    def test_df_from_json_rows(self):
        """Tests the following:
            1. Column order in JSON different from in DatasetInfo
            2. Nullable integer values
            3. Categorical values not in possible values

        """
        dataset_info = fdl.DatasetInfo(
            display_name='test_dataset',
            columns=[
                fdl.Column('int_col', fdl.DataType.INTEGER),
                fdl.Column('nullable_int_col', fdl.DataType.INTEGER),
                fdl.Column('categorical_col',
                           fdl.DataType.CATEGORY,
                           possible_values=['a', 'b', 'c']),
            ])
        json_rows = [
            {
                'nullable_int_col': 1,
                'categorical_col': 'a',
                'int_col': 1
            },
            {
                'nullable_int_col': 2,
                'categorical_col': 'b',
                'int_col': 1
            },
            {
                'nullable_int_col': None,
                'categorical_col': 'xyz',
                'int_col': 2
            },
            {
                'nullable_int_col': 3,
                'categorical_col': 'c',
                'int_col': 3
            },
            {
                'nullable_int_col': None,
                'categorical_col': 'a',
                'int_col': 3
            },
        ]
        df = fdl.utils.df_from_json_rows(json_rows, dataset_info)
        # check column ordering follows from DatasetInfo
        assert df.columns.tolist() == [
            'int_col', 'nullable_int_col', 'categorical_col'
        ]
        # the fact that no errors were raised means we didn't fail on nullable
        # integers, but let's double check that things worked out nicely
        assert df['nullable_int_col'].dtype == 'float'
        assert not np.isnan(df.loc[0, 'nullable_int_col'])
        assert np.isnan(df.loc[2, 'nullable_int_col'])
        # check categories worked well
        assert df['categorical_col'].dtype == 'category'
        assert df['categorical_col'].cat.categories.tolist() == \
            dataset_info['categorical_col'].possible_values
        assert np.isnan(df.loc[2, 'categorical_col'])


class TestDataIntegrity:
    @classmethod
    def setup_class(cls):
        titanic_path = pathlib.Path(__file__).parents[1].joinpath(
            'examples', 'starterorg', 'datasets', 'titanic')
        with titanic_path.joinpath('titanic.yaml').open('r') as f:
            info = fdl.DatasetInfo.from_dict(
                yaml.load(f, Loader=yaml.SafeLoader))

        df = pd.read_csv(titanic_path.joinpath('train.csv'))
        df = fdl.utils.df_from_json_rows(df.to_dict(orient='records'), info)
        cls.df = df
        cls.info = info

    def test_range(self):
        df_low_age = TestDataIntegrity.df[TestDataIntegrity.df['age'] < 2]
        TestDataIntegrity.info['age'].value_range_min = 1
        events = df_low_age.to_dict(orient='records')
        ev = events[0]
        assert TestDataIntegrity.info.get_event_integrity(ev) == (
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, True), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False))

        TestDataIntegrity.info['embarked'].possible_values.remove('C')
        events = TestDataIntegrity.df.head(10).to_dict(orient='records')
        ev_fine = events[0]
        ev_broken = events[9]

        assert TestDataIntegrity.info.get_event_integrity(ev_fine) == (
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False))

        assert TestDataIntegrity.info.get_event_integrity(ev_broken) == (
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, True), (False, False, False),
            (False, False, False), (False, False, False))

    def test_nullable(self):
        df_nulled = TestDataIntegrity.df.copy()
        df_nulled['parch'] = np.nan
        assert TestDataIntegrity.info.get_event_integrity(
            TestDataIntegrity.df.to_dict('records')[0]) == (
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False),
                (False, False, False), (False, False, False))

    def test_type(self):
        ev = TestDataIntegrity.df.to_dict('records')[0]
        ev['survived'] = True
        ev['name'] = 17.2
        ev['sex'] = 1
        ev['age'] = 'hello'
        assert TestDataIntegrity.info.get_event_integrity(ev) == (
            (False, False, False), (False, False, False),
            (False, True, False), (False, True, False),
            (False, True, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False),
            (False, False, False), (False, False, False))

    def test_event_fields(self):
        ev = TestDataIntegrity.df.to_dict('records')[0]
        ev['my_prediction'] = 0.9997
        assert len(TestDataIntegrity.info.get_event_integrity(ev)) == 14

        ev.pop('age')
        with pytest.raises(ValueError):
            TestDataIntegrity.info.get_event_integrity(ev)
