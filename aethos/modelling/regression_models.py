from .model import ModelBase
from aethos.config import shell
from aethos.model_analysis.regression_model_analysis import RegressionModelAnalysis
from aethos.analysis import Analysis
from aethos.cleaning.clean import Clean
from aethos.preprocessing.preprocess import Preprocess
from aethos.feature_engineering.feature import Feature
from aethos.visualizations.visualizations import Visualizations
from aethos.stats.stats import Stats
from aethos.modelling.util import add_to_queue


class Regression(
    ModelBase, Analysis, Clean, Preprocess, Feature, Visualizations, Stats
):
    def __init__(
        self,
        x_train,
        target,
        x_test=None,
        test_split_percentage=0.2,
        exp_name="my-experiment",
    ):
        """
        Class to run analysis, transform your data and run Regression algorithms.

        Parameters
        -----------
        x_train: pd.DataFrame
            Training data or aethos data object

        target: str
            For supervised learning problems, the name of the column you're trying to predict.

        x_test: pd.DataFrame
            Test data, by default None

        test_split_percentage: float
            Percentage of data to split train data into a train and test set, by default 0.2.

        exp_name : str
            Experiment name to be tracked in MLFlow.
        """

        super().__init__(
            x_train,
            target,
            x_test=x_test,
            test_split_percentage=test_split_percentage,
            exp_name=exp_name,
        )

    @add_to_queue
    def LinearRegression(
        self,
        cv_type=None,
        gridsearch=None,
        score="neg_mean_squared_error",
        model_name="lin_reg",
        run=True,
        verbose=1,
        **kwargs,
    ):
        # region
        """
        Trains a Linear Regression.

        For more Linear Regression info, you can view it here: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression

        If running gridsearch, the implemented cross validators are:
            - 'kfold' for KFold
            - 'strat-kfold' for StratifiedKfold

        Possible scoring metrics:
            - 'explained_variance'
            - 'max_error'
            - 'neg_mean_absolute_error' --> MAE
            - 'neg_mean_squared_error' --> MSE
            - 'neg_mean_squared_log_error' --> MSLE
            - 'neg_median_absolute_error' --> MeAE
            - 'r2'

        Parameters
        ----------
        cv : bool, optional
            If True run crossvalidation on the model, by default None.

        gridsearch : int, Crossvalidation Generator, optional
            Cross validation method, by default None

        score : str, optional
            Scoring metric to evaluate models, by default 'neg_mean_squared_error'

        model_name : str, optional
            Name for this model, by default "lin_reg"

        run : bool, optional
            Whether to train the model or just initialize it with parameters (useful when wanting to test multiple models at once) , by default False

        verbose : int, optional
            Verbosity level of model output, the higher the number - the more verbose. By default, 1

        fit_intercept : boolean, optional, default True
            whether to calculate the intercept for this model.
            If set to False, no intercept will be used in calculations (e.g. data is expected to be already centered).

        normalize : boolean, optional, default False
            This parameter is ignored when fit_intercept is set to False.
            If True, the regressors X will be normalized before regression by subtracting the mean and dividing by the l2-norm.

        Returns
        -------
        RegressionModelAnalysis
            RegressionModelAnalysis object to view results and analyze results

        Examples
        --------
        >>> model.LinearRegression()
        >>> model.LinearRegression(model_name='m1', normalize=True)
        >>> model.LinearRegression(cv=10)
        >>> model.LinearRegression(gridsearch={'normalize':[True, False]}, cv='strat-kfold')
        >>> model.LinearRegression(run=False) # Add model to the queue
        """
        # endregion

        from sklearn.linear_model import LinearRegression

        model = LinearRegression

        model = self._run_supervised_model(
            model,
            model_name,
            RegressionModelAnalysis,
            cv_type=cv_type,
            gridsearch=gridsearch,
            score=score,
            run=run,
            verbose=verbose,
            **kwargs,
        )

        return model

    @add_to_queue
    def ElasticnetRegression(
        self,
        cv_type=None,
        gridsearch=None,
        score="neg_mean_squared_error",
        model_name="elastic",
        run=True,
        verbose=1,
        **kwargs,
    ):
        # region
        """
        Elastic Net regression with combined L1 and L2 priors as regularizer.

        For more Linear Regression info, you can view it here: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet

        If running gridsearch, the implemented cross validators are:
            - 'kfold' for KFold
            - 'strat-kfold' for StratifiedKfold

        Possible scoring metrics:
            - 'explained_variance'
            - 'max_error'
            - 'neg_mean_absolute_error' --> MAE
            - 'neg_mean_squared_error' --> MSE
            - 'neg_mean_squared_log_error' --> MSLE
            - 'neg_median_absolute_error' --> MeAE
            - 'r2'

        Parameters
        ----------
        cv : bool, optional
            If True run crossvalidation on the model, by default None.

        gridsearch : int, Crossvalidation Generator, optional
            Cross validation method, by default None

        score : str, optional
            Scoring metric to evaluate models, by default 'neg_mean_squared_error'

        model_name : str, optional
            Name for this model, by default "elastic"

        run : bool, optional
            Whether to train the model or just initialize it with parameters (useful when wanting to test multiple models at once) , by default False

        verbose : int, optional
            Verbosity level of model output, the higher the number - the more verbose. By default, 1

        alpha : float, optional
            Constant that multiplies the penalty terms.
            Defaults to 1.0. See the notes for the exact mathematical meaning of this parameter.
            ``alpha = 0`` is equivalent to an ordinary least square, solved by the LinearRegression object.
            For numerical reasons, using alpha = 0 with the Lasso object is not advised.
            Given this, you should use the LinearRegression object.

        l1_ratio : float
            The ElasticNet mixing parameter, with 0 <= l1_ratio <= 1.
            For l1_ratio = 0 the penalty is an L2 penalty.
            For l1_ratio = 1 it is an L1 penalty.
            For 0 < l1_ratio < 1, the penalty is a combination of L1 and L2.

        fit_intercept : bool
            Whether the intercept should be estimated or not.
            If False, the data is assumed to be already centered.

        normalize : boolean, optional, default False
            This parameter is ignored when fit_intercept is set to False.
            If True, the regressors X will be normalized before regression by subtracting the mean and dividing by the l2-norm.
            If you wish to standardize, please use sklearn.preprocessing.

        precompute : True | False | array-like
            Whether to use a precomputed Gram matrix to speed up calculations.
            The Gram matrix can also be passed as argument.
            For sparse input this option is always True to preserve sparsity.

        max_iter : int, optional
            The maximum number of iterations

        tol : float, optional
            The tolerance for the optimization: if the updates are smaller than tol, the optimization code checks the dual gap for optimality and continues until it is smaller than tol.

        positive : bool, optional
            When set to True, forces the coefficients to be positive.

        selection : str, default 'cyclic'
            If set to 'random', a random coefficient is updated every iteration rather than looping over features sequentially by default.
            This (setting to 'random') often leads to significantly faster convergence especially when tol is higher than 1e-4.

        Returns
        -------
        RegressionModelAnalysis
            RegressionModelAnalysis object to view results and analyze results

        Examples
        --------
        >>> model.ElasticNetRegression()
        >>> model.ElasticNetRegression(model_name='m1', alpha=0.0003)
        >>> model.ElasticNetRegression(cv=10)
        >>> model.ElasticNetRegression(gridsearch={'alpha':[0.01, 0.02]}, cv='strat-kfold')
        >>> model.ElasticNetRegression(run=False) # Add model to the queue
        """
        # endregion

        from sklearn.linear_model import ElasticNet

        model = ElasticNet

        model = self._run_supervised_model(
            model,
            model_name,
            RegressionModelAnalysis,
            cv_type=cv_type,
            gridsearch=gridsearch,
            score=score,
            run=run,
            verbose=verbose,
            **kwargs,
        )

        return model

    @add_to_queue
    def GradientBoostingRegression(
        self,
        cv_type=None,
        gridsearch=None,
        score="neg_mean_squared_error",
        model_name="grad_reg",
        run=True,
        verbose=1,
        **kwargs,
    ):
        # region
        """
        Trains a Gradient Boosting regression model.

        GB builds an additive model in a forward stage-wise fashion; it allows for the optimization of arbitrary differentiable loss functions.
        In each stage n_classes_ regression trees are fit on the negative gradient of the binomial or multinomial deviance loss function.

        For more Gradient Boosting Classifier info, you can view it here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor

        If running gridsearch, the implemented cross validators are:
            - 'kfold' for KFold
            - 'strat-kfold' for StratifiedKfold

        Possible scoring metrics:
            - 'explained_variance'
            - 'max_error'
            - 'neg_mean_absolute_error' --> MAE
            - 'neg_mean_squared_error' --> MSE
            - 'neg_mean_squared_log_error' --> MSLE
            - 'neg_median_absolute_error' --> MeAE
            - 'r2'

        Parameters
        ----------
        cv : bool, optional
            If True run crossvalidation on the model, by default None.

        gridsearch : int, Crossvalidation Generator, optional
            Cross validation method, by default None

        score : str, optional
            Scoring metric to evaluate models, by default 'neg_mean_squared_error'

        model_name : str, optional
            Name for this model, by default "grad_reg"

        run : bool, optional
            Whether to train the model or just initialize it with parameters (useful when wanting to test multiple models at once) , by default False

        verbose : int, optional
            Verbosity level of model output, the higher the number - the more verbose. By default, 1

        loss : {'ls', 'lad', 'huber', 'quantile'}, optional (default='ls')
            loss function to be optimized.

            'ls' refers to least squares regression.
            'lad' (least absolute deviation) is a highly robust loss function solely based on order information of the input variables.
            'huber' is a combination of the two.
            'quantile' allows quantile regression (use alpha to specify the quantile).

        learning_rate : float, optional (default=0.1)
            learning rate shrinks the contribution of each tree by learning_rate.
            There is a trade-off between learning_rate and n_estimators.

        n_estimators : int (default=100)
            The number of boosting stages to perform.
            Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance.

        subsample : float, optional (default=1.0)
            The fraction of samples to be used for fitting the individual base learners.
            If smaller than 1.0 this results in Stochastic Gradient Boosting.
            Subsample interacts with the parameter n_estimators.
            Choosing subsample < 1.0 leads to a reduction of variance and an increase in bias.

        criterion : string, optional (default=”friedman_mse”)
            The function to measure the quality of a split.
            Supported criteria are “friedman_mse” for the mean squared error with improvement score by Friedman, “mse” for mean squared error, and “mae” for the mean absolute error.
            The default value of “friedman_mse” is generally the best as it can provide a better approximation in some cases.

        min_samples_split : int, float, optional (default=2)
            The minimum number of samples required to split an internal node:

                If int, then consider min_samples_split as the minimum number.
                If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split.

        min_samples_leaf : int, float, optional (default=1)
            The minimum number of samples required to be at a leaf node.
            A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches.
            This may have the effect of smoothing the model, especially in regression.

                If int, then consider min_samples_leaf as the minimum number.
                If float, then min_samples_leaf is a fraction and ceil(min_samples_leaf * n_samples) are the minimum number of samples for each node.

        max_depth : integer, optional (default=3)
            maximum depth of the individual regression estimators.
            The maximum depth limits the number of nodes in the tree.
            Tune this parameter for best performance; the best value depends on the interaction of the input variables.

        max_features : int, float, string or None, optional (default=None)
            The number of features to consider when looking for the best split:

                If int, then consider max_features features at each split.
                If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.
                If “auto”, then max_features=sqrt(n_features).
                If “sqrt”, then max_features=sqrt(n_features).
                If “log2”, then max_features=log2(n_features).
                If None, then max_features=n_features.

            Choosing max_features < n_features leads to a reduction of variance and an increase in bias.

            Note: the search for a split does not stop until at least one valid partition of the node samples is found, even if it requires to effectively inspect more than max_features features.

        alpha : float (default=0.9)
            The alpha-quantile of the huber loss function and the quantile loss function.
            Only if loss='huber' or loss='quantile'.

        max_leaf_nodes : int or None, optional (default=None)
            Grow trees with max_leaf_nodes in best-first fashion.
            Best nodes are defined as relative reduction in impurity.
            If None then unlimited number of leaf nodes.

        presort : bool or 'auto', optional (default='auto')
            Whether to presort the data to speed up the finding of best splits in fitting.
            Auto mode by default will use presorting on dense data and default to normal sorting on sparse data.
            Setting presort to true on sparse data will raise an error.

        validation_fraction : float, optional, default 0.1
            The proportion of training data to set aside as validation set for early stopping.
            Must be between 0 and 1. Only used if n_iter_no_change is set to an integer.

        tol : float, optional, default 1e-4
            Tolerance for the early stopping.
            When the loss is not improving by at least tol for n_iter_no_change iterations (if set to a number), the training stops.

        Returns
        -------
        RegressionModelAnalysis
            RegressionModelAnalysis object to view results and analyze results

        Examples
        --------
        >>> model.GradientBoostingRegression()
        >>> model.GradientBoostingRegression(model_name='m1', alpha=0.0003)
        >>> model.GradientBoostingRegression(cv=10)
        >>> model.GradientBoostingRegression(gridsearch={'alpha':[0.01, 0.02]}, cv='strat-kfold')
        >>> model.GradientBoostingRegression(run=False) # Add model to the queue
        """
        # endregion

        from sklearn.ensemble import GradientBoostingRegressor

        model = GradientBoostingRegressor

        model = self._run_supervised_model(
            model,
            model_name,
            RegressionModelAnalysis,
            cv_type=cv_type,
            gridsearch=gridsearch,
            score=score,
            run=run,
            verbose=verbose,
            **kwargs,
        )

        return model

    @add_to_queue
    def RandomForestRegression(
        self,
        cv_type=None,
        gridsearch=None,
        score="neg_mean_squared_error",
        model_name="rf_reg",
        run=True,
        verbose=1,
        **kwargs,
    ):
        # region
        """
        Trains a Random Forest Regression model.

        A random forest is a meta estimator that fits a number of decision tree regressors on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.
        The sub-sample size is always the same as the original input sample size but the samples are drawn with replacement if bootstrap=True (default).

        For more Random Forest info, you can view it here: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor

        If running gridsearch, the implemented cross validators are:
            - 'kfold' for KFold
            - 'strat-kfold' for StratifiedKfold

        Possible scoring metrics:
            - 'explained_variance'
            - 'max_error'
            - 'neg_mean_absolute_error' --> MAE
            - 'neg_mean_squared_error' --> MSE
            - 'neg_mean_squared_log_error' --> MSLE
            - 'neg_median_absolute_error' --> MeAE
            - 'r2'

        Parameters
        ----------
        cv : bool, optional
            If True run crossvalidation on the model, by default None.

        gridsearch : int, Crossvalidation Generator, optional
            Cross validation method, by default None

        score : str, optional
            Scoring metric to evaluate models, by default 'neg_mean_squared_error'

        model_name : str, optional
            Name for this model, by default "rf_reg"

        run : bool, optional
            Whether to train the model or just initialize it with parameters (useful when wanting to test multiple models at once) , by default False

        verbose : int, optional
            Verbosity level of model output, the higher the number - the more verbose. By default, 1

        n_estimators : integer, optional (default=10)
            The number of trees in the forest.

        criterion : string, optional (default=”mse”)
            The function to measure the quality of a split.
            Supported criteria are “mse” for the mean squared error, which is equal to variance reduction as feature selection criterion, and “mae” for the mean absolute error.

        max_depth : integer or None, optional (default=None)
            The maximum depth of the tree.
            If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.

        min_samples_split : int, float, optional (default=2)
            The minimum number of samples required to split an internal node:

                If int, then consider min_samples_split as the minimum number.
                If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split.

        min_samples_leaf : int, float, optional (default=1)
            The minimum number of samples required to be at a leaf node. A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression.

                If int, then consider min_samples_leaf as the minimum number.
                If float, then min_samples_leaf is a fraction and ceil(min_samples_leaf * n_samples) are the minimum number of samples for each node.

        max_features : int, float, string or None, optional (default=”auto”)
            The number of features to consider when looking for the best split:

                If int, then consider max_features features at each split.
                If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.
                If “auto”, then max_features=sqrt(n_features).
                If “sqrt”, then max_features=sqrt(n_features) (same as “auto”).
                If “log2”, then max_features=log2(n_features).
                If None, then max_features=n_features.

            Note: the search for a split does not stop until at least one valid partition of the node samples is found, even if it requires to effectively inspect more than max_features features.

        max_leaf_nodes : int or None, optional (default=None)
            Grow trees with max_leaf_nodes in best-first fashion.
            Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.

        min_impurity_decrease : float, optional (default=0.)
            A node will be split if this split induces a decrease of the impurity greater than or equal to this value.

            The weighted impurity decrease equation is the following:

            N_t / N * (impurity - N_t_R / N_t * right_impurity
                                - N_t_L / N_t * left_impurity)

            where N is the total number of samples, N_t is the number of samples at the current node, N_t_L is the number of samples in the left child, and N_t_R is the number of samples in the right child.

            N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed.

        bootstrap : boolean, optional (default=True)
            Whether bootstrap samples are used when building trees. If False, the whole datset is used to build each tree.

        oob_score : bool (default=False)
            Whether to use out-of-bag samples to estimate the generalization accuracy.

        ccp_alphanon-negative : float, optional (default=0.0)
            Complexity parameter used for Minimal Cost-Complexity Pruning.
            The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
            By default, no pruning is performed.
            See Minimal Cost-Complexity Pruning for details.

        Returns
        -------
        RegressionModelAnalysis
            RegressionModelAnalysis object to view results and analyze results

        Examples
        --------
        >>> model.RandomForestRegression()
        >>> model.RandomForestRegression(model_name='m1', n_estimators=100)
        >>> model.RandomForestRegression(cv=10)
        >>> model.RandomForestRegression(gridsearch={'n_estimators':[100, 200]}, cv='strat-kfold')
        >>> model.RandomForestRegression(run=False) # Add model to the queue
        """
        # endregion

        from sklearn.ensemble import RandomForestRegressor

        model = RandomForestRegressor

        model = self._run_supervised_model(
            model,
            model_name,
            RegressionModelAnalysis,
            cv_type=cv_type,
            gridsearch=gridsearch,
            score=score,
            run=run,
            verbose=verbose,
            **kwargs,
        )

        return model

    @add_to_queue
    def XGBoostRegression(
        self,
        cv_type=None,
        gridsearch=None,
        score="neg_mean_squared_error",
        model_name="xgb_reg",
        run=True,
        verbose=1,
        **kwargs,
    ):
        # region
        """
        Trains an XGBoost Regression Model.

        XGBoost is an optimized distributed gradient boosting library designed to be highly efficient, flexible and portable.
        It implements machine learning algorithms under the Gradient Boosting framework.
        XGBoost provides a parallel tree boosting (also known as GBDT, GBM) that solve many data science problems in a fast and accurate way.
        The same code runs on major distributed environment (Hadoop, SGE, MPI) and can solve problems beyond billions of examples.

        For more XGBoost info, you can view it here: https://xgboost.readthedocs.io/en/latest/ and
        https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst.

        If running gridsearch, the implemented cross validators are:
            - 'kfold' for KFold
            - 'strat-kfold' for StratifiedKfold

        Possible scoring metrics:
            - 'explained_variance'
            - 'max_error'
            - 'neg_mean_absolute_error' --> MAE
            - 'neg_mean_squared_error' --> MSE
            - 'neg_mean_squared_log_error' --> MSLE
            - 'neg_median_absolute_error' --> MeAE
            - 'r2'

        Parameters
        ----------
        cv : bool, optional
            If True run crossvalidation on the model, by default None.

        gridsearch : int, Crossvalidation Generator, optional
            Cross validation method, by default None

        score : str, optional
            Scoring metric to evaluate models, by default 'neg_mean_squared_error'

        model_name : str, optional
            Name for this model, by default "xgb_reg"

        run : bool, optional
            Whether to train the model or just initialize it with parameters (useful when wanting to test multiple models at once) , by default False

        verbose : int, optional
            Verbosity level of model output, the higher the number - the more verbose. By default, 1

        max_depth : int
            Maximum tree depth for base learners. By default 3

        learning_rate : float
            Boosting learning rate (xgb's "eta"). By default 0.1

        n_estimators : int
            Number of trees to fit. By default 100.

        objective : string or callable
            Specify the learning task and the corresponding learning objective or
            a custom objective function to be used (see note below).
            By default, reg:linear

        booster: string
            Specify which booster to use: gbtree, gblinear or dart. By default 'gbtree'

        tree_method: string
            Specify which tree method to use
            If this parameter is set to default, XGBoost will choose the most conservative option
            available.  It's recommended to study this option from parameters
            document. By default 'auto'

        gamma : float
            Minimum loss reduction required to make a further partition on a leaf node of the tree.
            By default 0

        subsample : float
            Subsample ratio of the training instance.
            By default 1

        reg_alpha : float (xgb's alpha)
            L1 regularization term on weights. By default 0

        reg_lambda : float (xgb's lambda)
            L2 regularization term on weights. By default 1

        scale_pos_weight : float
            Balancing of positive and negative weights. By default 1

        base_score:
            The initial prediction score of all instances, global bias. By default 0

        missing : float, optional
            Value in the data which needs to be present as a missing value. If
            None, defaults to np.nan.
            By default, None

        num_parallel_tree: int
            Used for boosting random forest.
            By default 1

        importance_type: string, default "gain"
            The feature importance type for the feature_importances\\_ property:
            either "gain", "weight", "cover", "total_gain" or "total_cover".
            By default 'gain'.

        Note
        ----
        A custom objective function can be provided for the ``objective``
        parameter. In this case, it should have the signature
        ``objective(y_true, y_pred) -> grad, hess``:

        y_true: array_like of shape [n_samples]
            The target values

        y_pred: array_like of shape [n_samples]
            The predicted values

        grad: array_like of shape [n_samples]
            The value of the gradient for each sample point.

        hess: array_like of shape [n_samples]
            The value of the second derivative for each sample point

        Returns
        -------
        RegressionModelAnalysis
            RegressionModelAnalysis object to view results and analyze results

        Examples
        --------
        >>> model.XGBoostRegression()
        >>> model.XGBoostRegression(model_name='m1', reg_alpha=0.0003)
        >>> model.XGBoostRegression(cv=10)
        >>> model.XGBoostRegression(gridsearch={'reg_alpha':[0.01, 0.02]}, cv='strat-kfold')
        >>> model.XGBoostRegression(run=False) # Add model to the queue
        """
        # endregion

        import xgboost as xgb

        model = xgb.XGBRegressor

        model = self._run_supervised_model(
            model,
            model_name,
            RegressionModelAnalysis,
            cv_type=cv_type,
            gridsearch=gridsearch,
            score=score,
            run=run,
            verbose=verbose,
            **kwargs,
        )

        return model
