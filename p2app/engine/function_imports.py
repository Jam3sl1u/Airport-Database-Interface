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
        search.execute("SELECT * FROM continent WHERE name = ? OR continent_code = ?", [self.event.name(), self.event.continent_code()])
        search_list = search.fetchall()
        return [p2app.events.Continent(items[0], items[1], items[2]) for items in search_list]

    def load_continent(self):
        """loads in the contents of the selected continent with a Continent tuple"""
        load = self.connection.cursor()
        load.execute("SELECT * FROM continent WHERE continent_id = ?", [self.event.continent_id()])
        load_item = load.fetchone()
        return p2app.events.Continent(load_item[0], load_item[1], load_item[2])

    def save_new_continent(self):
        """saves new continent into the continent table for the selected database"""
        continent = self.event.continent()
        save = self.connection
        access = self.connection.cursor()
        access.execute("SELECT continent_id FROM continent")
        ids = access.fetchall()
        max_id = max(ids)
        try:
            access.execute("INSERT INTO continent VALUES(?, ?, ?)", [max_id[0] + 1, continent[1], continent[2]])
            save.commit()
            return True, p2app.events.Continent(max_id[0] + 1, continent[1], continent[2])
        except Exception as reason:
            return False, reason

    def save_edited_continent(self):
        """saves changes to continent contents and returns the contents to process function"""
        continent = self.event.continent()
        save = self.connection
        try:
            save.execute("UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?", [continent[1], continent[2], continent[0]])
            save.commit()
            return True, continent
        except Exception as reason:
            return False, reason

class CountryEvents:
    def __init__(self,event, connection):
        self.event = event
        self.connection = connection

    def search_for_countries(self):
        """function finds countries that match the parameters given"""
        search = self.connection.cursor()
        search.execute("SELECT * FROM country WHERE name = ? OR country_code = ?", [self.event.name(), self.event.country_code()])
        search_list = search.fetchall()
        return [p2app.events.Country(items[0], items[1], items[2], items[3], items[4], items[5]) for items in search_list]

    def load_country(self):
        """loads in the contents of the selected country with a Country tuple"""
        load = self.connection.cursor()
        load.execute("SELECT * FROM country WHERE country_id = ?", [self.event.country_id()])
        load_item = load.fetchone()
        return p2app.events.Country(load_item[0], load_item[1], load_item[2], load_item[3], load_item[4], load_item[5])

    def save_new_country(self):
        """saves new country into the country table for the selected database"""
        country = self.event.country()
        save = self.connection
        access = self.connection.cursor()
        access.execute("SELECT country_id FROM country")
        ids = access.fetchall()
        max_id = max(ids)
        try:
            access.execute("INSERT INTO country VALUES(?, ?, ?, ?, ?, ?)", [max_id[0] + 1, country[1], country[2], country[3], country[4], country[5]])
            save.commit()
            return True, p2app.events.Country(max_id[0] + 1, country[1], country[2], country[3], country[4], country[5])
        except Exception as reason:
            return False, reason