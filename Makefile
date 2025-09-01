fastapi-build: 
			docker build --platform linux/amd64 -t negotiate_ai_app ./orchestration/fastapi
fastapi-start:
			cd ./orchestration/fastapi && docker compose up && cd ..
fastapi-stop:
			cd ./orchestration/fastapi && docker compose down && cd ..