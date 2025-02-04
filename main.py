from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

app = FastAPI(title="Number Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NumberResponse(BaseModel):
    number: Union[int, str]
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: Optional[int]
    fun_fact: str

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 0:
        return False
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 0:
        return False
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def get_properties(n: int) -> List[str]:
    """Get all properties of a number."""
    properties = []
    
    # Check if Armstrong (only for positive numbers)
    if n >= 0 and is_armstrong(n):
        properties.append("armstrong")
    
    # Check if odd/even
    properties.append("odd" if n % 2 else "even")
    
    return properties

def get_digit_sum(n: int) -> Optional[int]:
    """Calculate the sum of digits."""
    if n < 0:
        return None
    return sum(int(digit) for digit in str(abs(n)))

def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from the Numbers API."""
    if n < 0:
        return f"{n} is an uninteresting number."
        
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        else:
            return f"{n} is a number with interesting mathematical properties."
    except:
        return f"{n} is a number with interesting mathematical properties."

@app.get("/api/classify-number", response_model=Union[NumberResponse, ErrorResponse])
async def classify_number(number: Optional[str] = Query(None)):
    """Classify a number and return its properties."""
    # Check if number parameter is missing
    if number is None:
        return ErrorResponse(number="undefined")
        
    # Try to convert to integer
    try:
        num = int(number)
        
        return NumberResponse(
            number=num,
            is_prime=is_prime(num),
            is_perfect=is_perfect(num),
            properties=get_properties(num),
            digit_sum=get_digit_sum(num),
            fun_fact=get_fun_fact(num)
        )
    except ValueError:
        # For non-numeric inputs (alphabets or symbols)
        if number.isalpha():
            return ErrorResponse(number="alphabet")
        else:
            return ErrorResponse(number=number)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)