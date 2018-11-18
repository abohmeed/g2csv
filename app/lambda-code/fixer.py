import json,urllib,boto3

def lambda_function(event,context):
    url = "http://data.fixer.io/api/latest?access_key=6ff38d3f4aa615012ee2da5b47886e15&format=1"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    filename = str(data['timestamp']) + ".csv"
    with open("/tmp/" + filename, "w") as f:
        for c,r in data['rates'].iteritems():
            f.write("{},{}\n".format(c,r))
    s3 = boto3.client('s3')
    s3.upload_file("/tmp/" + filename, 'g2csv.fixer', filename)