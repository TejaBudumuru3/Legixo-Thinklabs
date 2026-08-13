from langgraph.graph import StateGraph, END
from app.state import GraphState
from app.nodes import generate_answer, retrieval, grade_documents

graph = StateGraph(GraphState)

def condition_for_route(state: GraphState):
    grade = state.get('grade', '') 

    if grade == 'SUFFICIENT':
        return 'answer'
    elif grade == 'INSUFFICIENT':
        return 'retrieval'
    else: 
        return END

graph.add_node('retrieval', retrieval)
graph.add_node('grade', grade_documents)
graph.add_node('answer', generate_answer)

graph.set_entry_point('retrieval')

graph.add_edge('retrieval', 'grade')
graph.add_edge('answer', END)

graph.add_conditional_edges(
    'grade',
    condition_for_route,
    {
        "answer": "answer",
        'retrieval': 'retrieval',
        END: END
    }
)

app_graph = graph.compile()