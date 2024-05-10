# p2app/engine/event_classes.py
#
# module for event functionality split into a separate module for readability and functionality

import sqlite3
import p2app.events

error_message = 'Sorry! Unfortunately, you have entered a invalid or pre-existing value in the database. Or something unexpected has occurred. Please try again :)'


class ContinentEvents:
    """
    Class for Continent-Related Events for searching, loading, adding, and editing Continents.
    Is referenced to in the engine/main module and returns values back.
    """
    def __init__(self, event, connection):
        """Initializer sets up the event separately from the database connection"""
        self.event = event
        self.connection = connection

    def search_for_continents(self):
        """function finds continents that match the parameters given"""
        search = self.connection.cursor()
        search.execute("SELECT * FROM continent WHERE name = ? OR continent_code = ?;", [self.event.name(), self.event.continent_code()])
        search_list = search.fetchall()
        return [p2app.events.Continent(items[0], items[1], items[2]) for items in search_list]

    def load_continent(self):
        """loads in the contents of the selected continent with a Continent tuple"""
        load = self.connection.cursor()
        try:
            load.execute("SELECT * FROM continent WHERE continent_id = ?;", [self.event.continent_id()])
            load_item = load.fetchone()
            return True, p2app.events.Continent(load_item[0], load_item[1], load_item[2])
        except:
            return False, error_message

    def save_new_continent(self):
        """saves new continent into the continent table for the selected database"""
        continent = self.event.continent()
        save = self.connection
        access = self.connection.cursor()
        access.execute("SELECT continent_id FROM continent;")
        ids = access.fetchall()
        max_id = max(ids)
        try:
            access.execute("INSERT INTO continent (continent_id, continent_code, name) VALUES (?, ?, ?);", [max_id[0] + 1, continent[1], continent[2]])
            save.commit()
            return True, p2app.events.Continent(max_id[0] + 1, continent[1], continent[2])
        except:
            return False, error_message

    def save_edited_continent(self):
        """saves changes to continent contents and returns the contents to process function"""
        continent = self.event.continent()
        save = self.connection
        try:
            save.execute("UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?;", [continent[1], continent[2], continent[0]])
            save.commit()
            return True, continent
        except:
            return False, error_message


class CountryEvents:
    """
    Class for Country-Related Events for searching, loading, adding, and editing Countries.
    Is referenced to in the engine/main module and returns values back.
    """
    def __init__(self,event, connection):
        """Initializer sets up the event separately from the database connection"""
        self.event = event
        self.connection = connection

    def search_for_countries(self):
        """function finds countries that match the parameters given"""
        search = self.connection.cursor()
        search.execute("SELECT * FROM country WHERE name = ? OR country_code = ?;", [self.event.name(), self.event.country_code()])
        search_list = search.fetchall()
        return [p2app.events.Country(items[0], items[1], items[2], items[3], items[4], items[5]) for items in search_list]

    def load_country(self):
        """loads in the contents of the selected country with a Country tuple"""
        load = self.connection.cursor()
        try:
            load.execute("SELECT * FROM country WHERE country_id = ?;", [self.event.country_id()])
            load_item = load.fetchone()
            return True, p2app.events.Country(load_item[0], load_item[1], load_item[2], load_item[3], load_item[4], load_item[5])
        except:
            return False, error_message

    def save_new_country(self):
        """saves new country into the country table for the selected database"""
        country = self.event.country()
        save = self.connection
        access = self.connection.cursor()
        access.execute("SELECT country_id FROM country;")
        ids = access.fetchall()
        max_id = max(ids)
        try:
            access.execute("INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?);", [max_id[0] + 1, country[1], country[2], country[3], country[4], country[5]])
            save.commit()
            return True, p2app.events.Country(max_id[0] + 1, country[1], country[2], country[3], country[4], country[5])
        except:
            return False, error_message

    def save_edited_country(self):
        """saves changes to country contents and returns the contents to process function"""
        country = self.event.country()
        save = self.connection
        try:
            save.execute("UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?;", [country[1], country[2], country[3], country[4], country[5], country[0]])
            save.commit()
            return True, country
        except:
            return False, error_message


class RegionEvents:
    """
    Class for Region-Related Events for searching, loading, adding, and editing Regions.
    Is referenced to in the engine/main module and returns values back.
    """
    def __init__(self, event, connection):
        """Initializer sets up the event separately from the database connection"""
        self.event = event
        self.connection = connection

    def search_for_regions(self):
        """function finds regions that match the parameters given"""
        search = self.connection.cursor()
        search.execute("SELECT * FROM region WHERE name = ? OR region_code = ? OR local_code = ?;", [self.event.name(), self.event.region_code(), self.event.local_code()])
        search_list = search.fetchall()
        return [p2app.events.Region(items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7]) for items in search_list]

    def load_region(self):
        """loads in the contents of the selected region with a Region tuple"""
        load = self.connection.cursor()
        try:
            load.execute("SELECT * FROM region WHERE region_id = ?;", [self.event.region_id()])
            load_item = load.fetchone()
            return True, p2app.events.Region(load_item[0], load_item[1], load_item[2], load_item[3], load_item[4], load_item[5], load_item[6], load_item[7])
        except:
            return False, error_message

    def save_new_region(self):
        """saves new region into the region table for the selected database"""
        region = self.event.region()
        save = self.connection
        access = self.connection.cursor()
        access.execute("SELECT region_id FROM region;")
        ids = access.fetchall()
        max_id = max(ids)
        try:
            access.execute("INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", [max_id[0] + 1, region[1], region[2], region[3], region[4], region[5], region[6], region[7]])
            save.commit()
            return True, p2app.events.Region(max_id[0] + 1, region[1], region[2], region[3], region[4], region[5], region[6], region[7])
        except:
            return False, error_message

    def save_edited_region(self):
        """saves changes to region contents and returns the contents to process function"""
        region = self.event.region()
        save = self.connection
        try:
            save.execute("UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?;", [region[1], region[2], region[3], region[4], region[5], region[6], region[7], region[0]])
            save.commit()
            return True, region
        except:
            return False, error_message
