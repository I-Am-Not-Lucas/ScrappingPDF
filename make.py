import hashlib
from ..bromo.bromo import Interation
import os
import sys
import time
import json
import logging as log
import platform

from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.firefox.options import Options as GeckoOptions

sys.path.append(os.getcwd())


os.environ['WDM_LOG'] = str(log.NOTSET)
os.environ['TMPDIR'] = 'tmp'


class Driver(Interation):

    def __init__(self, teste=False):

        driver = 'chrome'

        driver_path = '/var/www/clients/client17/web42/home/timesaver_ts/web/totem/config/driver/geckodriver'
        # print(platform.system())

        architecture = platform.architecture()
        is_windows_64bit = platform.system() == 'Windows' and '64bit' in architecture
        is_windows_32bit = platform.system() == 'Windows' and '32bit' in architecture

        if platform.system() == 'Windows':
            if is_windows_64bit:
                driver_path = r'./chromedriver.exe'  # Caminho para o driver no Windows

            else:
                driver_path = r'config\driver\chromedriver32.exe'
            driver_path = r'licitacoes/src/bot/drivers/chromedriver.exe'

        driver_path = os.path.normpath(driver_path)

        if driver == 'chrome':
            # driver_path ='/var/www/clients/client17/web42/home/timesaver_ts/web/totem/config/driver/chromedriver'
            # driver_path = '/usr/bin/google-chrome'

            self.make_chrome(driver_path)

        elif driver == 'mozilla':
            driver_path = r'licitacoes\src\bot\drivers\geckodriver.exe'
            self.make_mozilla(driver_path)

        super().__init__(self.driver)

        if not teste:
            # self.driver.minimize_window()
            pass

        # self.driver.get('https://timesaver.com.br/controller/read/senhas?empresa=stenci&id=1')

    def make_chrome(self, driver_path):

        caminho_completo = os.path.join(os.getcwd(), driver_path)
        # print(caminho_completo)

        service = ChromeService(executable_path=caminho_completo)

        # service = ChromeService(executable_path=ChromeDriverManager().install())

        # service = ChromeService(executable_path=ChromeDriverManager().install())
        options = ChromeOptions()
        # options.binary_location = os.getcwd() + driver_path
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.add_argument('--log-level=4')
        options.add_argument("--wait-for-connection=50000")

        # options.add_argument('--log-path=/var/www/clients/client17/web42/home/timesaver_ts/web/totem/logs/chromedriver.log')
        options.add_argument(
            f'--log-path={os.getcwd()}/tmp/logs/chromedriver.log')

        # options.add_argument('--headless')
        # Desativa notificações
        options.add_argument('--disable-notifications')
        # Desativa o carregamento de imagens
        options.add_argument('--blink-settings=imagesEnabled=false')
        # Desativa a execução de extensões do Chrome
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        # '--enable-logging')
        options.add_argument("--safebrowsing-disable-download-protection")
        # options.add_experimental_option('prefs',
        #                                 {'download.prompt_for_download': False,
        #                                 #  'profile.default_content_setting_values.notifications': 2,
        #                                 #  'profile.default_content_setting_values.automatic_downloads': 1,
        #                                  'download.default_directory': os.path.join(os.getcwd(), '/editais'),
        #                                  "download.directory_upgrade": True,
        #                                  "safebrowsing.enabled": True
        #                                  }
        #                                 )

        options.add_experimental_option('prefs',
                                        {'download.prompt_for_download': False,
                                         'profile.default_content_setting_values.notifications': 2,
                                         'profile.default_content_setting_values.automatic_downloads': 1,
                                         'download.default_directory': os.path.join(os.getcwd(), 'editais'),}
                                        )

        random_hash = hashlib.md5(os.urandom(32)).hexdigest()
        user_data_dir = f"{os.getcwd()}/tmp/data/{random_hash}"
        options.add_argument(f"--user-data-dir={user_data_dir}")
        # options.add_argument("--remote-debugging-port=9222")

        options.page_load_strategy = 'normal'
        # options.page_load_strategy = 'eager'

        # try:
        self.driver = webdriver.Chrome(service=service, options=options)

    def make_mozilla(self, driver_path):
        download_directory = os.path.abspath('licitacoes/src/bot/editais')

        firefox_path = r"D:\Programas\firefox\firefox.exe"
        # firefox_options =
        # firefox_options.binary_location = firefox_path
        service = GeckoService(executable_path=driver_path)
        options = webdriver.FirefoxOptions()
        options.binary_location = firefox_path
        options.add_argument('--log-level=4')

        # 0: Desktop, 1: Downloads, 2: Diretório personalizado
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_directory)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/pdf, application/octet-stream")  # Adicione os tipos MIME desejados

        # Essa linha pode ser útil para alguns casos
        options.set_preference("webdriver.load.strategy", "unstable")
        # Tempo em segundos (aumente conforme necessário)
        options.set_preference("webdriver.page.load.timeout", 60)

        # options.add_argument('--headless')
        # Desativa notificações
        # options.set_preference("dom.webnotifications.enabled", False)
        # # Desativa o carregamento de imagens
        # options.set_preference("permissions.default.image", 2)
        # options.set_preference("plugin.state.flash", 0)
        # # Desativa notificações
        # options.add_argument('--disable-notifications')
        # # Desativa o carregamento de imagens
        # options.add_argument('--blink-settings=imagesEnabled=false')
        # # Desativa a execução de extensões do Chrome
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-plugins')
        # options.add_argument('--disable-gpu')
        # options.set_preference("layers.acceleration.disabled", True)
        # options.set_preference("gfx.webrender.all", False)
        # options.set_preference("webgl.disabled", True)
        # options.set_preference("app.update.auto", False)
        # options.set_preference("app.update.enabled", False)
        # options.set_preference("security.enterprise_roots.enabled", False)
        # options.add_argument('--width=1920')
        # options.add_argument('--height=1080')
        # options.set_preference("toolkit.cosmeticAnimations.enabled", False)
        # options.set_preference("webdriver.log.driver", "OFF")

        options.page_load_strategy = 'normal'

        # options.page_load_strategy = 'eager'

        self.driver = webdriver.Firefox(service=service, options=options)


if __name__ == '__main__':
    pass
    d = Driver()
    time.sleep(5)
