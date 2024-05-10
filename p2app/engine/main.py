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
from p2app.engine.function_imports import *

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
        elif type_event is p2app.events.OpenDatabaseEvent:
            if event.path().suffix == '.db' and event.path().exists():
                self.establish_connection = sqlite3.connect(event.path())
                self.establish_connection.execute('PRAGMA foreign_keys = ON;')
                self.establish_connection.commit()
                yield p2app.events.DatabaseOpenedEvent(event.path())
            else:
                yield p2app.events.DatabaseOpenFailedEvent()
        elif type_event is p2app.events.CloseDatabaseEvent:
            yield p2app.events.DatabaseClosedEvent()
        # Continent-Related Events
        elif type_event is p2app.events.StartContinentSearchEvent:
            search = ContinentEvents(event, self.establish_connection)
            for continent in search.search_for_continents():
                yield p2app.events.ContinentSearchResultEvent(continent)
        elif type_event is p2app.events.LoadContinentEvent:
            load = ContinentEvents(event, self.establish_connection)
            yield p2app.events.ContinentLoadedEvent(load.load_continent())
        elif type_event is p2app.events.SaveNewContinentEvent:
            save = ContinentEvents(event, self.establish_connection)
            result, contents = save.save_new_continent()
            if result is True:
                yield p2app.events.ContinentSavedEvent(contents)
            else:
                yield p2app.events.SaveContinentFailedEvent(contents)
        elif type_event is p2app.events.SaveContinentEvent:
            save = ContinentEvents(event, self.establish_connection)
            result, contents = save.save_edited_continent()
            if result is True:
                yield p2app.events.ContinentSavedEvent(contents)
            else:
                yield p2app.events.SaveContinentFailedEvent(contents)
        # Country-Related Events
        elif type_event is p2app.events.StartCountrySearchEvent:
            search = CountryEvents(event, self.establish_connection)
            for country in search.search_for_countries():
                yield p2app.events.CountrySearchResultEvent(country)
        elif type_event is p2app.events.LoadCountryEvent:
            load = CountryEvents(event, self.establish_connection)
            yield p2app.events.CountryLoadedEvent(load.load_country())
        elif type_event is p2app.events.SaveNewCountryEvent:
            save = CountryEvents(event, self.establish_connection)
            result, contents = save.save_new_country()
            if result is True:
                yield p2app.events.CountrySavedEvent(contents)
            else:
                yield p2app.events.SaveCountryFailedEvent(contents)
        elif type_event is p2app.events.SaveCountryEvent:
            save = CountryEvents(event, self.establish_connection)
            result, contents = save.save_edited_country()
            if result is True:
                yield p2app.events.CountrySavedEvent(contents)
            else:
                yield p2app.events.SaveCountryFailedEvent(contents)
        # Region-Related Events
        elif type_event is p2app.events.StartRegionSearchEvent:
            search = RegionEvents(event, self.establish_connection)
            for region in search.search_for_regions():
                yield p2app.events.RegionSearchResultEvent(region)
        elif type_event is p2app.events.LoadRegionEvent:
            load = RegionEvents(event, self.establish_connection)
            yield p2app.events.RegionLoadedEvent(load.load_region())
        yield from ()
