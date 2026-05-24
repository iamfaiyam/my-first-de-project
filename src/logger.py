from datetime import datetime

def log(message: str) -> None: 
    print(f"{datetime.now()} - {message}")