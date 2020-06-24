PLAN_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "hardlinks": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "links": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "entity_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "type": {
                                    "enum": [
                                        "ORDER",
                                        "SHIFT"
                                    ],
                                    "nullable": false,
                                    "type": "string"
                                }
                            },
                            "required": [
                                "type",
                                "entity_key"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 2,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "links"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "locations": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "load_windows": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "gates_count": {
                                    "default": 0,
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
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
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
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
                    "transport_restrictions": {
                        "items": {
                            "maxLength": 256,
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
                    "location"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "orders": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
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
                        "minItems": 0,
                        "type": "array"
                    },
                    "demands": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "demand_type": {
                                    "enum": [
                                        "PICKUP",
                                        "DROP",
                                        "WORK"
                                    ],
                                    "nullable": false,
                                    "type": "string"
                                },
                                "key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "possible_events": {
                                    "items": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "duration": {
                                                "default": 5,
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "location_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "reward": {
                                                "format": "double",
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
                                            "location_key",
                                            "duration",
                                            "time_window",
                                            "reward"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 10,
                                    "minItems": 1,
                                    "type": "array"
                                },
                                "precedence_in_order": {
                                    "default": 0,
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "precedence_in_trip": {
                                    "default": 0,
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "target_cargos": {
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
                                "demand_type",
                                "possible_events"
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
                    "order_features": {
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
                    "order_restrictions": {
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
                    "performer_blacklist": {
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
                    "performer_restrictions": {
                        "items": {
                            "maxLength": 256,
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
                    "demands"
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
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "max_work_shifts": {
                        "default": 31,
                        "format": "int32",
                        "maximum": 31,
                        "minimum": 1,
                        "type": "integer"
                    },
                    "own_transport_type": {
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
                    },
                    "performer_features": {
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
                    "transport_restrictions": {
                        "items": {
                            "maxLength": 256,
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
                    "key"
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
                    "finish_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "resource_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "shift_type": {
                        "enum": [
                            "PERFORMER",
                            "TRANSPORT"
                        ],
                        "nullable": false,
                        "type": "string"
                    },
                    "start_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "tariff": {
                        "additionalProperties": false,
                        "properties": {
                            "constraints": {
                                "items": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "cost_per_unit": {
                                            "format": "double",
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "stage_length": {
                                            "format": "double",
                                            "minimum": 1,
                                            "type": "number"
                                        }
                                    },
                                    "required": [
                                        "stage_length",
                                        "cost_per_unit"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 100,
                                "minItems": 1,
                                "type": "array"
                            },
                            "cost_per_shift": {
                                "format": "double",
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "cost_per_shift",
                            "constraints"
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
                    "key",
                    "shift_type",
                    "resource_key",
                    "availability_time",
                    "working_time",
                    "tariff"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "transports": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "boxes": {
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
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "performer_restrictions": {
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
                    "transport_features": {
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
                    "key"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "trips": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "actions": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "cargo_placements": {
                                    "items": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "box_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "cargo_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "box_key",
                                            "cargo_key"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array"
                                },
                                "demand_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "location_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "order_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "todolist": {
                                    "items": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "job_time": {
                                                "format": "date-time",
                                                "type": "string"
                                            },
                                            "job_type": {
                                                "enum": [
                                                    "LOCATION_ARRIVAL",
                                                    "READY_TO_WORK",
                                                    "START_WORK",
                                                    "FINISH_WORK",
                                                    "LOCATION_DEPARTURE"
                                                ],
                                                "nullable": false,
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "job_type",
                                            "job_time"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 1,
                                    "type": "array"
                                }
                            },
                            "required": [
                                "order_key",
                                "demand_key",
                                "location_key",
                                "todolist"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 1,
                        "type": "array"
                    },
                    "assigned_shifts": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "shift_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "shift_time": {
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
                                "shift_key",
                                "shift_time"
                            ],
                            "type": "object"
                        },
                        "maxItems": 2,
                        "minItems": 2,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
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
                    "assigned_shifts"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        }
    },
    "required": [
        "locations",
        "orders",
        "performers",
        "transports",
        "shifts"
    ],
    "type": "object"
}'''