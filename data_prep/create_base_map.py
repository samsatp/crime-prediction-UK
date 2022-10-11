import folium, os, re
import json

def create_base_map():
    kml_files = os.listdir('data/force_kmls')

    print('reading coordinates')
    doc = {}
    for kml_file in kml_files:
        force_name = kml_file[:-4]
        with open('data/force_kmls/'+kml_file, 'rt', encoding="utf-8") as myfile:
            doc[force_name] = myfile.read()


    print('parsing')
    searched = {force: re.search("<coordinates>.*</coordinates>", e) for force, e in doc.items()}

    coords = {}
    for force in doc.keys():
        raw_text = doc[force][searched[force].start() + len('<coordinates>') : searched[force].end()-len('</coordinates>')-1]
        raw_text = raw_text.split()
        raw_text = [ list(e.split(',')[:2]) for e in raw_text]

        coords[force] = [[float(e[1]), float(e[0])] for e in raw_text]

    print('create a map')
    mapObj = folium.Map(location=[52.8739609957, -0.354840987388],
                        zoom_start=5)

    with open('VIZ/coords.json', 'w') as f:
        print(coords.keys())
        json.dump(coords, f)

    for coord in coords:
        folium.Polygon(coord,
                    color="blue",
                    weight=2,
                    fill=True,
                    #fill_color="orange",
                    fill_opacity=0.4).add_to(mapObj)

    #mapObj.save('data_prep/force_boundaries.html')
    print("done")

if __name__ == '__main__':
    create_base_map()