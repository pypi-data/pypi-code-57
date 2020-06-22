#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.
 

model_mapping = {
    'mappings': {
        'properties': {
            'id': {
                'type': 'keyword',
                'ignore_above': 128,
                'index': True
            },
            'timestamp': {
                'type': 'date',
                'format': 'epoch_millis',
                'index': True
            },
            'algorithm': {
                'type': 'keyword',
                'ignore_above': 64,
            },
            'model_file': {
                'type': 'keyword',
                'ignore_above': 64,
            },
            'scaler_file': {
                'type': 'keyword',
                'ignore_above': 64,
            },
            'metadata': {
                'type': 'object',
            },
            'labelencoder': {
                'type': 'object'
            },
            'model_params': {
                "type" : "object" ,
                "properties" : {
                    "data_type" : {
                        "type" : "keyword"
                    },
                    "num_previous_measures" : {
                        "type" : "keyword"
                    },
                    "num_forecasts" : {
                        "type" : "keyword"
                    },
                    "time_index" : {
                        "type" : "keyword"
                    },
                    "inference_features" : {
                        "type" : "keyword"
                    },
                    "dataset_features" : {
                        "type" : "keyword"
                    }
                }
            }
        }
    }
}

predictions_mapping = {
    "mappings": {
        "properties": {
            "model_file": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "algorithm": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "id": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "prediction_times": {
                "type": "date"
            },
            'timestamp': {
                'type': 'date',
                'index': True
            },
            "values": {
                "type": "object"
            },
            "latency": {
                "type": "float"
            }
        }
    }
}

classifications_mapping = {
    "mappings": {
        "properties": {
           "model_file": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "algorithm": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "id": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }, 
            "class": {
                "type": "text"
            },
            "confidence": {
                "type": "float"
            },
            "latency": {
                "type": "float"
            }
        }
    }

}
