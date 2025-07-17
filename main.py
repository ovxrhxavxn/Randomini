import uvicorn

from src.config import server_config


def main():
    
    uvicorn.run(

        'src.app:app',
        host=server_config.host,
        port=server_config.port
    )

if __name__ == "__main__":
    main()