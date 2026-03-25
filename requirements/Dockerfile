FROM ollama/ollama
# Sleep to wait for ollama server to be ready
RUN ollama serve & sleep 5 && ollama pull phi4
RUN apt-get update && apt-get install python3 python3-pip -y 
RUN echo 'alias python=python3' >> ~/.bashrc
COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages
WORKDIR /entry
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./requirements/entrypoint.sh"]