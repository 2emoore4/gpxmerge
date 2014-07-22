from dateutil import parser

import sys
import xml.etree.ElementTree as ET

def merge(dst, hr_list):
    print "writing closest hr measurements"
    gpx = ET.parse(dst)

    root = gpx.getroot()

    trk = None
    for child in root:
        if "trk" in child.tag:
            trk = child

    for child in trk:
        if "trkseg" in child.tag:
            for trkpt in child:
                for attr in trkpt:
                    if "time" in attr.tag:
                        timestring = attr.text
                        time = parser.parse(timestring)
                        closest = find_closest_hrm(time, hr_list)
                        trkpt.append(hr_list[closest][1])


    print "done"
    gpx.write("output.gpx")

def find_closest_hrm(time, hr_list):
    closest = min(range(len(hr_list)), key=lambda i: abs(hr_list[i][0] - time))
    return closest

def hrm_list(filename):
    ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
    ET.register_namespace('gpxtpx', "http://www.garmin.com/xmlschemas/TrackPointExtension/v1")

    print "creating hr list"
    gpx = ET.parse(filename)
    root = gpx.getroot()
    trk = root[1]
    trkseg = trk[1]

    measurements = []
    for trkpt in trkseg:
        timestring = trkpt[1].text
        time = parser.parse(timestring)
        if len(trkpt) == 3:
            measurements.append([time, trkpt[2]])

    print "done"
    return measurements

def main():
    print "merging gpx files"
    dst = sys.argv[1]
    src = sys.argv[2]

    hr_measurements = hrm_list(src)

    merge(dst, hr_measurements)

if __name__ == "__main__":
    main()
