FROM python:3.7
ADD requirements.txt /
ADD tags /tags
ADD data /data
ADD skills_generator.py /
ADD dataViz-v2.py /

RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","dataViz-v2.py"]
