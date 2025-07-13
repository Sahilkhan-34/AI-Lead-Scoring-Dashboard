# AI Lead Scoring Dashboard

A machine learning-powered dashboard for scoring sales leads based on various factors including credit score, age, family background, and income. The system includes both initial ML-based scoring and rule-based re-ranking based on lead comments.

## Features

- Machine learning-based lead scoring
- Rule-based score re-ranking based on comment analysis
- Interactive web dashboard
- Real-time scoring API
- Local storage for scored leads history

## Prerequisites

- Python 3.8 or higher
- Node.js (for serving the frontend locally)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-lead-scoring-dashboard.git
cd ai-lead-scoring-dashboard
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Train the model first:
```bash
python Backend/train_model.py
```

2. Start the FastAPI backend:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

3. Serve the frontend (using Python's built-in server):
```bash
# Navigate to the docs directory
cd docs

# Start Python's built-in server
python -m http.server 3000
```

4. Open your browser and visit:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
ai-lead-scoring-dashboard/
├── Backend/
│   ├── lead_data.csv
│   ├── train_model.py
│   └── model.pkl
├── docs/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── app.py
├── requirements.txt
└── README.md
```

## API Endpoints

- `POST /score`: Score a new lead
- `GET /leads`: Retrieve all scored leads

## Configuration

To modify the API URL for production:
1. Open `docs/script.js`
2. Update the `API_URL` constant with your deployed backend URL

## Local Development

1. Make sure to update the CORS settings in `app.py` if needed
2. The frontend automatically saves scored leads to localStorage
3. The model is trained on synthetic data and can be retrained with your own data

## Troubleshooting

1. If the model file is not found:
```bash
python Backend/train_model.py
```

2. If CORS errors occur, verify the `origins` list in `app.py`

3. If the API is not responding:
- Check if the backend server is running
- Verify the API_URL in script.js matches your backend URL

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request