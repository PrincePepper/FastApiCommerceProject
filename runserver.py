import argparse

import uvicorn

from app.core.config import settings

# init parser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--runserver', action='store_true')
args = parser.parse_args()


def main():
    if args.runserver:
        # Popen(['python', '-m', 'https_redirect'])
        uvicorn.run(
            'app.main:app',
            port=settings.SERVER_PORT,
            log_level='info',
            workers=int(settings.WORKERS),
            host=settings.SERVER_HOST,
            reload=True
        )


if __name__ == '__main__':
    main()
