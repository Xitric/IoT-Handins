from rdflib import Graph

g = Graph()
g.parse('ThermistorSchema.ttl',format='turtle')

def query(g, q):
    r = g.query(q)
    return list(map(lambda row: list(row), r))


q_sensor = \
    '''
    SELECT DISTINCT ?sensor_name 
    WHERE {
        ?sensor     rdf:type        iot5:PinSensor .
        ?sensor     rdfs:label      ?sensor_name .
    }
    '''
print(query(g, q_sensor))