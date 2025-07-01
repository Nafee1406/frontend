from fastapi import FastAPI
from supabase import create_client


app = FastAPI()
supabase_url="https://ctbpovmhgakrageabszx.supabase.co"
supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0YnBvdm1oZ2FrcmFnZWFic3p4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExODM0OTksImV4cCI6MjA2Njc1OTQ5OX0.5m2mHTmV3rh8xPSPctGl20h1zSna8ZYd3wgplxMuMI0"
client = create_client(supabase_url,supabase_key)

@app.get("/")
def read_users():
    result = client.table("users").select("*").execute()
    return result.data

