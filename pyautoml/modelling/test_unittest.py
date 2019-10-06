import unittest

import numpy as np
import pandas as pd
from pyautoml import Model


class TestModelling(unittest.TestCase):

    def test_text_gensim_summarize(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(x_train=data, split=False)
        model.summarize_gensim('data', ratio=0.5, run=True)
        validate = model.data_summarized is not None

        self.assertTrue(validate)

    
    def test_text_gensim_keywords(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(x_train=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, run=True)
        validate = model.data_extracted_keywords is not None

        self.assertTrue(validate)


    def test_model_getattr(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(x_train=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, model_name='model1', run=True)
        validate = model.model1 is not None and model['model1'] is not None

        self.assertTrue(validate)

    def test_model_addtoqueue(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(x_train=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, model_name='model1', run=False)
        model.summarize_gensim('data', ratio=0.5, run=False)
        validate = len(model._queued_models)

        self.assertEquals(validate, 2)

    def test_model_kmeans(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(x_train=data, split=False)
        model.kmeans(n_clusters=3, random_state=0, run=True)
        validate = model.kmeans_clusters is not None

        self.assertTrue(validate)

    
    def test_model_kmeans_split(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(x_train=data)
        model.kmeans(n_clusters=3, random_state=0, run=True)
        validate = model.x_train_results.kmeans_clusters is not None and model.x_test_results.kmeans_clusters is not None

        self.assertTrue(validate)

    def test_model_dbscan(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(x_train=data, split=False)
        model.dbscan(eps=3, min_samples=2, run=True)
        validate = model.dbscan_clusters is not None

        self.assertTrue(validate)

    def test_model_cluster_filter(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(x_train=data, split=False)
        model = model.dbscan(eps=3, min_samples=2, run=True)
        filtered = model.filter_cluster(0)
        validate = all(filtered.dbscan_clusters == 0)

        self.assertTrue(validate)

    def test_model_defaultgridsearch(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [3, 2, 0], [1, 2, 1]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', report_name='gridsearch_test')
        model.logistic_regression(gridsearch=True, cv_type=2, run=True)

        self.assertTrue(True)

    def test_model_logisticregression(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        validate = model.x_train_results.log_predictions is not None and model.x_test_results.log_predictions is not None

        self.assertTrue(validate)

    def test_model_confusionmatrix(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.confusion_matrix()

        self.assertTrue(True)

    def test_model_report_confusionmatrix(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', report_name='confusion_report')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.confusion_matrix()

        self.assertTrue(True)

    def test_model_all_score_metrics(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', report_name='metric_report')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.metrics()

        self.assertTrue(True)

    def test_model_report_classificationreport(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', report_name='classification_report')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.classification_report()

        self.assertTrue(True)

    def test_model_report_modelweights(self):
        
        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.model_weights()

        self.assertTrue(True)

    def test_plot_roccurve(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.roc_curve()

        self.assertTrue(True)
    
    def test_decision_plot(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.decision_plot()

        self.assertTrue(True)

    def test_decision_plot_all(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.decision_plot(num_samples='all')

        self.assertTrue(True)

    def test_decision_plot_sameaxis(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        r = model.log_reg.decision_plot(sample_no=1)
        model.log_reg.decision_plot(sample_no=2, feature_order=r.feature_idx, xlim=r.xlim)

        self.assertTrue(True)

    def test_decision_plot_misclassified(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.decision_plot(0.75, highlight_misclassified=True)

        self.assertTrue(True)

    def test_force_plot(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.force_plot()

        self.assertTrue(True)

    def test_force_plot_misclassified(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.6)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.force_plot(misclassified=True)

        self.assertTrue(True)

    def test_get_misclassified(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.shap_get_misclassified_index()

        self.assertTrue(True)

    def test_summaryplot(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.summary_plot()

        self.assertTrue(True)

    def test_dependence_plot(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2', run=True)
        model.log_reg.dependence_plot('col1')

        self.assertTrue(True)    

    def test_local_multiprocessing(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', model_name='l1', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l2', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l3', run=True)

        model.run_models()

        self.assertTrue(len(model._models) == 3 and len(model._queued_models) == 0)

    def test_local_seriesprocessing(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', model_name='l1', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l2', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l3', run=True)

        model.run_models(method='series')

        self.assertTrue(len(model._models) == 3 and len(model._queued_models) == 0)

    def test_interpretmodel_behaviour_all(self):


        train_data = np.random.random_sample(size=(1000,2))
        label_data = np.random.random_integers(0, 1, size=(1000,1))

        data = pd.DataFrame(data=train_data, columns=['col1', 'col2'])
        data['col3'] = label_data

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.2)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model_behavior(show=False)

        self.assertTrue(True)

    def test_interpretmodel_behaviour_dependence(self):

        data = np.random.random_integers(0, 1, size=(1000,3))
        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.4)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model_behavior(method='dependence', show=False)

        self.assertTrue(True)

    def test_interpretmodel_predictions_all(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.6)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_predictions(show=False)

        self.assertTrue(True)

    def test_interpretmodel_predictions_lime(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.6)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_predictions(method='lime', show=False)

        self.assertTrue(True)

    def test_interpretmodel_performance_all(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.6)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model_performance(show=False)

        self.assertTrue(True)

    def test_interpretmodel_performance_roc(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.6)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model_performance(method='ROC', show=False)

        self.assertTrue(True)

    def test_interpret_model(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.4)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model(show=False)

        self.assertTrue(True)

    def test_interpret_model_prerun(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.4)
        model.logistic_regression(random_state=2, run=True)
        model.log_reg.interpret_model_performance(method='ROC', show=False)
        model.log_reg.interpret_model(show=False)

        self.assertTrue(True)

    def test_comparemodels(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(x_train=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', model_name='l1', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l2', run=True)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l3', run=True)

        model.run_models(method='series')
        model.compare_models()

        self.assertTrue(True)

    def test_cv(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])
        model = Model(x_train=data, target_field='col3', test_split_percentage=0.2)
        model.logistic_regression(cv=True, cv_type=2, random_state=2, learning_curve=True)

        self.assertTrue(True)

    def test_stratified_cv(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])
        model = Model(x_train=data, target_field='col3', test_split_percentage=0.2)
        cv_values = model.logistic_regression(cv=True, cv_type='strat-kfold', random_state=2, learning_curve=True, run=False)

        self.assertIsNotNone(len(cv_values) == 5)

    def test_del_model(self):

        data = np.random.random_integers(0, 1, size=(1000,3))

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])
        model = Model(x_train=data, target_field='col3', test_split_percentage=0.2)
        model.logistic_regression(random_state=2, run=True)
        model.delete_model('log_reg')

        self.assertTrue(len(model._models) == 0)

if __name__ == "__main__":

    unittest.main()