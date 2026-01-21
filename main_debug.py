import ok
from src.config import config

if __name__ == '__main__':
    config = config
    config['debug'] = True
    ok = ok.OK(config)
    ok.start()
