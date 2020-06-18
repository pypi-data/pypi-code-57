import unittest
from sklearn.pipeline import Pipeline
from pprint import pprint
import pandas as pd
import traceback
from os import environ

from watson_machine_learning_client import WatsonMachineLearningAPIClient

from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.deployment import WebService

from watson_machine_learning_client.helpers.connections import S3Connection, S3Location, DataConnection, DSLocation

from watson_machine_learning_client.experiment.autoai.optimizers import RemoteAutoPipelines

from watson_machine_learning_client.tests.utils import get_wml_credentials, get_cos_credentials, is_cp4d, bucket_exists, bucket_name_gen
from watson_machine_learning_client.tests.utils.cleanup import delete_model_deployment, bucket_cleanup

from lale import wrap_imported_operators
from lale.operators import TrainablePipeline
from lale.lib.lale import Hyperopt


@unittest.skipIf(is_cp4d(), "Not supported on CP4D")
class TestAutoAIRemote(unittest.TestCase):
    wml_client: 'WatsonMachineLearningAPIClient' = None
    experiment: 'AutoAI' = None
    remote_auto_pipelines: 'RemoteAutoPipelines' = None
    wml_credentials = None
    cos_credentials = None
    pipeline_opt: 'RemoteAutoPipelines' = None
    service: 'WebService' = None

    data_location = './autoai/data/bank.csv'

    trained_pipeline_details = None
    run_id = None

    data_connection = None
    results_connection = None

    train_data = None
    holdout_data = None
    if "BUCKET_NAME" in environ:
        bucket_name = environ['BUCKET_NAME']
    else:
        bucket_name = "wml-autoaitests-qa"

    cos_endpoint = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    data_cos_path = 'data/bank.csv'

    results_cos_path = 'results_wml_autoai'

    pipeline: 'Pipeline' = None
    lale_pipeline = None
    deployed_pipeline = None
    hyperopt_pipelines = None
    new_pipeline = None
    new_sklearn_pipeline = None

    OPTIMIZER_NAME = 'Bank wml_autoai binary test'
    DEPLOYMENT_NAME = "Bank AutoAI Deployment tests"

    project_id = None
    space_id = None

    asset_id = None

    @classmethod
    def setUp(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.data = pd.read_csv(cls.data_location)
        cls.X = cls.data.drop(['y'], axis=1)
        cls.y = cls.data['y']

        cls.wml_credentials = get_wml_credentials()
        if not is_cp4d():
            cls.cos_credentials = get_cos_credentials()
            if 'endpoint_url' in cls.cos_credentials:
                cls.cos_endpoint = cls.cos_credentials['endpoint_url']

        cls.wml_client = WatsonMachineLearningAPIClient(wml_credentials=cls.wml_credentials.copy())

    def test_00_prepare_COS_instance(self):
        import ibm_boto3
        cos_resource = ibm_boto3.resource(
            service_name="s3",
            endpoint_url=self.cos_endpoint,
            aws_access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
            aws_secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']
        )
        # Prepare bucket
        if not bucket_exists(cos_resource, self.bucket_name):
            try:
                bucket_cleanup(cos_resource, prefix=f"{self.bucket_name}-")
            except Exception as e:
                print(f"Bucket cleanup with prefix {self.bucket_name}- failed due to:\n{e}\n skipped")

            import datetime
            TestAutoAIRemote.bucket_name = bucket_name_gen(prefix=f"{self.bucket_name}-{str(datetime.date.today())}")
            print(f"Creating COS bucket: {TestAutoAIRemote.bucket_name}")
            cos_resource.Bucket(TestAutoAIRemote.bucket_name).create()

            self.assertIsNotNone(TestAutoAIRemote.bucket_name)
            self.assertTrue(bucket_exists(cos_resource, TestAutoAIRemote.bucket_name))

        print(f"Using COS bucket: {TestAutoAIRemote.bucket_name}")

    def test_01_initialize_AutoAI_experiment__pass_credentials__object_initialized(self):
        if is_cp4d():
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials.copy(),
                                                 project_id=self.project_id,
                                                 space_id=self.space_id)
        else:
            TestAutoAIRemote.experiment = AutoAI(wml_credentials=self.wml_credentials)

        self.assertIsInstance(self.experiment, AutoAI, msg="Experiment is not of type AutoAI.")

    def test_02_save_remote_data_and_DataConnection_setup(self):
        if is_cp4d():
            self.wml_client.set.default_project(self.project_id)
            asset_details = self.wml_client.data_assets.create(
                name=self.data_location.split('/')[-1],
                file_path=self.data_location)
            asset_id = asset_details['metadata']['guid']

            TestAutoAIRemote.data_connection = DataConnection(
                                location=DSLocation(asset_id=asset_id))
            TestAutoAIRemote.results_connection = None

        else: #for cloud and COS
            TestAutoAIRemote.data_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.data_cos_path)
            )
            TestAutoAIRemote.results_connection = DataConnection(
                connection=S3Connection(endpoint_url=self.cos_endpoint,
                                        access_key_id=self.cos_credentials['cos_hmac_keys']['access_key_id'],
                                        secret_access_key=self.cos_credentials['cos_hmac_keys']['secret_access_key']),
                location=S3Location(bucket=self.bucket_name,
                                    path=self.results_cos_path)
            )
            TestAutoAIRemote.data_connection.write(data=self.data, remote_name=self.data_cos_path)

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_03_initialize_optimizer(self):
        TestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name=self.OPTIMIZER_NAME,
            desc='test description',
            prediction_type=self.experiment.PredictionType.BINARY,
            prediction_column='y',
            scoring=self.experiment.Metrics.ROC_AUC_SCORE,
            test_size=0.1,
            max_number_of_estimators=1
        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_04_get_configuration_parameters_of_remote_auto_pipeline(self):
        parameters = self.remote_auto_pipelines.get_params()
        # print(parameters)
        self.assertIsInstance(parameters, dict, msg='Config parameters are not a dictionary instance.')

    def test_05_fit_run_training_of_auto_ai_in_wml(self):
        TestAutoAIRemote.trained_pipeline_details = self.remote_auto_pipelines.fit(
            training_data_reference=[self.data_connection],
            training_results_reference=self.results_connection,
            background_mode=False)

        TestAutoAIRemote.run_id = self.trained_pipeline_details['metadata']['id']

        self.assertIsNotNone(self.data_connection.auto_pipeline_params,
                             msg='DataConnection auto_pipeline_params was not updated.')

        TestAutoAIRemote.train_data, TestAutoAIRemote.holdout_data = self.remote_auto_pipelines.get_data_connections()[0].read(with_holdout_split=True)

        print("train data sample:")
        print(self.train_data.head())
        self.assertGreater(len(self.train_data), 0)
        print("holdout data sample:")
        print(self.holdout_data.head())
        self.assertGreater(len(self.holdout_data), 0)

    def test_06_get_run_status(self):
        status = self.remote_auto_pipelines.get_run_status()
        self.assertEqual(status, "completed", msg="AutoAI run didn't finished successfully. Status: {}".format(status))

    def test_07_get_run_details(self):
        parameters = self.remote_auto_pipelines.get_run_details()
        # print(parameters)
        self.assertIsNotNone(parameters)

    def test_08_predict_using_fitted_pipeline(self):
        predictions = self.remote_auto_pipelines.predict(X=self.holdout_data.drop(['y'], axis=1).values[:5])
        print(predictions)
        self.assertGreater(len(predictions), 0)

    def test_09_summary_listing_all_pipelines_from_wml(self):
        pipelines_details = self.remote_auto_pipelines.summary()
        print(pipelines_details)

    def test_10__get_data_connections__return_a_list_with_data_connections_with_optimizer_params(self):
        data_connections = self.remote_auto_pipelines.get_data_connections()
        self.assertIsInstance(data_connections, list, msg="There should be a list container returned")
        self.assertIsInstance(data_connections[0], DataConnection,
                              msg="There should be a DataConnection object returned")

    def test_11_get_pipeline_params_specific_pipeline_parameters(self):
        pipeline_params = self.remote_auto_pipelines.get_pipeline_details(pipeline_name='Pipeline_1')
        print(pipeline_params)

    def test_12__get_pipeline_params__fetch_best_pipeline_parameters__parameters_fetched_as_dict(self):
        best_pipeline_params = self.remote_auto_pipelines.get_pipeline_details()
        print(best_pipeline_params)

    ####
    # LALE #
    ########

    def test_13__get_pipeline__load_lale_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.lale_pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4')
        print(f"Fetched pipeline type: {type(self.pipeline)}")

        self.assertIsInstance(self.lale_pipeline, TrainablePipeline,
                              msg="Fetched pipeline is not of TrainablePipeline instance.")
        # predictions = self.pipeline.predict(
        #     X=self.holdout_data.drop(['y'], axis=1).values[:5])  # works with autoai_libs from branch `development` (date: 9th March 20)
        # print(predictions)

    def test_13b_get_all_pipelines_as_lale(self):
        summary = self.remote_auto_pipelines.summary()
        print(summary)
        failed_pipelines = []
        for pipeline_name in summary.reset_index()['Pipeline Name']:
            print(f"Getting pipeline: {pipeline_name}")
            lale_pipeline = None
            try:
                lale_pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name=pipeline_name)
                self.assertIsInstance(lale_pipeline, TrainablePipeline)
                predictions = lale_pipeline.predict(
                    X=self.X.values[:1])
                print(predictions)
                self.assertGreater(len(predictions), 0, msg=f"Returned prediction for {pipeline_name} are empty")
            except:
                print(f"Failure: {pipeline_name}")
                failed_pipelines.append(pipeline_name)
                traceback.print_exc()

            if not TestAutoAIRemote.lale_pipeline:
                TestAutoAIRemote.lale_pipeline = lale_pipeline
                print(f"{pipeline_name} loaded for next test cases")

        self.assertEqual(len(failed_pipelines), 0, msg=f"Some pipelines failed. Full list: {failed_pipelines}")

    @unittest.skip("Skipped lale pretty print")
    def test_14__pretty_print_lale__checks_if_generated_python_pipeline_code_is_correct(self):
        pipeline_code = self.lale_pipeline.pretty_print()
        try:
            exec(pipeline_code)

        except Exception as exception:
            self.assertIsNone(exception,
                              msg=f"Pretty print from lale pipeline was not successful \n\n Full pipeline code:\n {pipeline_code}")

    def test_15a_remove_last_freeze_trainable_prefix_returned(self):
        from lale.lib.sklearn import KNeighborsClassifier, DecisionTreeClassifier, LogisticRegression
        prefix = self.lale_pipeline.remove_last().freeze_trainable()
        self.assertIsInstance(prefix, TrainablePipeline,
                              msg="Prefix pipeline is not of TrainablePipeline instance.")
        TestAutoAIRemote.new_pipeline = prefix >> (KNeighborsClassifier| DecisionTreeClassifier| LogisticRegression)

    def test_15b_hyperopt_fit_new_pipepiline(self):
        hyperopt = Hyperopt(estimator=TestAutoAIRemote.new_pipeline, cv=3, max_evals=2)
        try:
            TestAutoAIRemote.hyperopt_pipelines = hyperopt.fit(self.X.values, self.y.values)
        except ValueError as e:
            print(f"ValueError message: {e}")
            traceback.print_exc()
            hyperopt_results = hyperopt._impl._trials.results
            print(hyperopt_results)
            self.assertIsNone(e, msg="hyperopt fit was not successful")

    def test_15c_get_pipeline_from_hyperopt(self):
        new_pipeline_model = TestAutoAIRemote.hyperopt_pipelines.get_pipeline()
        print(f"Hyperopt_pipeline_model is type: {type(new_pipeline_model)}")
        TestAutoAIRemote.new_sklearn_pipeline = new_pipeline_model.export_to_sklearn_pipeline()
        self.assertIsInstance(TestAutoAIRemote.new_sklearn_pipeline, Pipeline,
                              msg=f"Incorect Sklearn Pipeline type after conversion. Current: {type(TestAutoAIRemote.new_sklearn_pipeline)}")

    def test_16_predict_refined_pipeline(self):
        predictions = TestAutoAIRemote.new_sklearn_pipeline.predict(
            X=self.X.values[:1])
        print(predictions)
        self.assertGreater(len(predictions), 0, msg=f"Returned prediction for refined pipeline are empty")

    # def test_15__predict__do_the_predict_on_lale_pipeline__results_computed(self):
    #     predictions = self.lale_pipeline.predict(self.X.values)
    #     print(predictions)

    def test_18__get_pipeline__load_specified_pipeline__pipeline_loaded(self):
        TestAutoAIRemote.pipeline = self.remote_auto_pipelines.get_pipeline(pipeline_name='Pipeline_4',
                                                                            astype=self.experiment.PipelineTypes.SKLEARN)
        print(f"Fetched pipeline type: {type(self.pipeline)}")

        self.assertIsInstance(self.pipeline, Pipeline,
                              msg="Fetched pipeline is not of sklearn.Pipeline instance.")

    def test_19__predict__do_the_predict_on_sklearn_pipeline__results_computed(self):
        predictions = self.pipeline.predict(self.X.values)
        print(predictions)

    #################################
    #      DEPLOYMENT SECTION       #
    #################################

    def test_20_deployment_setup_and_preparation(self):
        if is_cp4d():
            TestAutoAIRemote.service = WebService(wml_credentials=self.wml_credentials.copy(),
                                                  project_id=self.project_id,
                                                  space_id=self.space_id)
            self.wml_client.set.default_space(self.space_id)
        else:
            TestAutoAIRemote.service = WebService(wml_credentials=self.wml_credentials)

        self.wml_client.set.default_space(self.space_id) if self.wml_client.ICP else None

        delete_model_deployment(self.wml_client, deployment_name=self.DEPLOYMENT_NAME)

        self.wml_client.set.default_project(self.project_id) if self.wml_client.ICP else None

    def test_21__deploy__deploy_best_computed_pipeline_from_autoai_on_wml(self):
        self.service.create(
            experiment_run_id=self.remote_auto_pipelines._engine._current_run_id,
            model=self.pipeline,
            deployment_name=self.DEPLOYMENT_NAME)

    def test_22_score_deployed_model(self):
        nb_records = 5
        predictions = self.service.score(payload=self.holdout_data.drop(['y'], axis=1)[:nb_records])
        print(predictions)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions['predictions'][0]['values']), nb_records)

    def test_23_list_deployments(self):
        self.service.list()
        params = self.service.get_params()
        print(params)
        self.assertIsNotNone(params)

    def test_24_delete_deployment(self):
        print("Delete current deployment: {}".format(self.service.deployment_id))
        self.service.delete()

if __name__ == '__main__':
    unittest.main()
