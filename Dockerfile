FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
<<<<<<< HEAD
RUN pip install -r requirements.txt
COPY . .
CMD ["python","AppFlask.py"]
=======
RUN pip install --no-cache-dir -r requirements.txt --ignore-installed
COPY . .
CMD ["python","AppFlask.py"]
>>>>>>> 6b5fdff430800f6d8b682f66943e7a16e6042fbe
