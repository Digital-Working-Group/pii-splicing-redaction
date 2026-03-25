FROM ollama/ollama
# Sleep to wait for ollama server to be ready
RUN ollama serve & sleep 5 && ollama pull phi4
#RUN apt-get update && apt-get install -y dos2unix && apt-get install python3 python3-pip -y && apt-get clean autoclean && rm -rf /var/lib/apt/lists/*
#RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip3 install -r requirements.txt
WORKDIR /entry
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./requirements/entrypoint.sh"]
