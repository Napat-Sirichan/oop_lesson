import csv, os

class Table:
    def __init__(self, table_name, file_path):
        self.table_name = table_name
        self.data = self._load_data(file_path)

    def _load_data(self, file_path):
        """Load data from the CSV file into a list of dictionaries."""
        data = []
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, file_path)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                data.append(dict(r))
        return data

    def filter(self, condition):
        """Filter items based on the given condition."""
        return [item for item in self.data if condition(item)]

    def aggregate(self, aggregation_function, aggregation_key):
        """Aggregate data based on the key and the provided function."""
        values = [float(item[aggregation_key]) for item in self.data]
        return aggregation_function(values)

    def __str__(self):
        return f"Table: {self.table_name}, Rows: {len(self.data)}"


class TableDB:
    def __init__(self):
        self.table_database = []

    def insert(self, table):
        if not self.search(table.table_name):
            self.table_database.append(table)
        else:
            print(f"Table {table.table_name} already exists in the database.")

    def search(self, table_name):
        for table in self.table_database:
            if table.table_name == table_name:
                return table
        return None

    def __str__(self):
        return f"TableDB: {len(self.table_database)} tables"


if __name__ == "__main__":
    db = TableDB()

    cities_table = Table("Cities", "Cities.csv")
    countries_table = Table("Countries", "Countries.csv")

    db.insert(cities_table)
    db.insert(countries_table)

    print(db)

    print("The average temperature of all the cities:")
    avg_temp = cities_table.aggregate(lambda temps: sum(temps) / len(temps), "temperature")
    print(avg_temp)

    cities_in_italy = cities_table.filter(lambda city: city['country'] == 'Italy')
    print("All cities in Italy:", [city['city'] for city in cities_in_italy])

    max_temp_italy = max(float(city['temperature']) for city in cities_in_italy)
    print("The max temperature of all the cities in Italy:", max_temp_italy)

    min_temp_italy = min(float(city['temperature']) for city in cities_in_italy)
    print("The min temperature of all the cities in Italy:", min_temp_italy)