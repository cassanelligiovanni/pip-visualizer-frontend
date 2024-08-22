from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/api/package/{name}")
async def get_package_version(name: str):
    url = f"https://pypi.org/project/{name}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            header = soup.find("h1", class_="package-header__name")
            if header:
                package_version = header.text.strip().split()[-1]
                return {"package": name, "version": package_version}
            else:
                raise HTTPException(status_code=404, detail="Package version not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Package not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
