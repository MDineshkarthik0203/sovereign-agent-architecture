import streamlit as st

from .retriever import retrieve_documents
from .web_search import web_search


st.set_page_config(
    page_title="Sovereign RAG",
    page_icon="🔐",
    layout="wide"
)


st.title("🔐 Sovereign On-Premise RAG")

st.write(
    "Search local confidential documents first. "
    "If the information is missing, search the web."
)


query = st.text_input(
    "Enter your question",
    placeholder="Ask something..."
)


if st.button("Search"):

    if not query.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching local knowledge base..."):

            result = retrieve_documents(query)


        if result["status"] == "success":

            st.success(
                "Information found in the local knowledge base."
            )

            st.subheader("📄 Local Evidence")

            for i, item in enumerate(result["evidence"]):

                st.markdown(
                    f"### Evidence {i + 1}"
                )

                st.write(
                    item["content"]
                )

                st.markdown(
                    f"**Document:** {item['document']}"
                )

                st.markdown(
                    f"**Page:** {item['page']}"
                )

                st.markdown(
                    f"**Section:** {item['section']}"
                )

                st.markdown(
                    f"**Rerank Score:** {item['rerank_score']:.4f}"
                )

                st.markdown(
                    "**Source:** Local PDF"
                )

                st.divider()


        else:

            st.warning(
                "Information was not found in the local knowledge base."
            )

            st.info(
                "Searching the web for external information..."
            )

            with st.spinner("Searching the web..."):

                web_results = web_search(query)


            if web_results:

                st.success(
                    f"Found {len(web_results)} web results."
                )

                st.subheader(
                    "🌐 External Web Evidence"
                )

                for i, item in enumerate(web_results):

                    st.markdown(
                        f"### Web Result {i + 1}"
                    )

                    st.markdown(
                        f"**Title:** {item['title']}"
                    )

                    st.write(
                        item["content"]
                    )

                    st.markdown(
                        f"**URL:** {item['url']}"
                    )

                    st.markdown(
                        "**Source:** External Web"
                    )

                    st.divider()

            else:

                st.error(
                    "Web search failed or returned no results."
                )

                st.write(
                    "Check your internet connection and "
                    "look at the terminal for the web-search error."
                )