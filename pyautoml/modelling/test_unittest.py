import unittest

import pandas as pd

from pyautoml import Model


class TestModelling(unittest.TestCase):

    def test_text_gensim_summarize(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(data=data, split=False)
        model.summarize_gensim('data', ratio=0.5, run=True)
        validate = model.data_summarized is not None

        self.assertTrue(validate)

    
    def test_text_gensim_keywords(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(data=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, run=True)
        validate = model.data_extracted_keywords is not None

        self.assertTrue(validate)


    def test_model_getattr(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(data=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, model_name='model1', run=True)
        validate = model.model1 is not None and model['model1'] is not None

        self.assertTrue(validate)

    def test_model_addtoqueue(self):

        text_data = [
                    "Hi my name is PyAutoML. Please split me.",
                    "This function is going to split by sentence. Automation is great."
                    ]

        data = pd.DataFrame(data=text_data, columns=['data'])

        model = Model(data=data, split=False)
        model.extract_keywords_gensim('data', ratio=0.5, model_name='model1', run=False)
        model.summarize_gensim('data', ratio=0.5, run=False)
        validate = len(model._queued_models)

        self.assertEquals(validate, 2)

    def test_model_kmeans(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(data=data, split=False)
        model.kmeans(n_clusters=3, random_state=0)
        validate = model.kmeans_clusters is not None

        self.assertTrue(validate)

    
    def test_model_kmeans_split(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(data=data)
        model.kmeans(n_clusters=3, random_state=0)
        validate = model.train_data_results.kmeans_clusters is not None and model.test_data_results.kmeans_clusters is not None

        self.assertTrue(validate)

    def test_model_dbscan(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(data=data, split=False)
        model.dbscan(eps=3, min_samples=2)
        validate = model.dbscan_clusters is not None

        self.assertTrue(validate)

    def test_model_cluster_filter(self):

        data = [[1, 2], [2, 2], [2, 3],
            [8, 7], [8, 8], [25, 80]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2'])

        model = Model(data=data, split=False)
        model = model.dbscan(eps=3, min_samples=2)
        filtered = model.filter_cluster(0)
        validate = all(filtered.dbscan_clusters == 0)

        self.assertTrue(validate)

    def test_model_defaultgridsearch(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [3, 2, 0], [1, 2, 1]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', report_name='gridsearch_test')
        model.logistic_regression(gridsearch=True, gridsearch_cv=2)

        self.assertTrue(True)

    def test_model_logisticregression(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3')
        model.logistic_regression(random_state=2, penalty='l2')
        validate = model.train_data_results.log_predictions is not None and model.test_data_results.log_predictions is not None

        self.assertTrue(validate)

    def test_model_confusionmatrix(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.confusion_matrix()

        self.assertTrue(True)

    def test_model_report_confusionmatrix(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', report_name='confusion_report')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.confusion_matrix()

        self.assertTrue(True)

    def test_model_all_score_metrics(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', report_name='metric_report')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.metric('all', metric='all')

        self.assertTrue(True)

    def test_model_report_classificationreport(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', report_name='classification_report')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.classification_report()

        self.assertTrue(True)

    def test_model_report_modelweights(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.model_weights()

        self.assertTrue(True)

    def test_plot_roccurve(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.roc_curve()

        self.assertTrue(True)
    
    def test_decision_plot(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.decision_plot()

        self.assertTrue(True)

    def test_decision_plot_all(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.decision_plot(num_samples='all')

        self.assertTrue(True)

    def test_decision_plot_sameaxis(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        r = model.log_reg.decision_plot(sample_no=1)
        model.log_reg.decision_plot(sample_no=2, feature_order=r.feature_idx, xlim=r.xlim)

        self.assertTrue(True)

    def test_decision_plot_misclassified(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [4, 2, 1], [12, 2, 1], [25, 80, 1],
            [14, 23, 1], [215, 15, 1], [2, 33, 1],
            [81, 73, 0], [8, 28, 0], [625, 280, 0],
            [1, 22, 431], [21, 42, 11], [2, 3, 1],
            [81, 47, 0], [8, 8, 0], [425, 80, 0],
            [1, 22, 1], [2, 42, 1], [2, 13, 1],
            [83, 73, 0], [8, 83, 0], [125, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.8)
        model.logistic_regression(random_state=3)
        model.log_reg.decision_plot(0.75, highlight_misclassified=True)

        self.assertTrue(True)

    def test_force_plot(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.force_plot()

        self.assertTrue(True)

    def test_force_plot_misclassified(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [4, 2, 0], [12, 2, 0], [25, 80, 0],
            [14, 23, 1], [215, 15, 1], [2, 33, 1],
            [81, 73, 0], [8, 28, 0], [625, 280, 0],
            [1, 22, 431], [21, 42, 11], [2, 3, 1],
            [81, 47, 0], [8, 8, 0], [425, 80, 0],
            [1, 22, 1], [2, 42, 1], [2, 13, 1],
            [83, 73, 1], [8, 83, 1], [125, 80, 1]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.75)
        model.logistic_regression(random_state=2)
        model.log_reg.force_plot(misclassified=True)

        self.assertTrue(True)

    def test_get_misclassified(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.shap_get_misclassified_index()

        self.assertTrue(True)

    def test_summaryplot(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.summary_plot()

        self.assertTrue(True)

    def test_dependence_plot(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0],
            [1, 2, 1], [2, 2, 1], [2, 3, 1],
            [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5)
        model.logistic_regression(random_state=2, penalty='l2')
        model.log_reg.dependence_plot('col1')

        self.assertTrue(True)    

    def test_local_multiprocessing(self):

        data = [[1, 2, 1], [2, 2, 1], [2, 3, 1],
                [8, 7, 0], [8, 8, 0], [25, 80, 0],
                [1, 2, 1], [2, 2, 1], [2, 3, 1],
                [8, 7, 0], [8, 8, 0], [25, 80, 0],
                [1, 2, 1], [2, 2, 1], [2, 3, 1],
                [8, 7, 0], [8, 8, 0], [25, 80, 0],
                [1, 2, 1], [2, 2, 1], [2, 3, 1],
                [8, 7, 0], [8, 8, 0], [25, 80, 0]]

        data = pd.DataFrame(data=data, columns=['col1', 'col2', 'col3'])

        model = Model(data=data, target_field='col3', test_split_percentage=0.5, report_name='modelweights')
        model.logistic_regression(random_state=2, penalty='l2', model_name='l1', run=False)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l2', run=False)
        model.logistic_regression(random_state=2, penalty='l2', model_name='l3', run=False)

        model.run_models()

        print(model._models)
        self.assertTrue(len(model._models) == 3 and len(model._queued_models) == 0)


if __name__ == "__main__":

    unittest.main()
