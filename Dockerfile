# 1. Rasmiy yengil Python imijidan foydalanamiz
FROM python:3.11-slim

# 2. Docker ichidagi terminal har doim xatolarni srazi chiqarishi uchun sozlama
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Docker ichida loyiha qaysi papkada turishini belgilaymiz
WORKDIR /app

# 4. Tizim tizimidagi kerakli paketlarni yangilab olamiz
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Kutubxonalar ro'yxatini ko'chirib o'tkazamiz va o'rnatamiz
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Loyihaning qolgan barcha kodlarini ko'chiramiz
COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]