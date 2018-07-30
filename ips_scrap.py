# Made with love by Karlpy
import grequests, csv, json

ips_url = 'http://servicios.ips.gov.py/consulta_asegurado/comprobacion_de_derecho_externo.php'

# Cedula (id) range
id_range = 10
urls = [ips_url + str(ced) for ced in range(id_range)]

with open ('datos_ips.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['cedula', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 'nombreCompleto'])

    # grequests automatically creates a session to avoid TCP overhead. Let's create the requests generator
    requests_unsent = (grequests.get(u) for u in urls)
    # imap concurrently converts a generator object of Requests to a generator of Responses.
    requests_iterable = grequests.imap(requests_unsent, size=10)
    # iterate over the responses generator
    for response in requests_iterable:
        response_json = json.loads(response.text)
        if(response_json["presente"] == False):
            print("No existe el nro de cedula")
        else:
            print(response_json["resultado"])
            writer.writerow(response_json["resultado"].values())