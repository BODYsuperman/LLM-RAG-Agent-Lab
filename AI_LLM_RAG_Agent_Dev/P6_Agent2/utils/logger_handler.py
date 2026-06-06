import logging
import os
import sys

# 支持直接运行：将上级目录加入路径
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.path_tool import get_abs_path

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


# 日志根目录：项目根目录下的 logs 目录
LOG_ROOT = get_abs_path("logs")

os.makedirs(LOG_ROOT, exist_ok= True)

DEFAULT_LOG_FORMATTER = logging.Formatter(
   # 时间 - logger 名称 - 级别 - 文件名:行号 - 消息
    # 2026-03-04 13:31:41,240 - P6_Agent2.utils.logger_handler - DEBUG - test.py:3 - 这是一条 DEBUG 日志（默认只写入文件）。
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s" 
)

def get_logger(
        name: str = "agent",
        console_level :int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file = None,
        when: str = "D",
        interval: int = 1,       # 多久轮转一次日志文件（配合 when 使用），默认 1 天
        backup_count: int = 7,   # 最多保留多少个历史日志文件，超过会自动删除旧文件
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
 
    #如果已经配置过 handler，直接返回，避免重复添加
    if logger.handlers:
        return logger
    

    # 1. 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMATTER)
    logger.addHandler(console_handler)

       # 2. 文件 Handler（按时间轮转）
    if log_file is None:
        log_file = _build_log_file_path(name)

    # 如果传入了相对路径，自动转为基于项目根目录的绝对路径
    if not os.path.isabs(log_file):
        log_file = get_abs_path(log_file)

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMATTER)
    logger.addHandler(file_handler)

    return logger

def _build_log_file_path(name: str) -> str:
    """
    根据 logger 名称和当前日期生成日志文件路径。

    例如：logs/agent_20260304.log
    """
    safe_name = name.replace(":", "_").replace("/", "_")
    filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d')}.log"
    return os.path.join(LOG_ROOT, filename)

if __name__ == "__main__":
    """
    简单自测代码：
    - 在控制台打印不同级别日志；
    - 在 `logs/` 目录下生成对应的日志文件。
    运行方式（二选一）：
        # 在项目根目录下
        python -m zhisaotong_agent.utils.logger_handler

        # 或在包根目录 zhisaotong_agent/ 下
        python -m utils.logger_handler
    """
    # test_logger = get_logger("logger_handler_demo")
    test_logger = get_logger()
    test_logger.debug("这是一条 DEBUG 日志（默认只写入文件）。")
    test_logger.info("这是一条 INFO 日志。")
    test_logger.warning("这是一条 WARNING 日志。")
    test_logger.error("这是一条 ERROR 日志。")
    test_logger.critical("这是一条 CRITICAL 日志。")

