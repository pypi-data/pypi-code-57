PLAN_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "delivery_settings": {
            "additionalProperties": false,
            "properties": {
                "restrict_middle_warehouses": {
                    "default": true,
                    "type": "boolean"
                },
                "restrict_multiple_order_types": {
                    "default": false,
                    "type": "boolean"
                },
                "restrict_multiple_warehouses": {
                    "default": true,
                    "type": "boolean"
                }
            },
            "type": "object"
        },
        "orders": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "blacklist": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "cargos": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "capacity": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "capacity_x": {
                                            "default": 0,
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_y": {
                                            "default": 0,
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_z": {
                                            "default": 0,
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "mass": {
                                            "default": 1,
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "volume": {
                                            "default": 0,
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        }
                                    },
                                    "required": [
                                        "mass"
                                    ],
                                    "type": "object"
                                },
                                "height": {
                                    "default": 0,
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "length": {
                                    "default": 0,
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "max_storage_time": {
                                    "default": 14400,
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "restrictions": {
                                    "items": {
                                        "maxLength": 256,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 100,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "width": {
                                    "default": 0,
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                }
                            },
                            "required": [
                                "key",
                                "capacity"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 1,
                        "type": "array"
                    },
                    "cost": {
                        "additionalProperties": false,
                        "properties": {
                            "penalty": {
                                "additionalProperties": false,
                                "properties": {
                                    "max_value": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "period": {
                                        "format": "int32",
                                        "maximum": 1440,
                                        "minimum": 1,
                                        "type": "integer"
                                    },
                                    "start_time": {
                                        "format": "date-time",
                                        "type": "string"
                                    },
                                    "value": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "start_time",
                                    "period",
                                    "value",
                                    "max_value"
                                ],
                                "type": "object"
                            },
                            "reward": {
                                "format": "double",
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "reward"
                        ],
                        "type": "object"
                    },
                    "customer": {
                        "additionalProperties": false,
                        "properties": {
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
                            "time_windows": {
                                "items": {
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
                                "maxItems": 100,
                                "minItems": 0,
                                "type": "array"
                            }
                        },
                        "required": [
                            "location",
                            "time_windows"
                        ],
                        "type": "object"
                    },
                    "customer_duration": {
                        "default": 0,
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "restrictions": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "type": {
                        "default": "DROP",
                        "enum": [
                            "DROP",
                            "PICKUP"
                        ],
                        "nullable": false,
                        "type": "string"
                    },
                    "warehouse_duration": {
                        "default": 0,
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "warehouse_keys": {
                        "items": {
                            "maxLength": 1024,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "warehouse_keys",
                    "customer",
                    "cargos"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "performers": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "box": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "capacity": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "capacity_x": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_y": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_z": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "mass": {
                                        "default": 1,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "volume": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "mass"
                                ],
                                "type": "object"
                            },
                            "features": {
                                "items": {
                                    "maxLength": 256,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "height": {
                                "default": 0,
                                "format": "double",
                                "minimum": 0,
                                "type": "number"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "length": {
                                "default": 0,
                                "format": "double",
                                "minimum": 0,
                                "type": "number"
                            },
                            "max_size": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "capacity_x": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_y": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_z": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "mass": {
                                        "default": 1,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "volume": {
                                        "default": 0,
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "mass"
                                ],
                                "type": "object"
                            },
                            "width": {
                                "default": 0,
                                "format": "double",
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "key",
                            "capacity"
                        ],
                        "type": "object"
                    },
                    "count": {
                        "default": 1,
                        "format": "int32",
                        "maximum": 5000,
                        "minimum": 1,
                        "type": "integer"
                    },
                    "features": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
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
                    "shifts"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
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
        },
        "trips": {
            "items": {
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
                                "order_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
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
                                },
                                "warehouse_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                }
                            },
                            "required": [
                                "order_key",
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
                    "performer_key": {
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
                            "maxLength": 1024,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key",
                    "performer_key",
                    "trip_time"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "warehouses": {
            "items": {
                "additionalProperties": false,
                "properties": {
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
                    "work_windows": {
                        "items": {
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
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "location"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        }
    },
    "required": [
        "warehouses",
        "orders",
        "performers"
    ],
    "type": "object"
}'''