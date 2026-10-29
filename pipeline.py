from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_pipeline(topic :str) -> dict:
        state = {}



        #search agent 
        print("\n"+"="*50)
        print("step 1 - seraching agent working ...")
        print("="*50)

        search_agent = build_search_agent()
        search_results = search_agent.invoke({
                "messages" : [("user", f"Search for recent and reliable information on the topic: {topic}")]
        })

        state['search_results'] = search_results["messages"][-1].content

        print("\n search results ", state['search_results'])



        #search agent 
        print("\n"+"="*50)
        print("step 2 - reader agent working ...")
        print("="*50)

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })

        state["scraped_content"] = reader_result["messages"][-1].content

        print("\n scraped content ", state['scraped_content'])




        # writer's report 
        print("\n"+"="*50)
        print("step 3 - writer is drafting the report ...")
        print("="*50)

        research_combined =(
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPE CONTENT:\n{state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
        })

        print("\n Final Report\n ", state['report'])



        # crictic report 
        print("\n"+"="*50)
        print("step 4 - critic is reviewing the report...")
        print("="*50)


        state["feedback"] = critic_chain.invoke({
                "report": state["report"]
        })

        print("\n Critic Report\n ", state['feedback'])


        return state

if __name__ == "__main__":
    topic = input("Enter a topic to research: " )
    run_pipeline(topic)