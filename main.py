import uvicorn

def main():
    
    uvicorn.run(

        'src.app:app',
        reload=True
    )

if __name__ == "__main__":
    main()
