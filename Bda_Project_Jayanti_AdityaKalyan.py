__author__ = "Aditya Kalyan Jayanti"
__email__ = "aj8582@rit.edu"

import csv
import haversine


def convert_lat_long_to_degrees(value, direction):
    """
    Function to convert to degrees
    +ve value indicates 'N' or 'E'
    -ve value indicates 'S' or 'W'
    :param value: value to be converted to fractional degrees
    :param direction: direction of path mentioned in GPS data
    :return:
    """
    a = float(value)
    b = int(a / 100)
    a = a - b * 100
    f = a / 60
    result = b + f

    if direction == "N" or direction == "E":
        result *= 1
    if direction == "S" or direction == "W":
        result *= -1

    return result


def read_input(filename):
    """
    To read the input of the file
    :param filename: File path of the input file
    :return: Data for the attributes, attribute names, row indices
    """
    # To store all the rows of gps data
    row_of_gps_data = []

    with open(filename) as file:
        for index in range(5):
            next(file)

        reader = csv.reader(file, delimiter=",")

        for row in reader:
            # type of data
            field = row[0]

            if field == "$GPRMC" and row[3] != '':
                row[3] = convert_lat_long_to_degrees(row[3], row[4])
                row[5] = convert_lat_long_to_degrees(row[5], row[6])
                row_of_gps_data.append(row)
            else:
                continue
    return row_of_gps_data


def emit_header(filename):
    """
    Function to generate the header of the KML file
    :param filename: file to be written
    :return: file pointer
    """
    file = open(filename, "w")
    file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')
    file.write('<Style id="yellowPoly">\n')
    file.write('\t<LineStyle>\n')
    file.write('\t\t<color>Af00ffff</color>\n')
    file.write('\t\t<width>6</width>\n')
    file.write('\t</LineStyle>\n')
    file.write('\t<PolyStyle>\n')
    file.write('\t\t<color>7f00ff00</color>\n')
    file.write('\t</PolyStyle>\n')
    file.write('</Style>\n')
    file.write('<Placemark><styleUrl>#yellowPoly</styleUrl>\n')
    file.write('<LineString>\n')
    file.write('<Description>Speed in MPH, not altitude.</Description>\n')
    file.write('\t<extrude>1</extrude>\n')
    file.write('\t<tesselate>1</tesselate>\n')
    file.write('\t<altitudeMode>absolute</altitudeMode>\n')
    file.write('\t<coordinates>\n')
    return file


def emit_trailer(file):
    """
    Function to generate the trailer for the KML file
    :param file: file to be written
    :return: None
    """
    file.write('\t</coordinates>\n')
    file.write('</LineString>\n')
    file.write('</Placemark>\n')
    file.write('</Document>\n')
    file.write('</kml>\n')


def emit_trailer_best_path(file, list_of_stops, left_turns):
    """
    Function to generate the trailer for
    the KML file
    :param list_of_stops: list of stops signs
    :param file: file to be written
    :param left_turns: list of locations of left turns
    :return: None
    """
    file.write('\t</coordinates>\n')
    file.write('</LineString>\n')
    file.write('</Placemark>\n')
    for pair in list_of_stops:
        file.write('<Placemark>\n')
        file.write('<description>Red PIN for A Stop</description>\n')
        file.write('<Style id="normalPlacemark">\n')
        file.write('<IconStyle>\n')
        file.write('<color>ff0000ff</color>\n')
        file.write('<Icon>\n')
        file.write('<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n')
        file.write('</Icon>\n')
        file.write('</IconStyle>')
        file.write('</Style>\n')
        file.write('<Point>\n')
        file.write('<coordinates>\n')
        file.write("\t\t" + str(pair[1]) + "," + str(pair[0]) + "," + "300" + "\n")
        file.write('</coordinates>\n')
        file.write('</Point>\n')
        file.write('</Placemark>\n')
    for pair in left_turns:
        file.write('<Placemark>\n')
        file.write('<description>Default Pin is Yellow</description>\n')
        file.write('<Point>\n')
        file.write('<coordinates>\n')
        file.write("\t\t" + str(pair[1]) + "," + str(pair[0]) + "," + "300" + "\n")
        file.write('</coordinates>\n')
        file.write('</Point>\n')
        file.write('</Placemark>\n')

    file.write('</Document>\n')
    file.write('</kml>\n')


