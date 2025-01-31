import os
import argparse
import logging
import psutil
import socket
from datetime import datetime


class LogHandler:
    """Handles the configuration of application logging."""

    @staticmethod
    def configure_logging():
        """Sets up logging by creating a directory for logs and defining the log file format."""
        log_dir = os.path.join(os.getcwd(), "Application_Logs")
        log_filename = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        os.makedirs(log_dir, exist_ok=True)
        log_filepath = os.path.join(log_dir, log_filename)

        logging.basicConfig(
            filename=log_filepath,
            format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        logging.info("Log recording started successfully")


class SystemInspector:
    """
    Retrieves and processes system-related data.
    """

    @staticmethod
    def fetch_top_cpu_usage(limit=5):
        """
        Identifies the top N processes consuming CPU.
        :param limit: Number of high CPU usage processes to retrieve
        :return: Dictionary containing process names and their CPU utilization percentage
        """
        process_records = [proc.info for proc in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
        sorted_records = sorted(process_records, key=lambda proc: proc['cpu_percent'], reverse=True)

        return {f"Process_{idx + 1}": f"{proc['name']}: {proc['cpu_percent']}%"
                for idx, proc in enumerate(sorted_records[:limit])}

    @staticmethod
    def collect_system_metrics():
        """
        Aggregates various system-related statistics.
        :return: Dictionary with system details
        """
        return {
            "System Hostname": socket.getfqdn(),
            "Total Memory (GB)": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Physical CPU Units": psutil.cpu_count(logical=False),
            "Overall CPU Cores": psutil.cpu_count(logical=True),
            "Available Disk Drives": sum(1 for disk in psutil.disk_partitions() if 'removable' not in disk.opts),
            "High CPU Usage Processes": SystemInspector.fetch_top_cpu_usage()
        }


class SystemMonitorApp:
    """
    Core application class that interprets command-line arguments and executes tasks.
    """

    def __init__(self):
        self.argument_parser = argparse.ArgumentParser(description="System Performance Monitoring Tool")
        self.argument_parser.add_argument("-help", action="store_true", help="Display usage guide and exit")
        self.argument_parser.add_argument("-logInfo", action="store_true", help="Enable logging for system statistics")
        self.cmd_arguments = self.argument_parser.parse_args()

    def execute(self):
        """Executes the relevant functions based on user-specified arguments."""
        if self.cmd_arguments.help:
            self.argument_parser.print_help()
            return

        if self.cmd_arguments.logInfo:
            LogHandler.configure_logging()

        system_info = SystemInspector.collect_system_metrics()

        for key, value in system_info.items():
            print(f"{key}: {value}")
            logging.info(f"{key}: {value}")


if __name__ == "__main__":
    app_instance = SystemMonitorApp()
    app_instance.execute()