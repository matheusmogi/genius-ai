from loader import WebLoader, YouTubeLoader, PDFLoader, CsvLoader
from source import WebInput, Youtube, PDFInput, CSVInput

def get_source():
    sources = {
        'Web': {"Source": WebInput(), "Loader": WebLoader()},
        'Youtube': {"Source": Youtube(), "Loader": YouTubeLoader()},
        'PDF': {"Source": PDFInput(), "Loader": PDFLoader()},
        'CSV': {"Source": CSVInput(), "Loader": CsvLoader()},
    }
    return sources