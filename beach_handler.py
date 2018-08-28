import tornado.web
import tornado.template
import pymongo
import datetime
import time
import os

class BeachTime:
    @staticmethod
    def secondsSince2000():
        return 978285600

class BeachHandler(tornado.web.RequestHandler):
    def get(self):
        username = os.environ.get("MONGO_USER")
        password = os.environ.get("MONGO_PASS")
        server = os.environ.get("MONGO_HOST")
        mongo_url = "mongodb+srv://%s:%s@%s/test?retryWrites=true" % (username, password, server)
        myclient = pymongo.MongoClient(mongo_url)
        beach_db = myclient["beach"]
        house_collection = beach_db["house"]

        rental_agencies = house_collection.distinct("rentalAgency")

        house_query_options = {}

        oceanfront = self.get_argument('oceanfront', None)
        if oceanfront and oceanfront.lower() == "true":
            house_query_options["oceanfront"] = True

        four_by_four = self.get_argument('4x4', None)
        if four_by_four and four_by_four.lower() == "false":
            house_query_options["regionName"] = { "$not": { "$eq": "4x4" }  }
        elif four_by_four and four_by_four.lower() == "true":
            house_query_options["regionName"] = "4x4"

        nearby_lat = self.get_argument('nearby_lat', None)
        nearby_long = self.get_argument('nearby_long', None)
        if nearby_lat and nearby_long:
            nearby_lat = float(nearby_lat)
            nearby_long = float(nearby_long)
            gps_threshold = 0.003
            house_query_options["latitude"] = { "$gte": nearby_lat - gps_threshold, "$lte": nearby_lat + gps_threshold }
            house_query_options["longitude"] = { "$gte": nearby_long - gps_threshold, "$lte": nearby_long + gps_threshold }


        start_date = self.get_argument('start_date', None)
        start_time = None
        if start_date:
            start_datetime_object = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_time = time.mktime(start_datetime_object.timetuple()) - BeachTime.secondsSince2000()
            house_query_options["availability.arrivalDate"] = { "$gte": start_time }
            house_query_options["availability.isAvailable"] = True

        end_date = self.get_argument('end_date', None)
        end_time = None
        if end_date:
            end_datetime_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_time = time.mktime(end_datetime_object.timetuple()) - BeachTime.secondsSince2000()
            house_query_options["availability.arrivalDate"] = { "$lte": end_time }
            house_query_options["availability.isAvailable"] = True

        house_query = house_collection.find(house_query_options)

        sort_query = self.get_argument('sort', None)
        sorted_by = None
        if sort_query:
            sort_query_list = sort_query.split(",")
            for option in sort_query_list:
                if option == "cost":
                    house_query.sort("maxRate", -1)
                    sorted_by = "cost"
                elif option == "beds":
                    house_query.sort("bedrooms", -1)
                    sorted_by = "beds"

        houses = []
        arrival_dates = []
        today = int(time.time()) - BeachTime.secondsSince2000()
        for house in house_query:
            if house.get("maxRate") is None and house.get("availability") is not None:
                total_costs = [a.get("totalCost", -1) for a in house.get("availability")]
                if total_costs:
                    max_cost = max(total_costs)
                    if max_cost > 0:
                        house["maxRate"] = max_cost

            houses.append(house)

            if house.get("availability"):
                for availability in house.get("availability"):
                    arrivalDate = availability.get("arrivalDate")
                    if start_time and end_time:
                        if arrivalDate < start_time or arrivalDate > end_time:
                            continue

                    nextDay = arrivalDate + 86400
                    previousDay = arrivalDate - 86400
                    if arrivalDate > today and arrivalDate not in arrival_dates and nextDay not in arrival_dates and previousDay not in arrival_dates:
                        arrival_dates.append(arrivalDate)

        arrival_dates.sort()

        templates_dir = os.environ.get("TEMPLATES_DIR")
        loader = tornado.template.Loader(templates_dir)
        html_output = loader.load("houses.html").generate(house_count=len(houses), houses=houses, arrival_dates=arrival_dates, oceanfront=oceanfront, sorted_by=sorted_by, four_by_four=four_by_four, start_date=start_date, end_date=end_date, nearby_lat=nearby_lat, nearby_long=nearby_long, rental_agencies=rental_agencies)
        self.write(html_output)
