from ddgs import DDGS


def web_search(
    query,
    max_results=5
):

    try:

        results = []


        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )


            for item in search_results:

                results.append(
                    {
                        "source_type": "web",

                        "title": item.get(
                            "title",
                            ""
                        ),

                        "url": item.get(
                            "href",
                            ""
                        ),

                        "content": item.get(
                            "body",
                            ""
                        )
                    }
                )


        print(
            "Web results found:",
            len(results)
        )


        return results


    except Exception as e:

        print(
            "Web search error:",
            e
        )

        return []