from langgraph.graph import END, StateGraph
from app.domain.entities.question import Question
from langgraph.graph import StateGraph
from app.domain.entities.state import State 
from app.infrastructure.tools.generation_tools import GenerationTool
from app.infrastructure.tools.reflection_tools import ReflectionTool
import json
class LangGraphQuestionGenerator():
    def __init__(self, generation_tool: GenerationTool, reflection_tool: ReflectionTool):
        try:
            # Create the graph
            graph_builder = StateGraph(State)
            graph_builder.add_node("generate_question", generation_tool.generate_question)
            graph_builder.add_node("reflect", reflection_tool.reflect)

            graph_builder.set_entry_point("generate_question") 
            graph_builder.add_edge("generate_question", "reflect") 

            graph_builder.add_conditional_edges(
                "reflect", reflection_tool.reflect_conditional_context
                )

            # Compile the graph
            self.graph = graph_builder.compile()

            print("Successfully initialized LangGraph Question Generator")
            
        except Exception as e:
            print(f"Error initializing LangGraph Question Generator: {str(e)}")
            raise

    def generate_question(self, category: str) -> Question:
        """
        Generate a question for a given category using the LangGraph graph.

        Args:
            category (str): The category of the question to generate.

        Returns:
            Question: The generated question and the answers.
        """
        try:
            print("Generating question")
            final_state =  self.graph.invoke({"messages":[category]})
            print("Question generated")
            content_dict = json.loads(final_state.get("content", "{}"))  # Convert JSON string to dictionary
            print(content_dict)
            return content_dict
            
        except Exception as e:
            print(f"Error in generate_question: {str(e)}")
            raise
