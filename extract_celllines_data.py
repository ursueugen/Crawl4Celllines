from pathlib import Path
from ftplib import FTP
import json


DATA_DIR_PATH = Path('data')
CELLOSAURUS_DIR_PATH = DATA_DIR_PATH / 'cellosaurus'
ECACC_DIR_PATH = DATA_DIR_PATH / 'ecacc'


def create_directories():
    Path(DATA_DIR_PATH).mkdir(parents=True, exist_ok=True)
    Path(CELLOSAURUS_DIR_PATH).mkdir(parents=True, exist_ok=True)


def extract_cellosaurus(force_extraction=False):

    if ( len(list(CELLOSAURUS_DIR_PATH.rglob('*'))) == 12
         and (not force_extraction)):
        print('extract_cellosaurus: Cellosaurus data is found. Not downloading.')

    else:
        EXPASY_FTP_URL = 'ftp.expasy.org'
        PATH_TO_CELLOSAURUS = 'databases/cellosaurus'

        with FTP(EXPASY_FTP_URL) as ftp:
            ftp.login()  # anonymous access
            ftp.cwd(PATH_TO_CELLOSAURUS)
            cellosaurus_filenames = ftp.nlst()
            print(f"extract_cellosaurus: Identified {len(cellosaurus_filenames)} files")
            for fn in cellosaurus_filenames:
                with open(CELLOSAURUS_DIR_PATH / fn, 'wb') as file_handle:
                    ftp.retrbinary('RETR {}'.format(fn), file_handle.write)
                print(f"extract_cellosaurus: Downloaded {fn}")

        print(f"extract_cellosaurus: Successfully downloaded all.")


def scrape_atcc():    
    # This one requires more advanced solutions (like selenium)
    #  because it's rendering the html using javascript. Info
    #  not to be found in the html obtained via http.
    pass


def scrape_ecacc():

    ECACC_DB_PATH = ECACC_DIR_PATH / 'ecacc_celllines_db.json'

    if (ECACC_DB_PATH).is_file():
        print('scrape_ecacc: Found ecacc_celllines_db.json')
        
        with open(ECACC_DB_PATH.__str__(), 'r') as f:
            ecacc_cells = json.load(f)
            print(f'scrape_ecacc: Num records = {len(ecacc_cells)}')
    else:
        print('Scrap first.')
        raise NotImplementedError('Add call to scrapper module')


if __name__ == '__main__':
    create_directories()
    extract_cellosaurus()
    scrape_atcc()
    scrape_ecacc()