def knots_to_miles(speed):
    """
    Function to convert knots to miles
    :param speed: speed in miles
    :return: speed in mph
    """
    return float(speed) * 1.151


def gps_time_to_min(time):
    """
    Converts gps time to iso using astropy package
    :param time: gps time
    :return: time in minutes
    """
    hours = time[:2]
    minutes = time[2:4]
    seconds = time[4:]

    hours_to_min = int(hours) * 60
    seconds = float(seconds) / 60

    total = hours_to_min + int(minutes) + seconds
    return total


def best_emit_body(file, data):
    """
    Generates the body of the KML file
    :param file: file to be written
    :param data: pair of (lat,long)
    :return: file pointer
    """
    for pair in data:
        file.write("\t\t" + str(pair[1]) + "," + str(pair[0]) + "," + "300" + "\n")
    return file


def emit_body(file, data):
    """
    Generates the body of the KML file
    :param file: file to be written
    :param data: pair of (lat,long)
    :return: file pointer
    """
    for pair in data:
        file.write("\t\t" + str(pair[1]) + "," + str(pair[0]) + "," + "300" + "\n")
    return file


def clean_data(row_of_gps_data):
    """
    To clean the GPS data by avoiding duplicate values
    :param row_of_gps_data: a list of list of GPS values
    :return: list of tuples of (lat,long)
    """
    list_cleaned_gps_data = []
    new_list_cleaned_gps_data = []

    for row in row_of_gps_data:
        data = (row[3], row[5])
        list_cleaned_gps_data.append(data)

    for pair in list_cleaned_gps_data:
        if pair not in new_list_cleaned_gps_data:
            new_list_cleaned_gps_data.append(pair)

    return new_list_cleaned_gps_data


def cleaned_data_stop_left_cost(row_of_gps_data):
    """
    To clean the GPS data by avoiding duplicate values for
    the cost function
    :param row_of_gps_data: a list of list of GPS values
    :return: cleaned data
    """
    list_cleaned_gps_data = []
    cleaned_gps_data = []

    for row in row_of_gps_data:
        data = (gps_time_to_min(row[1]), row[3], row[5], knots_to_miles(row[7]), row[8])
        list_cleaned_gps_data.append(data)

    for pair in list_cleaned_gps_data:
        if pair not in cleaned_gps_data:
            cleaned_gps_data.append(pair)

    return cleaned_gps_data


def cost_function(travel_time, max_velocity):
    """
    cost function to find the best cost function by
    minimizing the objective function
    :param travel_time: total travel time of the trip
    :param max_velocity: maximum velocity of trip in mph
    :return: cost
    """
    objective_function = travel_time
    regularization = max_velocity
    cost = (objective_function / 30) + 0.5 * (regularization / 60)
    return cost


def task4_find_optimum_track(data):
    """
    Helper method calls the cost function to find the best
    optimal path
    :param data: contains a list of cleaned data
    :return: cost
    """
    speed = []
    time_difference = data[-1][0] - data[0][0]

    for value in data:
        speed.append(value[3])

    cost = cost_function(time_difference, max(speed))

    return cost


def calculate_distance(x1, x2, y1, y2):
    """
    Function to calculate the distance between two points
    :return: distance between the points in miles
    """
    # haversine distance in kilometers
    distance = haversine((x1, y1), (x2, y2), miles=True)

    return distance


