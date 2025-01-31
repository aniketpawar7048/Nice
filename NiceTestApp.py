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

        # Creating log directory if necessary
        os.makedirs(log_dir, exist_ok=True)
        log_filepath = os.path.join(log_dir, log_filename)

        # Logger configuration
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
    def fetch_cpu_usage(limit=5):
        """
        Identifies the top N processes consuming CPU.
        :param limit: Number of high CPU usage processes to retrieve
        :return: Dictionary containing process names and their CPU utilization percentage
        """

        # Collect PID, Process name and CPU usage.
        process_records = [proc.info for proc in psutil.process_iter(['pid', 'name', 'cpu_percent'])]

        # Sort processes based on CPU usage
        sorted_records = sorted(process_records, key=lambda proc: proc['cpu_percent'], reverse=True)

        # Return output in a directory format
        return {f"Process_{idx + 1}": f"{proc['name']}: {proc['cpu_percent']}%"
                for idx, proc in enumerate(sorted_records[:limit])}

    @staticmethod
    def collect_system_metrics():
        """
        Aggregates various system-related statistics.
        :return: Dictionary with system details
        """
        # Return consolidated output in a directory format
        return {
            "Computer Name": socket.getfqdn(),
            "Total Physical Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Total Number of Physical Processors": psutil.cpu_count(logical=False),
            "Total Number of Cores": psutil.cpu_count(logical=True),
            "Total Number of Hard Disks": sum(1 for disk in psutil.disk_partitions() if 'removable' not in disk.opts),
            "Top 5 processes in terms of CPU": SystemInspector.fetch_cpu_usage()
        }


class SystemMonitorApp:
    """
    Core application class that interprets command-line arguments and executes tasks.
    """

    def __init__(self):
        # Initialize argument parser
        self.argument_parser = argparse.ArgumentParser(description="Computer Information Application")

        # Define the -help argument
        self.argument_parser.add_argument("-help", action="store_true", help="Display usage guide and exit")

        # Define the -logInfo argument
        self.argument_parser.add_argument("-logInfo", action="store_true", help="Log the computer information to the log file")

        # Parsing the command-line arguments
        self.cmd_arguments = self.argument_parser.parse_args()

    def execute(self):
        """Executes the relevant functions based on user-specified arguments."""

        # For -help argument, print the help message and exit
        if self.cmd_arguments.help:
            self.argument_parser.print_help()
            return

        # For -logInfo argument, set up the logging
        if self.cmd_arguments.logInfo:
            LogHandler.configure_logging()

        # Get system information
        system_info = SystemInspector.collect_system_metrics()

        # Iterate through the directory of system_info
        for key, value in system_info.items():
            # Display system information on console
            print(f"{key}: {value}")
            # Append system information into log file
            logging.info(f"{key}: {value}")


if __name__ == "__main__":
    app_instance = SystemMonitorApp()
    app_instance.execute()