FROM python:3.8
COPY . /usr/app/
EXPOSE 8501
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD [ "streamlit" , "run", "streamlit_app.py"]