def calculate_stop_signs(best_gps_data):
    """
    Method to calculate the number of stops in route
    Using temporal sequential analysis algorithm
    :param: data: contains a list of tuple values (lat,long,speed,angle)
    :return: (lat,long) position of stop sign
    """
    # holds the (lat,long) of stop locations
    list_of_stop_signs = []

    # to convert the list of tuples(cleaned data) to a list of lists
    list_of_lists_best_gps_data = [list(x) for x in best_gps_data]

    for row in list_of_lists_best_gps_data:
        for values in list_of_lists_best_gps_data[
                      list_of_lists_best_gps_data.index(row) + 1:list_of_lists_best_gps_data.index(row) + 8]:
            # values[0] - row[0] => Time difference compare it with threshold time
            # row[3] => speed => Speed threshold
            if (values[0] - row[0]) >= 0.0005 and row[3] <= 0.0005:
                if not list_of_stop_signs:
                    list_of_stop_signs.append((row[1], row[2]))
                else:
                    last_position_of_list = list_of_stop_signs[-1]
                    distance = calculate_distance(last_position_of_list[0], row[1], last_position_of_list[1], row[2])
                    if distance <= 0.05:
                        del list_of_stop_signs[-1]
                list_of_stop_signs.append((row[1], row[2]))
    return list_of_stop_signs


def left_hand_turns(best_gps_data):
    """
    Function to find the location of a left turn
    :param best_gps_data:
    :return: list of left hand turns
    """
    left_turns = []
    # to convert the list of tuples(cleaned data) to a list of lists
    list_of_lists_best_gps_data = [list(x) for x in best_gps_data]

    for row in list_of_lists_best_gps_data:
        for values in list_of_lists_best_gps_data[
                      list_of_lists_best_gps_data.index(row) + 1:list_of_lists_best_gps_data.index(row) + 2]:
            angle1 = float(row[4])  # current angle
            angle2 = float(values[4])   # next angle
            difference = abs(angle2 - angle1)
            angle = difference
            if -180 < difference and difference < 180:
                angle = difference
            elif difference <= -180:
                angle = difference + 360
            elif difference >= 180:
                angle = difference - 360
            if angle > 0:
                continue
            else:
                # negative angle indicates left turns
                left_turns.append((row[1], row[2]))
    return left_turns


