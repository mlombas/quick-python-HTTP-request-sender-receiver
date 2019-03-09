from print_json import print_json
import http.client as http
import urllib.parse as parse

def gen_qs(query):
    out = "?"
    for k, v in query.items():
        for arg in v:
            out += f"{k}={arg}"

            out += "&"
    
    return out[:-1] #Eliminate last char, that will be an unnecesary &


running = True
while running:
    url = input("Please enter url: ")
    if not url:
        print("invalid url, try again")
        continue
    
    #get additional querys
    query = parse.parse_qs(parse.urlparse(url).query, True) #true to keep blank parameters
    print("Enter additional query parameters, or an empty line to end")
    q = input()
    while q:
        q = [arg.strip() for arg in q.split("=")]
        if q[0] in query:
            query[q[0]].append(q[1] if len(q) == 2 else "")
        else:
            query[q[0]] = [q[1] if len(q) == 2 else ""]

        q = input()
    
    #parse query and append to url again
    url += gen_qs(query)

    #get headers
    headers = {}
    print("Enter header params, or empty line to end")
    head = input()
    while head:
        try:
            name, value = (arg.strip() for arg in head.split(":"))
        except:
            print("Invalid values, try again")

        if name in headers:
            print("Header already exists, try again")
        else:
            headers[name] = value

        head = input()

    #get data
    data = input("Enter data: \n")

    #get method
    method = input("Enter the method you want to use: ")

    conn = http.HTTPConnection(url)
    conn.request(method, "", data, headers)
    with conn.getresponse() as res:
        print(f"Status: {res.status} ({res.reason})")
        print("Data: \n")
        if res.getheader("Content-type").find("json") != -1: #if data returned is json, print it nicely with print_json
            print_json(str(res.read()))
        else:
            print(str(res.read()))

    ans = input("Do you want to request again? (y/n)")
    if ans == "n":
        running = False

