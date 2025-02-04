from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
from typing import List, Dict, Union
from pydantic import BaseModel

app = FastAPI(title="Number Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 0:  # Handle negative numbers
        return False
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 0:  # Handle negative numbers
        return False
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    if n < 0:  # Handle negative numbers
        return False
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def get_properties(n: int) -> List[str]:
    """Get all properties of a number."""
    properties = []
    
    # Check if Armstrong
    if is_armstrong(n):
        properties.append("armstrong")
    
    # Check if odd/even
    properties.append("odd" if n % 2 else "even")
    
    return properties

def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(n))

def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        else:
            return f"{n} is a number with interesting mathematical properties."
    except:
        return f"{n} is a number with interesting mathematical properties."

@app.get("/api/classify-number", response_model=Union[NumberResponse, ErrorResponse])
async def classify_number(number: str):
    """Classify a number and return its properties."""
    try:
        num = int(number)
    except ValueError:
        return ErrorResponse(number=number)
    
    # Get all properties
    properties = get_properties(num)
    
    return NumberResponse(
        number=num,
        is_prime=is_prime(num),
        is_perfect=is_perfect(num),
        properties=properties,
        digit_sum=get_digit_sum(num),
        fun_fact=get_fun_fact(num)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)