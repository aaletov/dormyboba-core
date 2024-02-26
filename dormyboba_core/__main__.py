import warnings
import uvicorn

warnings.filterwarnings("ignore", category=SyntaxWarning)

if __name__ == "__main__":
    uvicorn.run("dormyboba_core.app:app", host="0.0.0.0", port=8000, workers=1)
