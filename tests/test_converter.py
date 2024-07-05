import pytest
import json

from luis_json_converter.converter import process_entity

def test_process_entity():
    input_data = {
        "entities": [
            {
                "name": "Where",
                "children": [
                    {
                        "name": "WhereDatetimeV2",
                        "children": [],
                        "features": [{"modelName": "datetimeV2", "isRequired": True}]
                    },
                    {
                        "name": "WhereRange",
                        "children": [
                            {
                                "name": "WhereRangeDatetimeV2",
                                "children": [],
                                "features": [{"modelName": "datetimeV2", "isRequired": True}]
                            },
                            {
                                "name": "WhereRangeDimension",
                                "children": [],
                                "features": [{"modelName": "Dimensions", "isRequired": False}]
                            },
                            {
                                "name": "WhereRangeOrdering",
                                "children": [],
                                "features": [{"modelName": "_Order_expressions", "isRequired": False}]
                            }
                        ],
                        "features": []
                    },
                    {
                        "name": "WhereOperatorSumExact",
                        "children": [],
                        "features": []
                    }
                ]
            }
        ]
    }

    expected_output = {
        "entities": [
            {
                "name": "Where",
                "children": [
                    {
                        "name": "DatetimeV2",
                        "children": [],
                        "features": [{"modelName": "datetimeV2", "isRequired": True}]
                    },
                    {
                        "name": "Range",
                        "children": [
                            {
                                "name": "DatetimeV2",
                                "children": [],
                                "features": [{"modelName": "datetimeV2", "isRequired": True}]
                            },
                            {
                                "name": "Dimension",
                                "children": [],
                                "features": [{"modelName": "Dimensions", "isRequired": False}]
                            },
                            {
                                "name": "Ordering",
                                "children": [],
                                "features": [{"modelName": "_Order_expressions", "isRequired": False}]
                            }
                        ],
                        "features": []
                    },
                    {
                        "name": "SumExact",
                        "children": [],
                        "features": []
                    }
                ]
            }
        ]
    }

    # Processing the input data
    for entity in input_data['entities']:
        process_entity(entity, entity['name'])

    assert input_data == expected_output
