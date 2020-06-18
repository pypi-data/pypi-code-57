from environs import Env


env = Env()


class Settings:
    BUCKET = env.str('BUCKET', 'bucket-name')
    DAS_URL = env.str('DAS_URL', 'https://www.akerbp.com')
    LOG_LEVEL = env.str('LOG_LEVEL', 'INFO')
    SERVICE_DISCOVERY_URL = env.str('SERVICE_DISCOVERY_URL', 'https://www.akerbp.com')
    SWAP_API_TOKEN = env.str('SWAP_API_TOKEN')
    UBL_URL = env.str('UBL_URL', 'https://www.akerbp.com')