def main():
    """
    calculates the number of stop signs, left turns, best path
    :return: None
    """

    input_file_list_task1 = [
        "InputFiles/ZI8G_ERF_2018_08_16_1428.txt", "InputFiles/ZI8H_HJC_2018_08_17_1745.txt",
        "InputFiles/ZI8J_GKX_2018_08_19_1646.txt", "InputFiles/ZI8K_EV7_2018_08_20_1500.txt",
        "InputFiles/ZI8N_DG8_2018_08_23_1316.txt", "InputFiles/ZIAA_CTU_2018_10_10_1255.txt",
        "InputFiles/ZIAB_CIU_2018_10_11_1218.txt", "InputFiles/ZIAC_CO0_2018_10_12_1250.txt"
    ]

    output_file_write_task1 = [
        "KMLFiles_Task1/ZI8G_ERF_2018_08_16_1428.kml", "KMLFiles_Task1/ZI8H_HJC_2018_08_17_1745.kml",
        "KMLFiles_Task1/ZI8J_GKX_2018_08_19_1646.kml", "KMLFiles_Task1/ZI8K_EV7_2018_08_20_1500.kml",
        "KMLFiles_Task1/ZI8N_DG8_2018_08_23_1316.kml", "KMLFiles_Task1/ZIAA_CTU_2018_10_10_1255.kml",
        "KMLFiles_Task1/ZIAB_CIU_2018_10_11_1218.kml", "KMLFiles_Task1/ZIAC_CO0_2018_10_12_1250.kml"
    ]

    # to keep track of which output file to write
    i = 0

    # to obtain the min cost path
    cost_list = []

    # map to hold file name as key & cost as value
    best_file_map = {}

    for input_file in input_file_list_task1:
        emit_header_file = emit_header(output_file_write_task1[i])
        row_of_gps_data = read_input(input_file)
        data = clean_data(row_of_gps_data)
        emit_body_file = emit_body(emit_header_file, data)
        emit_trailer(emit_body_file)
        data = cleaned_data_stop_left_cost(row_of_gps_data)
        cost = task4_find_optimum_track(data)
        cost_list.append(cost)
        best_file_map[input_file] = cost
        i += 1

    # to retrieve file name, cost with the minimum cost function
    best_file, best_cost = min(best_file_map.items(), key=lambda best_file_map: best_file_map[1])
    print("\nBest path is " + best_file + " has a cost of: " + str(best_cost))

    # output file of best_file
    best_out = "best_output_file.kml"

    # write the header of best output file
    emit_header_file = emit_header(best_out)

    # read the best file
    best_gps_data = read_input(best_file)

    # to clean the data
    best_gps_data = cleaned_data_stop_left_cost(best_gps_data)

    temp = []
    for row in best_gps_data:
        temp.append((row[1], row[2]))

    # write the body of the best output file
    emit_body_file = best_emit_body(emit_header_file, temp)

    # print(best_gps_data)

    # calculate left hand turns
    left_turns = left_hand_turns(best_gps_data)
    no_duplicates_left_turn = []
    for l in left_turns:
        if l not in no_duplicates_left_turn:
            no_duplicates_left_turn.append((l[0], l[1]))

    # to calculate the stop signs
    list_of_stops = calculate_stop_signs(best_gps_data)

    # write the trailer of the best output file
    emit_trailer_best_path(emit_body_file, list_of_stops, no_duplicates_left_turn)

    # list of stop signs
    # (lat,long) per stop, sorted from largest to lowest long
    print("\nlist of stop signs (lat,long):\n" + str(sorted(list_of_stops, key=lambda x: x[1], reverse=True)))

    # list of left turns
    lt = []
    for i in no_duplicates_left_turn:
        lt.append((i[1], i[0]))

    # (long,lat) points out sorted from highest to lowest longitude
    print("\n\nlist of left turn (long,lat):\n" + str(sorted(lt, key=lambda x: x[0], reverse=True)))


# # ZI8G_ERF_2018_08_16_1428 (1st data file)
# emit_header_file = emit_header(output_file_write_task1[0])
# row_of_gps_data = read_input(input_file_list_task1[0]) \
#
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZI8H_HJC_2018_08_17_1745 (2nd data file)
# emit_header_file = emit_header(output_file_write_task1[1])
# row_of_gps_data = read_input(input_file_list_task1[1])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZI8J_GKX_2018_08_19_1646 (3rd data file)
# emit_header_file = emit_header(output_file_write_task1[2])
# row_of_gps_data = read_input(input_file_list_task1[2])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZI8K_EV7_2018_08_20_1500 (4th data file)
# emit_header_file = emit_header(output_file_write_task1[3])
# row_of_gps_data = read_input(input_file_list_task1[3])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZI8N_DG8_2018_08_23_1316 (5th data file)
# emit_header_file = emit_header(output_file_write_task1[4])
# row_of_gps_data = read_input(input_file_list_task1[4])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZIAA_CTU_2018_10_10_1255 (6th data file)
# emit_header_file = emit_header(output_file_write_task1[5])
# row_of_gps_data = read_input(input_file_list_task1[5])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZIAB_CIU_2018_10_11_1218 (7th data file)
# emit_header_file = emit_header(output_file_write_task1[6])
# row_of_gps_data = read_input(input_file_list_task1[6])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)
#
# # ZIAC_CO0_2018_10_12_1250 (8th data file)
# emit_header_file = emit_header(output_file_write_task1[7])
# row_of_gps_data = read_input(input_file_list_task1[7])
# data = clean_data(row_of_gps_data)
# emit_body_file = emit_body(emit_header_file, data)
# emit_trailer(emit_body_file)


if __name__ == '__main__':
    main()


