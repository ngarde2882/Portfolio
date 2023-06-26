import requests

GOOGLE_API_KEY = 'GOOGLE API KEY HERE'

def extract_neighborhood_via_address(address_or_zipcode):
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None
    try:
        results = r.json()['results'][0]
        try:
            i = results['postcode_localities']
            out = ''
            for x in i:
                if x != 'Houston':
                    out += x + '.'
        except:
            if results['address_components'][2]['types'][0] in ('neighborhood', 'locality'):
                out = results['address_components'][2]['long_name']
            elif results['address_components'][1]['types'][0] in ('neighborhood', 'locality'):
                out = results['address_components'][1]['long_name']
            else:
                out = None
    except:
        pass
    return out

def return_req(address_or_zipcode):
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None
    try:
        results = r.json()['results'][0]
    except:
        pass
    return results

def main():
    f = open("Desktop/CONFIDENTIAL - Google Sub-market Lookup - Nicholas Garde.csv", errors="ignore")
    o = open("Desktop/outfile.csv", 'w') # TODO
    # line = 1
    f.readline() # drop first line key
    o.write("Address,City,Zip Code,Corrected / Validated USPS Address,Google Maps Submarket\n") # TODO
    for x in f:
        # line+=1
        # print(f'{line}: {x}')
        x = x.split(',')
        try:
            add = x[0]
            city = x[1]
            zip = x[2]
            if add[0] == ' ':
                add = add[1:]
            if add[-1] == ' ':
                add = add[:-1]
            zip = int(zip)
            # print(f'{line}: {add}, {city}, TX {zip}')
            corrected = f'\"{add}, {city}, TX {zip}\"'
            neighborhood = extract_neighborhood_via_address(corrected)
            if neighborhood == None:
                neighborhood = extract_neighborhood_via_address(corrected)
            if neighborhood == None:
                neighborhood = '?'
            o.write(f'{add},{city},{zip},{corrected},{neighborhood}\n') # TODO
        except:
            # print(line)
            continue
    o.close() # TODO
    f.close()

def make_all_req():
    f = open("Desktop/CONFIDENTIAL - Google Sub-market Lookup - Nicholas Garde.csv", errors="ignore")
    o = open("Desktop/req.txt", 'w') # TODO
    # line = 1
    f.readline() # drop first line key
    o.write("Address,City,Zip Code,Corrected / Validated USPS Address,Google Maps Submarket\n") # TODO
    for x in f:
        # line+=1
        # print(f'{line}: {x}')
        x = x.split(',')
        try:
            add = x[0]
            city = x[1]
            zip = x[2]
            if add[0] == ' ':
                add = add[1:]
            if add[-1] == ' ':
                add = add[:-1]
            zip = int(zip)
            corrected = f'\"{add}, {city}, TX {zip}\"'
            o.write(f'{return_req(corrected)}\n') # TODO
        except:
            continue
    o.close() # TODO
    f.close()

# print(return_req('insert example address here'))
# make_all_req()
main()