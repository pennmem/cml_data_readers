import os
import pytest
import pandas as pd
import numpy as np
import functools
from cmlreaders.readers import TextReader, CSVReader, ElectrodeCategoriesReader
from pkg_resources import resource_filename

datafile = functools.partial(resource_filename, 'cmlreaders.test.data')


class TestTextReader:

    @pytest.mark.parametrize("method", ['dataframe', 'recarray', 'dict'])
    @pytest.mark.parametrize("data_type", [
        "voxel_coordinates", "leads", "classifier_excluded_leads", "good_leads",
        "jacksheet", "area"])
    @pytest.mark.parametrize("subject,localization", [
        ('R1389J', '0'),
    ])
    def test_as_methods(self, method, data_type, subject, localization):
        file_path = datafile(data_type + ".txt")
        reader = TextReader(data_type, subject, localization,
                            file_path=file_path)
        expected_types = {
            'dataframe': pd.DataFrame,
            'recarray': np.recarray,
            'dict': list
        }
        method_name = "as_{}".format(method)
        callable_method = getattr(reader, method_name)
        data = callable_method()
        assert data is not None
        assert type(data) == expected_types[method]

    @pytest.mark.parametrize("method", ['json', 'csv'])
    @pytest.mark.parametrize("data_type", [
        "voxel_coordinates", "leads", "classifier_excluded_leads", "good_leads",
        "jacksheet", "area"])
    @pytest.mark.parametrize("subject,localization", [
        ('R1389J', '0'),
    ])
    def test_to_methods(self, method, data_type, subject, localization,
                        rhino_root):
        file_path = datafile(data_type + ".txt")
        reader = TextReader(data_type, subject, localization,
                            file_path=file_path, rootdir=rhino_root)

        # Save as specified format
        method_name = "to_{}".format(method)
        callable_method = getattr(reader, method_name)
        exp_output = datafile("output/" + data_type + "." + method)
        callable_method(exp_output)
        assert os.path.exists(exp_output)

        # Check that data can be reloaded
        re_reader = TextReader(data_type, subject, localization,
                               file_path=exp_output)
        reread_data = re_reader.as_dataframe()
        assert reread_data is not None


class TestCSVReader:

    @pytest.mark.parametrize("method", ["dataframe", "recarray", "dict"])
    @pytest.mark.parametrize("data_type", [
        'electrode_coordinates', 'prior_stim_results', 'target_selection_table'
    ])
    @pytest.mark.parametrize("subject,localization", [
        ('R1409D', '0'),
    ])
    def test_as_methods(self, method, data_type, subject, localization, rhino_root):
        file_path = datafile(data_type + ".csv")
        reader = CSVReader(data_type, subject, localization, experiment="FR1",
                           file_path=file_path)
        expected_types = {
            'dataframe': pd.DataFrame,
            'recarray': np.recarray,
            'dict': list
        }
        method_name = "as_{}".format(method)
        callable_method = getattr(reader, method_name)
        data = callable_method()
        assert data is not None
        assert type(data) == expected_types[method]

    @pytest.mark.parametrize("method", ['json', 'csv'])
    @pytest.mark.parametrize("data_type", [
        'electrode_coordinates', 'prior_stim_results', 'target_selection_table'
    ])
    @pytest.mark.parametrize("subject,localization", [
        ('R1409D', '0'),
    ])
    def test_to_methods(self, method, data_type, subject, localization,
                        rhino_root):
        # Load the test data
        file_path = datafile(data_type + ".csv")
        reader = CSVReader(data_type, subject, localization, experiment="FR1",
                           file_path=file_path, rootdir=rhino_root)

        # Save as specified format
        method_name = "to_{}".format(method)
        callable_method = getattr(reader, method_name)
        exp_output = datafile("output/" + data_type + "." + method)
        callable_method(exp_output)
        assert os.path.exists(exp_output)

        # Check that data can be reloaded
        re_reader = CSVReader(data_type, subject, localization,
                              experiment="FR1", file_path=exp_output)
        reread_data = re_reader.as_dataframe()
        assert reread_data is not None


@pytest.mark.rhino
class TestElectrodeCategoriesReader:
    @pytest.mark.parametrize("subject,lens", [
        ("R1111M", {'soz': 9, 'interictal': 15, 'brain_lesion': 5, 'bad_channel': 6}),
        ("R1052E", {'soz': 2, 'interictal': 14, 'brain_lesion': 0, 'bad_channel': 0})
    ])
    def test_load(self, subject, lens, rhino_root):
        reader = ElectrodeCategoriesReader('electrode_categories',
                                           subject=subject,
                                           rootdir=rhino_root)
        categories = reader.load()
        pytest.set_trace()
        for key, len_ in lens.items():
            assert len(categories[key]) == len_
