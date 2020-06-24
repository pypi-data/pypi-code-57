PLAN_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "info": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "planning_time": {
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 0,
                    "type": "integer"
                },
                "result_version": {
                    "format": "int32",
                    "maximum": 1159116,
                    "minimum": 0,
                    "type": "integer"
                },
                "status": {
                    "enum": [
                        "WAITING",
                        "IN_PROGRESS",
                        "FINISHED_IN_TIME",
                        "FINISHED_OUT_OF_TIME",
                        "CANCELED",
                        "FAILED"
                    ],
                    "type": "string"
                },
                "waiting_time": {
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 0,
                    "type": "integer"
                }
            },
            "required": [
                "status"
            ],
            "type": "object"
        },
        "progress": {
            "format": "int32",
            "maximum": 100,
            "minimum": 0,
            "type": "integer"
        },
        "statistics": {
            "additionalProperties": false,
            "nullable": true,
            "properties": {
                "total_statistics": {
                    "additionalProperties": false,
                    "nullable": true,
                    "properties": {
                        "capacity_utilization": {
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
                        "cost": {
                            "format": "double",
                            "minimum": 0,
                            "type": "number"
                        },
                        "measurements": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "arriving_time": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "departure_time": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "distance": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "driving_time": {
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
                                },
                                "total_time": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "waiting_time": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "working_time": {
                                    "format": "int32",
                                    "minimum": 0,
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "driving_time",
                                "waiting_time",
                                "working_time",
                                "arriving_time",
                                "departure_time",
                                "total_time",
                                "distance"
                            ],
                            "type": "object"
                        },
                        "orders_count": {
                            "format": "int32",
                            "maximum": 9000,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "performers_count": {
                            "format": "int32",
                            "maximum": 9000,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "reward": {
                            "format": "double",
                            "minimum": 0,
                            "type": "number"
                        }
                    },
                    "required": [
                        "cost",
                        "reward",
                        "measurements",
                        "orders_count",
                        "performers_count"
                    ],
                    "type": "object"
                },
                "trips_statistics": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "max_load": {
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
                                    "count": {
                                        "format": "int32",
                                        "minimum": 0,
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "count",
                                    "capacity"
                                ],
                                "type": "object"
                            },
                            "statistics": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "capacity_utilization": {
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
                                    "cost": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "measurements": {
                                        "additionalProperties": false,
                                        "nullable": true,
                                        "properties": {
                                            "arriving_time": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "departure_time": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "distance": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "driving_time": {
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
                                            },
                                            "total_time": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "waiting_time": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "working_time": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "driving_time",
                                            "waiting_time",
                                            "working_time",
                                            "arriving_time",
                                            "departure_time",
                                            "total_time",
                                            "distance"
                                        ],
                                        "type": "object"
                                    },
                                    "orders_count": {
                                        "format": "int32",
                                        "maximum": 9000,
                                        "minimum": 0,
                                        "type": "integer"
                                    },
                                    "performers_count": {
                                        "format": "int32",
                                        "maximum": 9000,
                                        "minimum": 0,
                                        "type": "integer"
                                    },
                                    "reward": {
                                        "format": "double",
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "cost",
                                    "reward",
                                    "measurements",
                                    "orders_count",
                                    "performers_count"
                                ],
                                "type": "object"
                            },
                            "stop_statistics": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "current_load": {
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
                                                "count": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "count",
                                                "capacity"
                                            ],
                                            "type": "object"
                                        },
                                        "demand_ids": {
                                            "items": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "type": "array"
                                        },
                                        "download": {
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
                                                "count": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "count",
                                                "capacity"
                                            ],
                                            "type": "object"
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
                                        "location_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "measurements": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "arriving_time": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "departure_time": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "distance": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "driving_time": {
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
                                                },
                                                "total_time": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "waiting_time": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "working_time": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "driving_time",
                                                "waiting_time",
                                                "working_time",
                                                "arriving_time",
                                                "departure_time",
                                                "total_time",
                                                "distance"
                                            ],
                                            "type": "object"
                                        },
                                        "upload": {
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
                                                "count": {
                                                    "format": "int32",
                                                    "minimum": 0,
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "count",
                                                "capacity"
                                            ],
                                            "type": "object"
                                        }
                                    },
                                    "required": [
                                        "location",
                                        "measurements"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 9000,
                                "minItems": 0,
                                "type": "array"
                            },
                            "total_load": {
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
                                    "count": {
                                        "format": "int32",
                                        "minimum": 0,
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "count",
                                    "capacity"
                                ],
                                "type": "object"
                            },
                            "trip_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            }
                        },
                        "required": [
                            "trip_key",
                            "statistics",
                            "stop_statistics"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 0,
                    "type": "array"
                }
            },
            "required": [
                "total_statistics",
                "trips_statistics"
            ],
            "type": "object"
        },
        "tracedata": {
            "additionalProperties": false,
            "properties": {
                "code": {
                    "maxLength": 256,
                    "minLength": 3,
                    "type": "string"
                }
            },
            "required": [
                "code"
            ],
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
        },
        "unplanned_orders": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "order": {
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
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "order"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "validations": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "entity_key": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "entity_type": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "info": {
                        "type": "string"
                    },
                    "type": {
                        "enum": [
                            "info",
                            "warning",
                            "error"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "info"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        }
    },
    "required": [
        "trips"
    ],
    "type": "object"
}'''