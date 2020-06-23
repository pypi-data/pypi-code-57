
import sidemash_sdk.SidemashClient
import sidemash_sdk.Auth


sdm = SidemashClient(Auth(token = "1234", privateKey = "****"))
sdm.streamSquare.create(CreateStreamSquareForm(size = StreamSquare.Size.M, isElastic = false))