from dotenv import load_dotenv
from air import DistillerClient
import os

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))

distiller_client = DistillerClient(api_key=api_key)

project = "cricket"
distiller_client.create_project(config_path="config.yaml", project=project)
# response = distiller_client.interactive(project=project, uuid="rajneesh_uuid")
