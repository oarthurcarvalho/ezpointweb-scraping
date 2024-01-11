import os

from src.get_data import DataScraper
from src.handle_data import ExtractorXl
from src.upload_file import SharepointUploader
from src.utils import gerar_datas, get_files

if __name__ == '__main__':
#    datas = gerar_datas()
#
#    for range in datas:
#        datafim, datainicio = range
#        data_scraper = DataScraper(datainicio, datafim)
#        data_scraper.login()
#        data_scraper.download_report()
#        data_scraper.close()

    files = get_files()
    excel_extractor = ExtractorXl()

    for file in files:
        if os.path.exists(file):
            excel_extractor.process_data(file)
            os.remove(file)

    excel_extractor.save_to_csv('storage/tmk-data.csv')

    uploader = SharepointUploader()
    uploader.upload_file()
