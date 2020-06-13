
from axlnlp.models.lstm import LSTM
from axlnlp.models.lstm_crf import LSTM_CRF
from axlnlp.models.bert_token_clf import BertTok
#from axlnlp.models.lstm_cnn_crf import BiLSTM_CNN_CRF

__all__ = [ 
            LSTM, 
            LSTM_CRF,
            BertTok,
            #BiLSTM_CNN_CRF,
            
            ]

# def get_model(model_name):

#     if model_name == "lstm":
#         return LSTM

#     elif model_name == "lstm_crf":
#         return BiLSTM_CRF

#     elif model_name == "lstm_cnn_crf":
#     	return BiLSTM_CNN_CRF
    	
#     else:
#         raise KeyError('"{}" is not a supported model'.format(model_name))
