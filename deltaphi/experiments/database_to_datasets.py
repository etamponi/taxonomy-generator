import psycopg2

__author__ = 'Emanuele Tamponi'


def main():
    from dataset_definitions import definitions

    for name, parents in definitions:
        transform(name, parents)


def transform(csv_name, parents):
    rows = []
    with psycopg2.connect("dbname=DIEE_filtered_new user=postgres password=postgres") as conn:
        with conn.cursor() as curs:
            for parent in parents:
                curs.execute(
                    """SELECT tablename FROM pg_tables WHERE SUBSTRING(tablename FROM 'Root/{}/.+/') <> ''"""
                    .format(parent)
                )
                categories = [row[0][len("Root/"):-1] for row in curs.fetchall()]
                for category in categories:
                    curs.execute("""SELECT "count", "term" FROM "Root/{}/" """.format(category))
                    terms, frequencies = [], []
                    for count, term in curs.fetchall():
                        terms.append(term)
                        frequencies.append(count)
                    frequencies.sort()
                    curs.execute("""SELECT COUNT(*) AS documents FROM leafitems WHERE path = 'Top/{}/' """
                                 .format(category))
                    documents, = curs.fetchone()
                    rows.append(",".join([
                        category,
                        str(documents),
                        " ".join(sorted(terms)), " ".join(map(str, frequencies))
                    ]) + "\n")
    with open("datasets/{}.csv".format(csv_name), "w") as f:
        f.writelines(rows)


if __name__ == '__main__':
    main()
