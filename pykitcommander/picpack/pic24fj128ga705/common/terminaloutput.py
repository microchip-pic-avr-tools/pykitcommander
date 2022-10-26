"""
This file contains a class that wraps the msg object injected by MPLAB
The purpose is to get a proper python object that can be mocked during testing
"""

class TerminalOutput(object):
    """
    Wraps the msg object injected by MPLAB
    """
    def __init__(self, msg_obj):
        """
        The msg_obj is the msg object injected into the tool device file by MPLAB
        """
        self.msg = msg_obj

    def display(self, message):
        """
        Output message in MPLAB
        """
        self.msg.print(message)

    def show_info_dialog_non_blocking(self, message):
        """
        Created a pop-up warning box in MPLAB X
        """
        self.msg.msg(message, "Script Warning:")
