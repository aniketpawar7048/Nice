import os
import argparse
import logging
import psutil
import socket
from datetime import datetime


class Logger:
    """Handles application logging."""

    @staticmethod
    def setup_logger():
        """Sets up logging by creating a log directory and initializing logging."""
        logs_path = os.path.join(os.getcwd(), "App_Logs")
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

        os.makedirs(logs_path, exist_ok=True)
        log_file_path = os.path.join(logs_path, log_file)

        logging.basicConfig(
            filename=log_file_path,
            format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        logging.info("Execution logs have started")

class SystemInfo:
    """
    SystemInfo class to fetch system-related information.
    """

    @staticmethod
    def get_top_cpu_processes(limit=5):
        """
        Retrieves the top N CPU-consuming processes.
        :param limit: Number of top processes to retrieve
        :return: Dictionary of process names with their CPU usage percentage
        """
        cpu_processes = [proc.info for proc in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
        cpu_processes.sort(key=lambda proc: proc['cpu_percent'], reverse=True)

        return {f"Process{idx + 1}": f"{proc['name']}: {proc['cpu_percent']}%"
                for idx, proc in enumerate(cpu_processes[:limit])}

    @staticmethod
    def get_computer_info():
        """
        Retrieves computer system information.
        :return: Dictionary containing system information
        """
        return {
            "Computer Name": socket.getfqdn(),
            "Total Physical Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Total Number of Physical Processors": psutil.cpu_count(logical=False),
            "Total Number of Cores": psutil.cpu_count(logical=True),
            "Total Number of Hard Disks": sum(1 for disk in psutil.disk_partitions() if 'removable' not in disk.opts),
            "Top 5 processes in terms of CPU": SystemInfo.get_top_cpu_processes()
        }


class ComputerInfoApp:
    """
    Main application class to handle argument parsing and execution.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Computer information application")
        self.parser.add_argument("-help", action="store_true", help="Display help message and exit")
        self.parser.add_argument("-loginfo", action="store_true", help="Log the computer information to a file")
        self.args = self.parser.parse_args()

    def run(self):
        """
        Executes the application based on command-line arguments.
        """
        if self.args.help:
            self.parser.print_help()
            return

        if self.args.loginfo:
            Logger.setup_logger()

        info = SystemInfo.get_computer_info()

        for key, value in info.items():
            print(f"{key}: {value}")
            logging.info(f"{key}: {value}")


if __name__ == "__main__":
    app = ComputerInfoApp()
    app.run()
