# p2app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import sqlite3

import p2app.events


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.establish_connection = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        type_event = type(event)
        # Application-Level Events
        if type_event is p2app.events.QuitInitiatedEvent:
            yield p2app.events.EndApplicationEvent()






        yield from ()
