
BOT_NAME = 'leruaparser'

SPIDER_MODULES = ['homework_7_lerua.leruaparser.spiders']
NEWSPIDER_MODULE = 'homework_7_lerua.leruaparser.spiders'

COOKIES_ENABLED = True

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.163 Chrome/80.0.3987.163 Safari/537.36'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'homework_7_lerua.leruaparser.pipelines.LeruaparserPipeline': 300,
    'homework_7_lerua.leruaparser.pipelines.LeruaparserPhoptosPipeline': 200,
}

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'lerua_log.txt'

IMAGES_STORE = 'images'
IMAGES_EXPIRES = 30
#изменение размера картинок – будет сохраняться в  	<IMAGES_STORE>/thumbs/<size_name>/<image_id>.jpg
IMAGES_THUMBS = {
    'small': (50, 50)
}
#фильтрация картинок по размеру(длины и ширины)
IMAGES_MIN_HEIGHT = 80
IMAGES_MIN_WIDTH = 80
