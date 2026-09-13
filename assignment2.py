import argparse
import csv
import logging
from datetime import datetime
from urllib.request import urlopen


def downloadData(url):
    response = urlopen(url)
    return response.read().decode("utf-8")


def processData(file_content):
    personData = {}
    logger = logging.getLogger("assignment2")

    lines = file_content.splitlines()
    reader = csv.reader(lines)

    # Skip the header row
    next(reader)

    # Start at line 2 because line 1 is the header
    for line_number, row in enumerate(reader, start=2):
        person_id = int(row[0])
        name = row[1]
        birthday = row[2]

        try:
            birthday_object = datetime.strptime(
                birthday,
                "%d/%m/%Y"
            )

            personData[person_id] = (
                name,
                birthday_object
            )

        except ValueError:
            logger.error(
                "Error processing line #{} for ID #{}".format(
                    line_number,
                    person_id
                )
            )

    return personData


def displayPerson(id, personData):
    if id not in personData:
        print("No user found with that id")
    else:
        name, birthday = personData[id]

        print(
            "Person #{} is {} with a birthday of {}".format(
                id,
                name,
                birthday.strftime("%Y-%m-%d")
            )
        )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        required=True,
        help="URL of the CSV file"
    )

    args = parser.parse_args()

    logging.basicConfig(
        filename="error.log",
        level=logging.ERROR,
        format="%(message)s"
    )

    try:
        csvData = downloadData(args.url)

    except Exception as error:
        print("Error downloading data: {}".format(error))
        return

    personData = processData(csvData)

    while True:
        try:
            user_id = int(
                input("Enter an ID to lookup: ")
            )

        except ValueError:
            print("Please enter a valid number.")
            continue

        if user_id <= 0:
            break

        displayPerson(user_id, personData)


if __name__ == "__main__":
    main()
