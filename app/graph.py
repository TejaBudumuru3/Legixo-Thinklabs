from langgraph.graph import StateGraph, END
from app.state import GraphState
from app.nodes import generate_answer, retrival, grade_documents

graph = StateGraph(GraphState)

def condition_for_route(state: GraphState):
    grade = state['grade']

    if grade == 'SUFFICIENT':
        return 'answer'
    elif grade == 'INSUFFICIENT':
        return 'retrival'
    else: 
        return END

graph.add_node('retrival', retrival)
graph.add_node('grade', grade_documents)
graph.add_node('answer', generate_answer)

graph.set_entry_point('retrival')

graph.add_edge('retrival', 'grade')
graph.add_edge('answer', END)

graph.add_conditional_edges(
    'grade',
    condition_for_route,
    {
        "answer": "answer",
        'retrival': 'retrival',
        END: END
    }
)

app_graph = graph.compile()