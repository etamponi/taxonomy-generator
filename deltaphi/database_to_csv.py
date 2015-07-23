import psycopg2

__author__ = 'Emanuele Tamponi'


def main():
    transform("easy_crafts_tal", [
        "Arts/Crafts/Ceramic_Art_and_Pottery/",
        "Arts/Crafts/Flowers/",
        "Arts/Crafts/Quilting/",
        "Arts/Crafts/Textiles/",
        "Arts/Crafts/Woodcraft/",

        "Business/Transportation_and_Logistics/Aviation/",
        "Business/Transportation_and_Logistics/Distribution_and_Log",
        "Business/Transportation_and_Logistics/Freight_Forwarding/",
        "Business/Transportation_and_Logistics/Maritime/",
        "Business/Transportation_and_Logistics/Trucking/",
    ])


def transform(csv_name, categories):
    rows = []
    with psycopg2.connect("dbname=DIEE_filtered_new user=postgres password=postgres") as conn:
        with conn.cursor() as curs:
            for category in categories:
                curs.execute("""SELECT "count", "term" FROM "Root/{}" """.format(category))
                terms, frequencies = [], []
                for count, term in curs.fetchall():
                    terms.append(term)
                    frequencies.append(count)
                curs.execute("""SELECT COUNT(*) AS documents FROM leafitems WHERE path = 'Top/{}' """.format(category))
                documents, = curs.fetchone()
                rows.append(",".join([category, str(documents), " ".join(terms), " ".join(map(str, frequencies))])
                            + "\n")
    with open("{}.csv".format(csv_name), "w") as f:
        f.writelines(rows)


if __name__ == '__main__':
    main()
