class DummyClassifier(MultiOutputMixin, ClassifierMixin, BaseEstimator):
    """<#TODO Description>

    Parameters
    ----------
    strategy : <#TODO type definition>, default=warn
        <#TODO Description>

    random_state : <#TODO type definition>, default=None
        <#TODO Description>

    constant : <#TODO type definition>, default=None
        <#TODO Description>

    Attributes
    ----------
    sparse_output_ : <#TODO type definition>
        <#TODO Attribute Description>

    n_outputs_ : <#TODO type definition>
        <#TODO Attribute Description>

    n_features_in_ : <#TODO type definition>
        <#TODO Attribute Description>

    outputs_2d_ : <#TODO type definition>
        <#TODO Attribute Description>

    Examples
    --------
    >>> from crawto_doc import crawto_doc
    >>> example = DummyClassifier(strategy='warn', random_state=None, constant=None)
    >>> example.fit(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
    <#TODO Method Return Value>
    >>> example.predict(X=<#TODO Example Value>)
    <#TODO Method Return Value>
    >>> example.predict_proba(X=<#TODO Example Value>)
    <#TODO Method Return Value>
    >>> example.predict_log_proba(X=<#TODO Example Value>)
    <#TODO Method Return Value>
    >>> example.score(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
    <#TODO Method Return Value>
    """

    @_deprecate_positional_args
    def __init__(self, *, strategy='warn', random_state=None, constant=None):
        self.strategy = strategy
        self.random_state = random_state
        self.constant = constant

    def fit(self, X, y, sample_weight: Optional=None):
        """<#TODO Description>

        Parameters
        ----------
        X : <#TODO type definition>
            <#TODO Description>

        y : <#TODO type definition>
            <#TODO Description>

        sample_weight : Optional, default=None
            <#TODO Description>

        Returns
        -------
        self : <#TODO return description>
        """
        allowed_strategies = ('most_frequent', 'stratified', 'uniform',
            'constant', 'prior')
        if self.strategy == 'warn':
            warnings.warn(
                'The default value of strategy will change from stratified to prior in 0.24.'
                , FutureWarning)
            self._strategy = 'stratified'
        elif self.strategy not in allowed_strategies:
            raise ValueError(
                'Unknown strategy type: %s, expected one of %s.' % (self.
                strategy, allowed_strategies))
        else:
            self._strategy = self.strategy
        if self._strategy == 'uniform' and sp.issparse(y):
            y = y.toarray()
            warnings.warn(
                'A local copy of the target data has been converted to a numpy array. Predicting on sparse target data with the uniform strategy would not save memory and would be slower.'
                , UserWarning)
        self.sparse_output_ = sp.issparse(y)
        if not self.sparse_output_:
            y = np.asarray(y)
            y = np.atleast_1d(y)
        if y.ndim == 1:
            y = np.reshape(y, (-1, 1))
        self.n_outputs_ = y.shape[1]
        self.n_features_in_ = None
        check_consistent_length(X, y)
        if sample_weight is not None:
            sample_weight = _check_sample_weight(sample_weight, X)
        if self._strategy == 'constant':
            if self.constant is None:
                raise ValueError(
                    'Constant target value has to be specified when the constant strategy is used.'
                    )
            else:
                constant = np.reshape(np.atleast_1d(self.constant), (-1, 1))
                if constant.shape[0] != self.n_outputs_:
                    raise ValueError(
                        'Constant target value should have shape (%d, 1).' %
                        self.n_outputs_)
        self.classes_, self.n_classes_, self.class_prior_ = class_distribution(
            y, sample_weight)
        if self._strategy == 'constant':
            for k in range(self.n_outputs_):
                if not any(constant[k][0] == c for c in self.classes_[k]):
                    err_msg = (
                        'The constant target value must be present in the training data. You provided constant={}. Possible values are: {}.'
                        .format(self.constant, list(self.classes_[k])))
                    raise ValueError(err_msg)
        if self.n_outputs_ == 1:
            self.n_classes_ = self.n_classes_[0]
            self.classes_ = self.classes_[0]
            self.class_prior_ = self.class_prior_[0]
        return self

    def predict(self, X):
        """<#TODO Description>

        Parameters
        ----------
        X : <#TODO type definition>
            <#TODO Description>

        Returns
        -------
        y : <#TODO return description>
        """
        check_is_fitted(self)
        n_samples = _num_samples(X)
        rs = check_random_state(self.random_state)
        n_classes_ = self.n_classes_
        classes_ = self.classes_
        class_prior_ = self.class_prior_
        constant = self.constant
        if self.n_outputs_ == 1:
            n_classes_ = [n_classes_]
            classes_ = [classes_]
            class_prior_ = [class_prior_]
            constant = [constant]
        if self._strategy == 'stratified':
            proba = self.predict_proba(X)
            if self.n_outputs_ == 1:
                proba = [proba]
        if self.sparse_output_:
            class_prob = None
            if self._strategy in ('most_frequent', 'prior'):
                classes_ = [np.array([cp.argmax()]) for cp in class_prior_]
            elif self._strategy == 'stratified':
                class_prob = class_prior_
            elif self._strategy == 'uniform':
                raise ValueError(
                    'Sparse target prediction is not supported with the uniform strategy'
                    )
            elif self._strategy == 'constant':
                classes_ = [np.array([c]) for c in constant]
            y = _random_choice_csc(n_samples, classes_, class_prob, self.
                random_state)
        else:
            if self._strategy in ('most_frequent', 'prior'):
                y = np.tile([classes_[k][class_prior_[k].argmax()] for k in
                    range(self.n_outputs_)], [n_samples, 1])
            elif self._strategy == 'stratified':
                y = np.vstack([classes_[k][proba[k].argmax(axis=1)] for k in
                    range(self.n_outputs_)]).T
            elif self._strategy == 'uniform':
                ret = [classes_[k][rs.randint(n_classes_[k], size=n_samples
                    )] for k in range(self.n_outputs_)]
                y = np.vstack(ret).T
            elif self._strategy == 'constant':
                y = np.tile(self.constant, (n_samples, 1))
            if self.n_outputs_ == 1:
                y = np.ravel(y)
        return y

    def predict_proba(self, X):
        """<#TODO Description>

        Parameters
        ----------
        X : <#TODO type definition>
            <#TODO Description>

        Returns
        -------
        P : <#TODO return description>
        """
        check_is_fitted(self)
        n_samples = _num_samples(X)
        rs = check_random_state(self.random_state)
        n_classes_ = self.n_classes_
        classes_ = self.classes_
        class_prior_ = self.class_prior_
        constant = self.constant
        if self.n_outputs_ == 1:
            n_classes_ = [n_classes_]
            classes_ = [classes_]
            class_prior_ = [class_prior_]
            constant = [constant]
        P = []
        for k in range(self.n_outputs_):
            if self._strategy == 'most_frequent':
                ind = class_prior_[k].argmax()
                out = np.zeros((n_samples, n_classes_[k]), dtype=np.float64)
                out[:, (ind)] = 1.0
            elif self._strategy == 'prior':
                out = np.ones((n_samples, 1)) * class_prior_[k]
            elif self._strategy == 'stratified':
                out = rs.multinomial(1, class_prior_[k], size=n_samples)
                out = out.astype(np.float64)
            elif self._strategy == 'uniform':
                out = np.ones((n_samples, n_classes_[k]), dtype=np.float64)
                out /= n_classes_[k]
            elif self._strategy == 'constant':
                ind = np.where(classes_[k] == constant[k])
                out = np.zeros((n_samples, n_classes_[k]), dtype=np.float64)
                out[:, (ind)] = 1.0
            P.append(out)
        if self.n_outputs_ == 1:
            P = P[0]
        return P

    def predict_log_proba(self, X):
        """<#TODO Description>

        Parameters
        ----------
        X : <#TODO type definition>
            <#TODO Description>

        Returns
        -------
        None : <#TODO return description>
        """
        proba = self.predict_proba(X)
        if self.n_outputs_ == 1:
            return np.log(proba)
        else:
            return [np.log(p) for p in proba]

    def _more_tags(self):
        return {'poor_score': True, 'no_validation': True, '_xfail_checks':
            {'check_methods_subset_invariance': 'fails for the predict method'}
            }

    def score(self, X, y, sample_weight=None):
        """<#TODO Description>

        Parameters
        ----------
        X : <#TODO type definition>
            <#TODO Description>

        y : <#TODO type definition>
            <#TODO Description>

        sample_weight : <#TODO type definition>, default=None
            <#TODO Description>

        Returns
        -------
        <#TODO return value> : <#TODO return description>
        """
        if X is None:
            X = np.zeros(shape=(len(y), 1))
        return super().score(X, y, sample_weight)

    @deprecated(
        'The outputs_2d_ attribute is deprecated in version 0.22 and will be removed in version 0.24. It is equivalent to n_outputs_ > 1.'
        )
    @property
    def outputs_2d_(self):
        return self.n_outputs_ != 1
