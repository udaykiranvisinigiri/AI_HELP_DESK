import psycopg2
DATABASE_URL = "postgresql://postgres:kiransmiley%4018@localhost:5432/ai_helpdesk"
#DATABASE_URL = "postgresql://postgres:b.XJ04RnYq2Jlrf8knFlFHjWHkzCaa9n@crossover.proxy.rlwy.net:31864/railway"

def get_connection():
    return psycopg2.connect(DATABASE_URL)