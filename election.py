import os
import psycopg2
import psycopg2.extras
from datetime import datetime, timezone, timedelta
from configs import homepage_data


def election2024():
    # just for 2024 election homepage json
    #db = os.environ['DBNAME']
    #db_user = os.environ['DATABASE_USER']
    #db_pw = os.environ['DATABASE_PASSWORD']
    #db_host = os.environ['DATABASE_HOST']
    #db_port = os.environ['DATABASE_PORT']
    db = 'openrelationship'
    db_user = 'openrelation'
    db_pw = ''
    db_host = '35.234.56.9'
    db_port = 5432
    election_id = 85
    connection = psycopg2.connect(database=db, user=db_user,password=db_pw, host=db_host, port=db_port)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    politics_count = """
SELECT "Politic"."person", "Politic"."politicCategory", count(*) FROM "Politic", "PersonElection" WHERE "Politic"."thread_parent" IS NULL AND "Politic"."reviewed" = TRUE AND "Politic"."person" = "PersonElection"."id" AND "PersonElection"."election" = %s GROUP BY "Politic"."person", "Politic"."politicCategory";
    """ % (election_id)
    # how to get the relationship count
    # SELECT count("_Politic_factCheck"."B") FROM "_Politic_factCheck", "Politic" WHERE "_Politic_factCheck"."A" = "Politic"."id" AND "Politic"."id" = ANY(ARRAY[8031, 8032, 8033, 8034]);
    print(politics_count)
    cursor.execute(politics_count)
    all_politics = cursor.fetchall()
    for politic in all_politics:
        print(politic[0], politic[1], politic[2])
    return "ok"

def factcheck_data():
	categories = ['交通']
	for category in categories:
        gql_string = """query GetPresidents { personElections( orderBy:{ number: asc }, where: { election: {type: { equals: "總統: }, election_year_year: { equals: 2024 } }, mainCandidate: null }) { id number person_id { id name } politicsCount( where: { status: { equals: "verified" }, reviewed: { equals: true } }) politics( where: { status: { equals: "verified" }, reviewed: { equals: true } politicCategory: { name: { equals: '外交' } } }) { id content politicCategory { id name } positionChange { id isChanged factcheckPartner { id name } } positionChangeCount expertPoint { id expertPointSummary expert } expertPointCount factCheck { id factCheckSummary checkResultType factcheckPartner { id name } } factCheckCount repeat { id repeatSummary factcheckPartner { id name } } repeatCount } } }"""
        data_endpoint = DATA_SERVICE + '/gql_to_json?bucket=' + WHORU_BUCKET + '&dest_file=files/json/president_' + category + '.json&gql_string=' + gql_string
        r = requests.get(data_endpoint) 
    return "ok"

if __name__=="__main__":
    election2024();
