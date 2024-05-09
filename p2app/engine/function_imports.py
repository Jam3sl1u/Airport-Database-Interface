# p2app/engine/event_functions.py
#
# module for event functionality split into a separate module for readability and functionality

import sqlite3
import p2app.events
class ContinentEvents:
    """Initializer sets up the event separately from the database connection"""
    def __init__(self, event, connection):
        self.event = event
        self.connection = connection

    def search_for_continents(self):
        """function finds continents that match the parameters given"""
        search = self.connection.cursor()
        search.execute("SELECT * FROM continent WHERE name = ? OR continent_code = ?", (self.event.name(), self.event.continent_code(),))
        search_list = search.fetchall()
        return [p2app.events.Continent(items[0], items[1], items[2]) for items in search_list]

    def load_continent(self):
        """loads in the contents of the selected continent with a Continent tuple"""
        load = self.connection.cursor()
        load.execute("SELECT * FROM continent WHERE continent_id = ?", (self.event.continent_id(),))
        load_item = load.fetchone()
        return p2app.events.Continent(load_item[0], load_item[1], load_item[2])