import requests
import json
import pandas

def get():
    response = requests.get("http://data-mobility.irisnet.be/resources/artisticheritage-2016-01-01.json")

    raw_data = json.loads(response.text)

    data = []
    for entry in raw_data["features"]:
        flat_entry = {}
        for k,v in entry.items():
            if type(v) is not dict:
                flat_entry[k] = v
            else:
                for k2,v2 in v.items():
                    if k2 == "coordinates":
                        flat_entry["%s_%s_lat" % (k, k2)] = v2[0]
                        flat_entry["%s_%s_lon" % (k, k2)] = v2[1]
                    else:
                        flat_entry["%s_%s" % (k, k2)] = v2
        data.append(flat_entry)
        
    df = pandas.DataFrame(data)
    df["properties_build_year"] = df["properties_build_year"].map(lambda a: -1 if a is None else int(a))

    return df