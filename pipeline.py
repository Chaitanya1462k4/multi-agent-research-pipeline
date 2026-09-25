from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str)->dict:
    state={}
    print("\n"+"="*50)
    print("step 1- search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"find recent,reliable and detailed information about :{topic}")]}
    )

    # Pull the raw tool output (has real URLs) instead of the LLM's paraphrased summary
    tool_messages = [m for m in search_result["messages"] if getattr(m, "type", None) == "tool"]
    if tool_messages:
        state["search_results"] = "\n\n".join(m.content for m in tool_messages)
    else:
        # fallback if no tool call was made
        state["search_results"] = search_result["messages"][-1].content
    
    print("\n search result ",state['search_results'])



    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting a report ...")
    print("="*50)

    research_combined=(
        f"SEARCH RESULTS : \n {state['search_results']}"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}" 
    )

    state['report']=writer_chain.invoke({
        'topic':topic,
        'research':research_combined
    })

    print("\nFinal Report: \n",state["report"])

    print("\n"+" ="*50)
    print("step 4 - Critic is reviewing the report ...")
    print("="*50)

    state['Critic']=critic_chain.invoke({
        'report':state['report']
    })

    print("\nCritic Review: \n",state["Critic"])

    return state

if __name__=="__main__":
    topic=input("\nENTER THE TOPIC: ")
    run_research_pipeline(topic)