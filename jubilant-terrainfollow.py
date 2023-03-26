import sys
import re

if len(sys.argv) != 2:
    print("Usage: python script_name.py filename.kml")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as f:
    data = f.read()

placemarks = re.findall(r"<Placemark>(.*?)</Placemark>", data, re.DOTALL)

for placemark in placemarks:
    alt_rel = re.findall(r"Alt Rel: (\d+\.\d+)", placemark)
    if alt_rel:
        alt_rel = float(alt_rel[0])
        print("Altitude relative to ground level: ", alt_rel, "m")

        coordinates = re.findall(r"<coordinates>(.*?)</coordinates>", placemark, re.DOTALL)
        if coordinates:
            coord_list = coordinates[0].split(",")
            coord_list[2] = str(alt_rel)
            new_coordinates = ",".join(coord_list)
            data = data.replace(coordinates[0], f"{new_coordinates}")

            data = re.sub(r"<altitudeMode>absolute</altitudeMode>", "<altitudeMode>relative</altitudeMode>", data)

new_filename = filename.split(".")[0] + "_new.kml"
with open(new_filename, "w") as f:
    f.write(data)

print(f"New file saved as {new_filename}")
