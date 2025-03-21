from app.domain.entities.generator_agent import GenerateQuestion
from app.domain.entities.state import State
from app.infrastructure.datasource.azure_openai_llm import LlmProvider

class GenerationTool():
    def __init__(self, llm_provider: LlmProvider):
        self.llm = llm_provider.get_llm()

    def generate_question(self,state: State):
        if(len(state.get("updated_content",""))>0 or False):
            return {"content":state.get("updated_content","")}
        else: 
            result =  self.llm.with_structured_output(GenerateQuestion).invoke(state["messages"])
            print(result.output)
            #return {"content":result.output}
            return {"content":"{\"question\":\"¿Cuál es el río más largo del mundo?\",\"correctAnswer\":\"Río Amazonas\",\"incorrectAnswers\":[\"Río Nilo\",\"Río Mississippi\",\"Río Ebro\"]}"}