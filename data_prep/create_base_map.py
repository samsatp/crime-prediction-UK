import folium, os, re

def create_base_map():
    kml_files = os.listdir('data/force_kmls')

    print('reading coordinates')
    doc = []
    for kml_file in kml_files:
        with open('data/force_kmls/'+kml_file, 'rt', encoding="utf-8") as myfile:
            doc.append(myfile.read())


    print('parsing')
    searched = [ re.search("<coordinates>.*</coordinates>", e) for e in doc]

    coords = [
        e[s.start()+len('<coordinates>'): s.end()-len('</coordinates>')-1]
        for e, s in zip(doc, searched)
        ]
    coords = [e.split() for e in coords]
    coords = [[ tuple(e.split(',')[:2]) for e in coord] for coord in coords]
    coords = [[(float(e[1]), float(e[0])) for e in coord] for coord in coords ]

    print('create a map')
    mapObj = folium.Map(location=[52.8739609957, -0.354840987388],
                        zoom_start=5)

    for coord in coords:
        folium.Polygon(coord,
                    color="blue",
                    weight=2,
                    fill=True,
                    #fill_color="orange",
                    fill_opacity=0.4).add_to(mapObj)

    mapObj.save('data_prep/force_boundaries.html')
    print("done")