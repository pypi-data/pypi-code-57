expected_results = {
        'pommes_poires no uncert': [[
            [None, 'Production de fruits', 'Production de pommes', 'Production de poires', 'Consommation', 'International'],  # noqa: E501
            ['Fruits', 45.0, 30.0, 15.0, None, 20.0],
            ['Pommes', 30.0, 30.0, None, None, 10.0],
            ['Poires', 15.0, None, 15.0, None, 10.0]
        ], [
            [None, 'Production de fruits', 'Production de pommes', 'Production de poires', 'Consommation', 'International'],  # noqa: E501
            ['Fruits', None, None, None, 45.0, 20.0],
            ['Pommes', None, None, None, 20.0, 20.0],
            ['Poires', None, None, None, 25.0, None]
        ]
        ],
        'simplified_example_fr no uncert': [[
             [None, 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'International'],
             ['P1', 98.4, None, None, None, None, None, None],
             ['P2', None, -1.0, None, None, None, None, 16.8],
             ['P3', None, None, 70.0, None, None, None, 4.2],
             ['P4', None, None, None, 74.4, 11.4, None, 4.9],
             ['P5', None, None, None, None, 16.2, None, 7.3]
        ], [
            [None, 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'International'],
            ['P1', None, -1.0, -1.0, None, None, None, None],
            ['P2', None, None, -1.0, 39.4, None, None, 5.8],
            ['P3', None, None, None, 35.0, 27.6, None, 11.6],
            ['P4', None, None, None, None, None, 80.6, 10.2],
            ['P5', None, None, None, None, None, 15.4, 8.1]
        ]
        ]
}
