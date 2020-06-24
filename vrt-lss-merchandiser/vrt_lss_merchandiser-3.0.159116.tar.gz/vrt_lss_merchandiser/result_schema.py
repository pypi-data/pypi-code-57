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
        "timetable": {
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
        "unplanned_orders": {
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
            "type": "array"
        }
    },
    "type": "object"
}'''