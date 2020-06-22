"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""


class Key:
    def __init__(self, id, private_key_str):
        self.id = id
        self.private_key_str = private_key_str


class KeyPair:
    def __init__(self, private_key_str, public_key_str):
        self.private_key_str = private_key_str
        self.public_key_str = public_key_str


class Settings:
    # API url to dialogue with a Katena network
    api_url = "http://127.0.0.1:5000/api/v1"

    # Katena network id
    chain_id = "katena-chain-test"

    # Number of transactions the API should return
    tx_per_page = 10

    # Sample transaction ids used in examples
    # If one id is already used on the Katena test network, feel free to change these values
    certificate_id = "ce492f92-a529-40c1-91e9-2af71e74ebea"
    secret_id = "3b1cfd5f-d0fe-478c-ba30-17817e29611e"
    key_id = "9941bc28-4033-4d5a-a337-76b640223de2"

    # Dummy company committed on chain
    class Company:
        # Unique company identifier on a Katena network
        bcid = "abcdef"

        # Dummy users with their keys to sign transactions
        ed25519_keys = {
            "alice": Key("36b72ca9-fd58-44aa-b90d-5a855276ff82",
                         "7C67DeoLnhI6jvsp3eMksU2Z6uzj8sqZbpgwZqfIyuCZbfoPcitCiCsSp2EzCfkY52Mx58xDOyQLb1OhC7cL5A=="),
            "bob": Key("7cf17643-5567-4dfa-9b0c-9cd19c45177a",
                       "3awdq5HUZ2fgV2fM6sbV1yJKIvuTV2OZ5AMfes4ftHUiOpqsicnv+67vLfKLwWR/Bh/hNbJaq6fziXoh+oqxRQ=="),
            "carla": Key("236f8028-bb87-4c19-b6e0-cbcaea35e764",
                         "p2T1gRu2HHdhcsTVEk6VwpJRkLahvnLsi9miSS1Yg4PSk6jrTRFvtoPzi2z6yn+Ul9+niTHBUvbskbQ2TkDxmQ=="),
        }

    # Off chain samples data to do off chain operations
    class OffChain:
        # Dummy users with their keys to sign off-chain data
        ed25519_keys = {
            "david": KeyPair("aGya1W2C2bfu1bMA+wJ8kbpZePjKprv4t93EhX+durqOksFaT9pC0054jFeKYFyGzi+1gCp1NZAeCsG/yQEJWA==",
                             "jpLBWk/aQtNOeIxXimBchs4vtYAqdTWQHgrBv8kBCVg="),
        }

        # Dummy users with their keys to seal/open nacl boxes to share secret information
        x25519_keys = {
            "alice": KeyPair("nyCzhimWnTQifh6ucXLuJwOz3RgiBpo33LcX1NjMAsP1ZkQcdlDq64lTwxaDx0lq6LCQAUeYywyMUtfsvTUEeQ==",
                             "9WZEHHZQ6uuJU8MWg8dJauiwkAFHmMsMjFLX7L01BHk="),
            "bob": KeyPair("quGBP8awD/J3hjSvwGD/sZRcMDks8DPz9Vw0HD4+zecqJP0ojBoc4wQtyq08ywxUksTkdz0/rQNkOsEZBwqWTw==",
                           "KiT9KIwaHOMELcqtPMsMVJLE5Hc9P60DZDrBGQcKlk8="),
        }
