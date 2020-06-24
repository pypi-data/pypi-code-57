PLAN_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "merchandiser_settings": {
            "additionalProperties": false,
            "properties": {
                "accuracy": {
                    "default": "DAY",
                    "enum": [
                        "EXACT",
                        "DAY",
                        "CUSTOM_1",
                        "CUSTOM_2",
                        "CUSTOM_3"
                    ],
                    "nullable": false,
                    "type": "string"
                }
            },
            "type": "object"
        },
        "orders": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "duration": {
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "facts": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "time_window": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "from": {
                                            "format": "date-time",
                                            "type": "string"
                                        },
                                        "to": {
                                            "format": "date-time",
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "from",
                                        "to"
                                    ],
                                    "type": "object"
                                }
                            },
                            "required": [
                                "time_window"
                            ],
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "location": {
                        "additionalProperties": false,
                        "properties": {
                            "arrival_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "departure_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "latitude": {
                                "format": "double",
                                "maximum": 90,
                                "minimum": -90,
                                "type": "number"
                            },
                            "longitude": {
                                "format": "double",
                                "maximum": 180,
                                "minimum": -180,
                                "type": "number"
                            }
                        },
                        "required": [
                            "latitude",
                            "longitude"
                        ],
                        "type": "object"
                    },
                    "reward": {
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "visits": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "time_window": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "from": {
                                            "format": "date-time",
                                            "type": "string"
                                        },
                                        "to": {
                                            "format": "date-time",
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "from",
                                        "to"
                                    ],
                                    "type": "object"
                                }
                            },
                            "required": [
                                "time_window"
                            ],
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "location",
                    "visits",
                    "duration",
                    "reward"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "performer": {
            "additionalProperties": false,
            "properties": {
                "finish_location": {
                    "additionalProperties": false,
                    "properties": {
                        "arrival_duration": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 1440,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "departure_duration": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 1440,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "latitude": {
                            "format": "double",
                            "maximum": 90,
                            "minimum": -90,
                            "type": "number"
                        },
                        "longitude": {
                            "format": "double",
                            "maximum": 180,
                            "minimum": -180,
                            "type": "number"
                        }
                    },
                    "required": [
                        "latitude",
                        "longitude"
                    ],
                    "type": "object"
                },
                "key": {
                    "maxLength": 1024,
                    "minLength": 1,
                    "type": "string"
                },
                "shifts": {
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "availability_time": {
                                "additionalProperties": false,
                                "properties": {
                                    "from": {
                                        "format": "date-time",
                                        "type": "string"
                                    },
                                    "to": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "from",
                                    "to"
                                ],
                                "type": "object"
                            },
                            "trip": {
                                "additionalProperties": false,
                                "properties": {
                                    "actions": {
                                        "items": {
                                            "additionalProperties": false,
                                            "properties": {
                                                "location_time": {
                                                    "additionalProperties": false,
                                                    "properties": {
                                                        "from": {
                                                            "format": "date-time",
                                                            "type": "string"
                                                        },
                                                        "to": {
                                                            "format": "date-time",
                                                            "type": "string"
                                                        }
                                                    },
                                                    "required": [
                                                        "from",
                                                        "to"
                                                    ],
                                                    "type": "object"
                                                },
                                                "order": {
                                                    "additionalProperties": false,
                                                    "properties": {
                                                        "duration": {
                                                            "format": "double",
                                                            "minimum": 0,
                                                            "type": "number"
                                                        },
                                                        "facts": {
                                                            "items": {
                                                                "additionalProperties": false,
                                                                "properties": {
                                                                    "time_window": {
                                                                        "additionalProperties": false,
                                                                        "properties": {
                                                                            "from": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            },
                                                                            "to": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            }
                                                                        },
                                                                        "required": [
                                                                            "from",
                                                                            "to"
                                                                        ],
                                                                        "type": "object"
                                                                    }
                                                                },
                                                                "required": [
                                                                    "time_window"
                                                                ],
                                                                "type": "object"
                                                            },
                                                            "maxItems": 100,
                                                            "minItems": 0,
                                                            "type": "array"
                                                        },
                                                        "key": {
                                                            "maxLength": 1024,
                                                            "minLength": 1,
                                                            "type": "string"
                                                        },
                                                        "location": {
                                                            "additionalProperties": false,
                                                            "properties": {
                                                                "arrival_duration": {
                                                                    "default": 0,
                                                                    "format": "int32",
                                                                    "maximum": 1440,
                                                                    "minimum": 0,
                                                                    "type": "integer"
                                                                },
                                                                "departure_duration": {
                                                                    "default": 0,
                                                                    "format": "int32",
                                                                    "maximum": 1440,
                                                                    "minimum": 0,
                                                                    "type": "integer"
                                                                },
                                                                "latitude": {
                                                                    "format": "double",
                                                                    "maximum": 90,
                                                                    "minimum": -90,
                                                                    "type": "number"
                                                                },
                                                                "longitude": {
                                                                    "format": "double",
                                                                    "maximum": 180,
                                                                    "minimum": -180,
                                                                    "type": "number"
                                                                }
                                                            },
                                                            "required": [
                                                                "latitude",
                                                                "longitude"
                                                            ],
                                                            "type": "object"
                                                        },
                                                        "reward": {
                                                            "format": "double",
                                                            "minimum": 0,
                                                            "type": "number"
                                                        },
                                                        "visits": {
                                                            "items": {
                                                                "additionalProperties": false,
                                                                "properties": {
                                                                    "time_window": {
                                                                        "additionalProperties": false,
                                                                        "properties": {
                                                                            "from": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            },
                                                                            "to": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            }
                                                                        },
                                                                        "required": [
                                                                            "from",
                                                                            "to"
                                                                        ],
                                                                        "type": "object"
                                                                    }
                                                                },
                                                                "required": [
                                                                    "time_window"
                                                                ],
                                                                "type": "object"
                                                            },
                                                            "maxItems": 100,
                                                            "minItems": 1,
                                                            "type": "array"
                                                        }
                                                    },
                                                    "required": [
                                                        "key",
                                                        "location",
                                                        "visits",
                                                        "duration",
                                                        "reward"
                                                    ],
                                                    "type": "object"
                                                },
                                                "order_time": {
                                                    "additionalProperties": false,
                                                    "properties": {
                                                        "from": {
                                                            "format": "date-time",
                                                            "type": "string"
                                                        },
                                                        "to": {
                                                            "format": "date-time",
                                                            "type": "string"
                                                        }
                                                    },
                                                    "required": [
                                                        "from",
                                                        "to"
                                                    ],
                                                    "type": "object"
                                                }
                                            },
                                            "required": [
                                                "order",
                                                "order_time",
                                                "location_time"
                                            ],
                                            "type": "object"
                                        },
                                        "maxItems": 1000,
                                        "minItems": 1,
                                        "type": "array"
                                    },
                                    "key": {
                                        "maxLength": 1024,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "trip_time": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "from": {
                                                "format": "date-time",
                                                "type": "string"
                                            },
                                            "to": {
                                                "format": "date-time",
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "from",
                                            "to"
                                        ],
                                        "type": "object"
                                    },
                                    "waitlist": {
                                        "items": {
                                            "additionalProperties": false,
                                            "properties": {
                                                "order": {
                                                    "additionalProperties": false,
                                                    "properties": {
                                                        "duration": {
                                                            "format": "double",
                                                            "minimum": 0,
                                                            "type": "number"
                                                        },
                                                        "facts": {
                                                            "items": {
                                                                "additionalProperties": false,
                                                                "properties": {
                                                                    "time_window": {
                                                                        "additionalProperties": false,
                                                                        "properties": {
                                                                            "from": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            },
                                                                            "to": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            }
                                                                        },
                                                                        "required": [
                                                                            "from",
                                                                            "to"
                                                                        ],
                                                                        "type": "object"
                                                                    }
                                                                },
                                                                "required": [
                                                                    "time_window"
                                                                ],
                                                                "type": "object"
                                                            },
                                                            "maxItems": 100,
                                                            "minItems": 0,
                                                            "type": "array"
                                                        },
                                                        "key": {
                                                            "maxLength": 1024,
                                                            "minLength": 1,
                                                            "type": "string"
                                                        },
                                                        "location": {
                                                            "additionalProperties": false,
                                                            "properties": {
                                                                "arrival_duration": {
                                                                    "default": 0,
                                                                    "format": "int32",
                                                                    "maximum": 1440,
                                                                    "minimum": 0,
                                                                    "type": "integer"
                                                                },
                                                                "departure_duration": {
                                                                    "default": 0,
                                                                    "format": "int32",
                                                                    "maximum": 1440,
                                                                    "minimum": 0,
                                                                    "type": "integer"
                                                                },
                                                                "latitude": {
                                                                    "format": "double",
                                                                    "maximum": 90,
                                                                    "minimum": -90,
                                                                    "type": "number"
                                                                },
                                                                "longitude": {
                                                                    "format": "double",
                                                                    "maximum": 180,
                                                                    "minimum": -180,
                                                                    "type": "number"
                                                                }
                                                            },
                                                            "required": [
                                                                "latitude",
                                                                "longitude"
                                                            ],
                                                            "type": "object"
                                                        },
                                                        "reward": {
                                                            "format": "double",
                                                            "minimum": 0,
                                                            "type": "number"
                                                        },
                                                        "visits": {
                                                            "items": {
                                                                "additionalProperties": false,
                                                                "properties": {
                                                                    "time_window": {
                                                                        "additionalProperties": false,
                                                                        "properties": {
                                                                            "from": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            },
                                                                            "to": {
                                                                                "format": "date-time",
                                                                                "type": "string"
                                                                            }
                                                                        },
                                                                        "required": [
                                                                            "from",
                                                                            "to"
                                                                        ],
                                                                        "type": "object"
                                                                    }
                                                                },
                                                                "required": [
                                                                    "time_window"
                                                                ],
                                                                "type": "object"
                                                            },
                                                            "maxItems": 100,
                                                            "minItems": 1,
                                                            "type": "array"
                                                        }
                                                    },
                                                    "required": [
                                                        "key",
                                                        "location",
                                                        "visits",
                                                        "duration",
                                                        "reward"
                                                    ],
                                                    "type": "object"
                                                }
                                            },
                                            "type": "object"
                                        },
                                        "maxItems": 1000,
                                        "minItems": 0,
                                        "type": "array"
                                    }
                                },
                                "required": [
                                    "key",
                                    "trip_time"
                                ],
                                "type": "object"
                            },
                            "working_time": {
                                "additionalProperties": false,
                                "properties": {
                                    "from": {
                                        "format": "date-time",
                                        "type": "string"
                                    },
                                    "to": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "from",
                                    "to"
                                ],
                                "type": "object"
                            }
                        },
                        "required": [
                            "availability_time",
                            "working_time"
                        ],
                        "type": "object"
                    },
                    "maxItems": 100,
                    "minItems": 1,
                    "type": "array"
                },
                "start_location": {
                    "additionalProperties": false,
                    "properties": {
                        "arrival_duration": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 1440,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "departure_duration": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 1440,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "latitude": {
                            "format": "double",
                            "maximum": 90,
                            "minimum": -90,
                            "type": "number"
                        },
                        "longitude": {
                            "format": "double",
                            "maximum": 180,
                            "minimum": -180,
                            "type": "number"
                        }
                    },
                    "required": [
                        "latitude",
                        "longitude"
                    ],
                    "type": "object"
                },
                "tariff": {
                    "additionalProperties": false,
                    "properties": {
                        "basic": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "cost_per_meter": {
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "cost_per_minute": {
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "cost_per_shift": {
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "max_length": {
                                    "format": "double",
                                    "minimum": 0.1,
                                    "type": "number"
                                },
                                "max_time": {
                                    "format": "double",
                                    "minimum": 0.1,
                                    "type": "number"
                                }
                            },
                            "required": [
                                "cost_per_shift",
                                "cost_per_meter",
                                "max_length",
                                "cost_per_minute",
                                "max_time"
                            ],
                            "type": "object"
                        },
                        "extra": {
                            "items": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "cost_per_meter": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "cost_per_minute": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "cost_per_shift": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "max_length": {
                                        "format": "double",
                                        "minimum": 0.1,
                                        "type": "number"
                                    },
                                    "max_time": {
                                        "format": "double",
                                        "minimum": 0.1,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "cost_per_shift",
                                    "cost_per_meter",
                                    "max_length",
                                    "cost_per_minute",
                                    "max_time"
                                ],
                                "type": "object"
                            },
                            "maxItems": 10,
                            "minItems": 0,
                            "type": "array"
                        }
                    },
                    "required": [
                        "basic"
                    ],
                    "type": "object"
                },
                "transport_type": {
                    "default": "CAR",
                    "enum": [
                        "CAR",
                        "TRUCK",
                        "CAR_GT",
                        "TUK_TUK",
                        "BICYCLE",
                        "PEDESTRIAN",
                        "PUBLIC_TRANSPORT"
                    ],
                    "nullable": false,
                    "type": "string"
                }
            },
            "required": [
                "key",
                "transport_type",
                "shifts",
                "tariff"
            ],
            "type": "object"
        },
        "settings": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "assumptions": {
                    "additionalProperties": false,
                    "nullable": false,
                    "properties": {
                        "disable_capacity": {
                            "default": false,
                            "type": "boolean"
                        },
                        "disable_compatibility": {
                            "default": false,
                            "type": "boolean"
                        },
                        "expand_shift_time_window": {
                            "default": false,
                            "type": "boolean"
                        },
                        "flight_distance": {
                            "default": false,
                            "type": "boolean"
                        },
                        "same_order_time_window": {
                            "default": false,
                            "type": "boolean"
                        },
                        "traffic_jams": {
                            "default": true,
                            "type": "boolean"
                        }
                    },
                    "type": "object"
                },
                "capacity_factor": {
                    "default": [],
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "capacity": {
                                "default": 1,
                                "format": "double",
                                "maximum": 10,
                                "minimum": 0.1,
                                "type": "number"
                            },
                            "transport_type": {
                                "default": "CAR",
                                "enum": [
                                    "CAR",
                                    "TRUCK",
                                    "CAR_GT",
                                    "TUK_TUK",
                                    "BICYCLE",
                                    "PEDESTRIAN",
                                    "PUBLIC_TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            }
                        },
                        "required": [
                            "transport_type",
                            "capacity"
                        ],
                        "type": "object"
                    },
                    "maxItems": 7,
                    "minItems": 0,
                    "type": "array"
                },
                "configuration": {
                    "default": "default",
                    "maxLength": 1000,
                    "minLength": 1,
                    "type": "string"
                },
                "planning_time": {
                    "default": 20,
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 1,
                    "type": "integer"
                },
                "precision": {
                    "default": 3,
                    "format": "int32",
                    "maximum": 6,
                    "minimum": 0,
                    "type": "integer"
                },
                "predict_slots": {
                    "default": 0,
                    "format": "int32",
                    "maximum": 4,
                    "minimum": 0,
                    "type": "integer"
                },
                "result_timezone": {
                    "default": 0,
                    "format": "int32",
                    "maximum": 12,
                    "minimum": -12,
                    "type": "integer"
                },
                "result_ttl": {
                    "default": 20,
                    "format": "int32",
                    "maximum": 14400,
                    "minimum": 1,
                    "type": "integer"
                },
                "routing": {
                    "default": [],
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "matrix": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "distances": {
                                        "items": {
                                            "items": {
                                                "format": "int64",
                                                "minimum": -1,
                                                "type": "integer"
                                            },
                                            "maxItems": 9000,
                                            "minItems": 2,
                                            "type": "array",
                                            "uniqueItems": false
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    },
                                    "durations": {
                                        "items": {
                                            "items": {
                                                "format": "int64",
                                                "minimum": -1,
                                                "type": "integer"
                                            },
                                            "maxItems": 9000,
                                            "minItems": 2,
                                            "type": "array",
                                            "uniqueItems": false
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    },
                                    "waypoints": {
                                        "items": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "duration": {
                                                    "default": 0,
                                                    "format": "int32",
                                                    "maximum": 1440,
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "latitude": {
                                                    "format": "double",
                                                    "maximum": 90,
                                                    "minimum": -90,
                                                    "type": "number"
                                                },
                                                "longitude": {
                                                    "format": "double",
                                                    "maximum": 180,
                                                    "minimum": -180,
                                                    "type": "number"
                                                }
                                            },
                                            "required": [
                                                "latitude",
                                                "longitude"
                                            ],
                                            "type": "object"
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    }
                                },
                                "required": [
                                    "waypoints",
                                    "distances",
                                    "durations"
                                ],
                                "type": "object"
                            },
                            "traffic_jams": {
                                "items": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "length_additive": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 100000,
                                            "minimum": -100000,
                                            "type": "number"
                                        },
                                        "length_multiplier": {
                                            "default": 1,
                                            "format": "double",
                                            "maximum": 100,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "time_additive": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1440,
                                            "minimum": -1440,
                                            "type": "number"
                                        },
                                        "time_multiplier": {
                                            "default": 1,
                                            "format": "double",
                                            "maximum": 100,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "time_window": {
                                            "additionalProperties": false,
                                            "properties": {
                                                "from": {
                                                    "format": "date-time",
                                                    "type": "string"
                                                },
                                                "to": {
                                                    "format": "date-time",
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "from",
                                                "to"
                                            ],
                                            "type": "object"
                                        }
                                    },
                                    "required": [
                                        "time_window"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 24,
                                "minItems": 0,
                                "type": "array"
                            },
                            "transport_type": {
                                "default": "CAR",
                                "enum": [
                                    "CAR",
                                    "TRUCK",
                                    "CAR_GT",
                                    "TUK_TUK",
                                    "BICYCLE",
                                    "PEDESTRIAN",
                                    "PUBLIC_TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            }
                        },
                        "required": [
                            "transport_type",
                            "matrix"
                        ],
                        "type": "object"
                    },
                    "maxItems": 7,
                    "minItems": 0,
                    "type": "array"
                },
                "transport_factor": {
                    "default": [],
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "speed": {
                                "format": "double",
                                "maximum": 1000,
                                "minimum": 0.1,
                                "type": "number"
                            },
                            "transport_type": {
                                "default": "CAR",
                                "enum": [
                                    "CAR",
                                    "TRUCK",
                                    "CAR_GT",
                                    "TUK_TUK",
                                    "BICYCLE",
                                    "PEDESTRIAN",
                                    "PUBLIC_TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            }
                        },
                        "required": [
                            "transport_type",
                            "speed"
                        ],
                        "type": "object"
                    },
                    "maxItems": 7,
                    "minItems": 0,
                    "type": "array"
                }
            },
            "type": "object"
        }
    },
    "required": [
        "performer",
        "orders"
    ],
    "type": "object"
}'''