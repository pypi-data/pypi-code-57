


from axlnlp.training import Trainer
from axlnlp import DataSet, FeatureSet



class Evaluator:

    def __init__(self,dataset:DataSet, experiment_name:str, method:str="default", features:FeatureSet=None):
        self.dataset = dataset
        self.features = features
        self.method = method
        self.experiment_name = experiment_name
        self.eval_method = self.__select_eval_method()

    
    def __init__experiment_log(self):
        
        """
        create a spread-sheet, with:

        model id, (score on train), score on dev, score on test, STD for each score,  model name, model type, hyperparams, link to comet?

        scores are average accros folds, seeds etc..

        if experiment log already exist we just append to it.

        """
        pass


    def default(self, trainer, model_class, hyperparams):
        """
        normal train, dev  eval
        """
        model = model_class(self.dataset, self.features, hyperparams)
        trainer.train(model)


    def cross_validation(self, trainer, model_class, hyperparams):
        """
        cross validation


        NOT THE NUMBER OF SPLITS DONE IS DECIDED BY DATASET?
        OR SHOULD WE CHANGE THIS?        
        """
        while true:
            model = model_class(self.dataset, self.features, hyperparams)
            trainer.train(model)



    def __select_eval_method(self):

        
        if self.method == "default":
            return self.default
        


    def evalutate(self, models, of_percent, hyperparam_set):
        #
        """

        for each model test hyperparams

        """
        for model_class in models:
            for hyperparams in hyperparam_set:

                gpu = None
                model_save_path = ""
                model_load_path = ""


                trainer = Trainer(   
                                    hyperparams=hyperparams, 
                                    gpu=gpu,
                                    of_percent=of_percent,
                                    model_save_path=model_save_path,
                                    model_load_path=model_load_path,
                                    monitor="val_mean_task_f1",
                                    logger=None
                                    )
                #m = model(self.dataset, self.features, hyperparams)
                self.eval_method(trainer, model_class, hyperparams)



    def test(self, select="all"):  # all, best, or a name of a model
        # test all, or best. based on VAL SCORE

        """

        testing all the models, or a set of models, or one model


        """
        pass