import logging


class Loggers:

    def __init__(self, syslog_name, urllog_name, sys_level=logging.INFO, url_level=logging.INFO):
        self.formatter = logging.Formatter('%(asctime)s\t|\t%(levelname)s\t|%(message)s')
        self.syslog_name = syslog_name
        self.sys_level = sys_level
        self.urllog_name = urllog_name
        self.url_level = url_level

    def get_syslogger(self):
        # System logger config
        sys_logger = logging.getLogger('sysLogger')
        sys_logger.setLevel(self.sys_level)
        sys_fh = logging.FileHandler(self.syslog_name)
        sys_fh.setFormatter(self.formatter)
        # sys_fh.setLevel(sys_level)
        sys_logger.addHandler(sys_fh)
        return sys_logger

    def get_urllogger(self):
        # URL logger config
        url_logger = logging.getLogger('urlLogger')
        url_logger.setLevel(self.url_level)
        url_fh = logging.FileHandler(self.urllog_name)
        # url_fh.setFormatter('%(message)s')
        # url_fh.setLevel(url_level)
        url_logger.addHandler(url_fh)
        return url_logger
