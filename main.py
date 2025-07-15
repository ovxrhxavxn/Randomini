import uvicorn

def main():
    
    uvicorn.run(

        'src.app:app'
    )

if __name__ == "__main__":
    main()
