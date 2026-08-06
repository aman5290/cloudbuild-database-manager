from src.utils.search import filter_items


def main():

    tables = [

        "actor",

        "address",

        "film",

        "film_actor",

        "film_category",

    ]

    result = filter_items(

        tables,

        "film",

    )

    print(result)


if __name__ == "__main__":

    main()
