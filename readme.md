# HNG Stage 1 API

# Number Classification API

A FastAPI-based service that analyzes numbers and returns their mathematical properties along with interesting facts.

## Features

- Number classification (prime, perfect, Armstrong)
- Digit sum calculation
- Fun facts about numbers using the Numbers API
- CORS support
- Input validation
- Error handling

## API Specification

### Endpoint

```
GET /api/classify-number?number={number}
```

### Success Response (200 OK)

```json
{
	"number": 371,
	"is_prime": false,
	"is_perfect": false,
	"properties": ["armstrong", "odd"],
	"digit_sum": 11,
	"fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)

```json
{
	"number": "alphabet",
	"error": true
}
```

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/Jcolejeff/BE-stage-2
cd number-classifier-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn main:app --reload
```

## Dependencies

- FastAPI
- Uvicorn
- Pydantic
- Requests

## Running Tests

```bash
pytest tests/
```

## Deployment

The API is deployed at: ``

## Performance

- Average response time: < 500ms
- Handles concurrent requests efficiently

## Error Handling

The API implements robust error handling:

- Invalid input validation
- Numbers API service unavailability
- Internal server errors

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
