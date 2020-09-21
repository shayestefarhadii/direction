from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
import math
import overpy





def home(request):
    return render_to_response('index.html')



def app_dir(request):
    return render_to_response('dir.html')

def app_add(request):
    return render_to_response('address.html')

def app_amenity(request):
    return render_to_response('amenity.html')




from django.http import JsonResponse
import json

#def map_add(request):
    #if 'q1' in request.GET and 'q2'in request.GET:
       # a = [request.GET['q1']]
       # a.append(request.GET['q2'])
      #  message = 'You searched for: %r' %  a

    #else:
       # message = 'You submitted an empty form.'
    #print(message)
    #return JsonResponse({'data': message})

from functools import partial
from geopy.geocoders import Nominatim
def answer_me(request):
    input_long = request.GET.get('inputValue_long')
    input_lat = request.GET.get('inputValue_lat')
    geolocator = Nominatim(user_agent="map")
    reverse = partial(geolocator.reverse, language="es")
    x = reverse(str(input_lat) + ', ' + str(input_long))

    b = []
    string = ""
    b.append((input_lat, input_long))
    location = geolocator.reverse((b))
    x = location.raw["address"]
    if "amenity" in x:
        string = string + '{}'.format(x["amenity"]) + '\n '
    if "road" in x:
        string = string + ' نام جاده: {}'.format(x["road"]) + '\n  '
    if "suburb" in x:
        string = string + ' نام منطقه: {}'.format(x["suburb"]) + '\n '
    if "street" in x:
        string = string + ' نام خیابان: {}'.format(x["street"]) + '\n '
    if "village" in x:
        string = string + ' نام روستا: {}'.format(x["village"]) + '\n '
    if "city" in x:
        string = string + ' نام شهر: {}'.format(x["city"]) + '\n '
    if "state" in x:
        string = string + ' نام استان: {}'.format(x["state"]) + '\n '
    if "county" in x:
        string = string + ' نام شهرستان: {}'.format(x["county"]) + '\n '
    if "district" in x:
        string = string + ' نام ناحیه: {}'.format(x["district"]) + '\n '
    if "postcode" in x:
        string = string + ' کد پستی: {}'.format(x["postcode"]) + '\n'
    if "country" in x:
        string = string +  ' نام کشور: {}'.format(x["country"])

    data = {'response_long': string, 'response_lat': f'You typed: {location.raw["address"]}'}
    return JsonResponse(data)



