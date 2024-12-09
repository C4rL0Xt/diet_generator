from core.api import GeminiAPI

class DietaGenerator:
    def __init__(self):
        self.api = GeminiAPI()
        self.prompt_template = (
            """
            Crear una dieta personalizada para una persona con un IMC de {imc}, sexo {sexo}, 
            y preferencias alimenticias {preferencias}. 
            Indique los alimentos sugeridos para desayuno, almuerzo, cena y snacks. 
            Asegúrese de proporcionar un análisis nutricional detallado, 
            incluyendo calorías, proteínas, grasas y carbohidratos por comida. 
            Use un lenguaje formal y claro.
            """
        )

    def generar_dieta(self, imc, sexo, preferencias):
        prompt = self.prompt_template.format(imc=imc, sexo=sexo, preferencias=preferencias)
        dieta = self.api.generate_diet(prompt)
        return dieta
