from langgraph.graph import END
from app.domain.entities.state import State
from typing import Literal
from app.domain.entities.reflect_agent import Reflect
from app.infrastructure.datasource.azure_openai_llm import LlmProvider
class ReflectionTool:
    def __init__(self,llm_provider: LlmProvider):
        self.llm = llm_provider.get_llm()

    def reflect(self, state: State):
        if(state.get("loop_needed", False) or False):
            return {
                "loop_needed": False,
                "updated_content" : state.get("updated_content","")
            }  
        else:
            result = self.llm.with_structured_output(Reflect).invoke(state["content"])
            print(result.reason)
            print(result.output)
            return {
                "loop_needed": result.loop_needed,
                "updated_content" : result.output
            }

    def reflect_conditional_context(self, state: State) -> Literal["generate_question", END]:
        if state.get("loop_needed", False):
            return "generate_question"
        else:
                return END