def dir_map(request):
    all_routes = []
    nei = []
    count = 0
    neighbors = []
    cal = []
    dis = []
    closed = []
    sum = 0
    inputValue_or_long = request.GET.get('inputValue_or_long')
    inputValue_or_lat = request.GET.get('inputValue_or_lat')
    inputValue_des_long = request.GET.get('inputValue_des_long')
    inputValue_des_lat = request.GET.get('inputValue_des_lat')

    geolocator = Nominatim(user_agent="map")
    reverse = partial(geolocator.reverse, language="es")



    def nearest(long, lat):
        url2 = 'http://router.project-osrm.org/nearest/v1/car/{},{}?number=1&bearings=90,100'.format(long, lat)
        res = requests.post(url2)
        c = res.json()['waypoints']
        return c[0]['location']

    def check_route(orig_lat, orig_long, des_lat, des_long):

        url2 = 'http://router.project-osrm.org/route/v1/driving/{},{};{},{}?steps=true'.format(orig_long, orig_lat, des_long,
                                                                                      des_lat)
        res = requests.post(url2)
        c = res.json()
        intersection = []
        for i in c['routes'][0]['legs'][0]['steps']:
            intersection.append(i['intersections'][0]['location'])
        return intersection


    def distance(lat1, lat2, lon1, lon2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return (c * r)

    def findpoints(lon, lat):
        radius = 0.001
        N = 360

        # generate points
        circlePoints2 = []

        for k in range(N):
            angle = math.pi * 2 * k / N
            dx = radius * math.cos(angle)
            dy = radius * math.sin(angle)
            # add to list
            point2 = []
            point2.append((lat + (180 / math.pi) * (dy / 6371)))  # Earth Radius
            point2.append(lon + (180 / math.pi) * (dx / 6371) / math.cos(lon * math.pi / 180))

            circlePoints2.append(point2)

        return circlePoints2

    def call(lat1, lat2, lon1, lon2):
        nei = []
        neighbors = []
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="map")
        b = []
        b.append((lat1, lon1))
        location_or = geolocator.reverse((b))
        location_des = geolocator.reverse(b)
        closed = []
        dis = []
        sum = distance(location_or.latitude, lat2, location_or.longitude, lon2)
        neighbors.append([location_or.latitude, location_or.longitude])
        dis.append(((location_or.latitude, location_or.longitude), sum))
        closed.append(([location_or.latitude, location_or.longitude], 0, sum))
        while (distance(closed[-1][0][0], lat2, closed[-1][0][1], lon2) >= 0.001):
            c = findpoints(closed[-1][0][1], closed[-1][0][0])

            for i in c:
                dis.append((i, distance(i[0], lat2, i[1], lon2),
                            distance(location_or.latitude, i[0], location_or.longitude, i[1])))

            dis.sort(key=lambda x: x[1])
            closed.append(dis[0])
            dis = []
        a = []
        for i in closed:
            i[0].reverse()
        return closed


    def dist(sum):
        sum = sum + (sum * 0.3)
        t = 0
        v = 60
        t = sum/v
        return t*60





    intersections= check_route(inputValue_or_lat, inputValue_or_long, inputValue_des_lat, inputValue_des_long)
    for i in intersections:
        i.reverse()
    list_of_des = []
    for i in range(len(intersections) - 1):
        g = i + 1
        list_of_des.append([intersections[i], intersections[g]])

    for i in list_of_des:
        all_routes.append(call(i[0][0], i[1][0], i[0][1], i[1][1]))

    final_route1 = []
    for i in all_routes:
        sum = sum + i[-1][2]
        for j in i:
            final_route1.append(j[0])

    ff = len(final_route1)
    total = ff/300

    node = []
    node.append([float(inputValue_or_long), float(inputValue_or_lat)])
    for u in range(1, ff):

       node.append(final_route1[u])

    node.append([float(inputValue_des_long), float(inputValue_des_lat)])
    for i in intersections:
        i.reverse()

    print(intersections)
    print(sum, "ppp")
    print(node)
    print(dist(sum), "t")
    t = math.ceil(dist(sum))
    total_cost = math.ceil(sum*1000)
    print(total_cost)
    d = str(intersections)
    print(d)
    data = {'data': d, 'cost': str(total_cost), 'time': str(t)}
    return JsonResponse(data)


def amenity(request):
    inputValue_or_long = request.GET.get('inputValue_or_long')
    inputValue_or_lat = request.GET.get('inputValue_or_lat')
    inputValue_rad = request.GET.get('inputValue_rad')
    inputValue_amenity = request.GET.get('inputValue_amenity')
    api = overpy.Overpass()
    data = {}
    print(inputValue_rad)
    print(inputValue_amenity)
    set = []

    if inputValue_amenity == 'مدرسه':
        result = api.query("[out:json];node[amenity=school](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat, inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    elif inputValue_amenity == 'کتابخانه':
        result = api.query("[out:json];node[amenity=library](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat, inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])
    elif inputValue_amenity == 'کافه':
        result = api.query("[out:json];node[amenity=cafe](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat, inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    elif inputValue_amenity == 'رستوران':
        result = api.query(
            "[out:json];node[amenity=restaurant](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                          inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])


    elif inputValue_amenity == 'فست فود':
        result = api.query(
            "[out:json];node[amenity=fast_food](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                          inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    elif inputValue_amenity == 'فست فود':
        result = api.query(
            "[out:json];node[amenity=fast_food](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                               inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    elif inputValue_amenity == 'دانشگاه':
        result = api.query(
            "[out:json];node[amenity=university](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                               inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])


    elif inputValue_amenity == 'بانک':
        result = api.query(
            "[out:json];node[amenity=bank](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                               inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])


    elif inputValue_amenity == 'بیمارستان':
        result = api.query(
            "[out:json];node[amenity=hospital](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                               inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    elif inputValue_amenity == 'پارکینگ':
        result = api.query(
            "[out:json];node[amenity=parking](around:{},{}, {});out;".format(inputValue_rad, inputValue_or_lat,
                                                                              inputValue_or_long))
        print(result.nodes)
        for i in result.nodes:
            set.append([float(i.lon), float(i.lat)])

    set = str(set)
    set2 = str(len(set))

    data = {'set': set, 'number': set2}

    return JsonResponse(data)