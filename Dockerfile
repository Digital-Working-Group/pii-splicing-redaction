FROM ollama/ollama
# Sleep to wait for ollama server to be ready
RUN ollama serve & sleep 5 && ollama pull llama3.2 && ollama pull phi4 && ollama pull llama3.3
RUN apt-get update && apt-get install python3 python3-pip -y && apt-get clean autoclean && rm -rf /var/lib/apt/lists/*
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip3 install -r requirements.txt
ADD app /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["-h"]
