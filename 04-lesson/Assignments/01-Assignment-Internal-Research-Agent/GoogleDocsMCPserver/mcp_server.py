import os
from mcp.server.fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define scopes for Google Docs and Drive
SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]


JSON_FILE_NAME = "Dummy-Google-console-credentials.json"


KEY_FILE = os.path.join(os.path.dirname(__file__), JSON_FILE_NAME)

def get_google_services():
   
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError(
            f"Service account key file '{KEY_FILE}' not found. "
        )
    
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return docs_service, drive_service

def read_structural_elements(elements) -> str:
  
    text = ""
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements', [])
            for elem in elements:
                if 'textRun' in elem:
                    text += elem.get('textRun').get('content', '')
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows', []):
                for cell in row.get('tableCells', []):
                    text += read_structural_elements(cell.get('content', []))
        elif 'tableOfContents' in value:
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content', []))
    return text


mcp_server = FastMCP("google-docs-server")

@mcp_server.tool()
async def list_documents() -> str:
   
    """Lists all Google Docs available to the service account, along with their IDs."""
   
    try:
        _, drive_service = get_google_services()
        q = "mimeType = 'application/vnd.google-apps.document'"
        results = drive_service.files().list(
            q=q, 
            spaces='drive', 
            fields='files(id, name)',
            pageSize=50
        ).execute()
        files = results.get('files', [])
        if not files:
            return "No Google Docs available."
        response = "Available Google Docs:\n"
        for f in files:
            response += f"- Name: {f['name']} (ID: {f['id']})\n"
        return response
    except Exception as e:
        return f"Error listing docs: {str(e)}"

@mcp_server.tool()
async def read_google_doc(doc_id: str) -> str:
   
    """Reads the text content of a Google Doc given its Document ID."""
    try:
        docs_service, _ = get_google_services()
        doc = docs_service.documents().get(documentId=doc_id).execute()
        doc_content = doc.get('body').get('content', [])
        text = read_structural_elements(doc_content)
        return f"Document Title: {doc.get('title')}\n\nContent:\n{text}"
    except Exception as e:
        return f"Error reading document {doc_id}: {str(e)}"

@mcp_server.tool()
async def search_insurance_docs(query: str) -> str:
   
    """Searches Google Drive for Google Docs matching the query (useful for finding insurance policies, feedback, etc.)."""
    try:
        _, drive_service = get_google_services()
     
        q = f"mimeType = 'application/vnd.google-apps.document' and name contains '{query}'"
        results = drive_service.files().list(
            q=q, 
            spaces='drive', 
            fields='files(id, name)',
            pageSize=10
        ).execute()
        
        files = results.get('files', [])
        if not files:
            return f"No Google Docs found matching query '{query}'."
        
        response = "Found documents:\n"
        for f in files:
            response += f"- Name: {f['name']} (ID: {f['id']})\n"
        return response
    except Exception as e:
        return f"Error searching documents: {str(e)}"


app = mcp_server.sse_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)