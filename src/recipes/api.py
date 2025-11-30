"""
A dummi API for recipes based chatbot
"""
import random
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Recetas Aleatorias")


# Definición de un modelo Pydantic para la respuesta
class Receta(BaseModel):
    """
    Model for recipe data
    """
    nombre: str
    tema: str
    ingredientes: List[str]
    pasos: List[str]


# Diccionario de recetas de ejemplo por tema
recetas_por_tema = {
    "mexicana": [
        Receta(
            nombre="Tacos al Pastor",
            tema="mexicana",
            ingredientes=[
                "Tortillas de maíz",
                "Carne de cerdo marinada",
                "Piña",
                "Cebolla",
                "Cilantro"
                ],
            pasos=[
                "Cocinar la carne",
                "Calentar las tortillas",
                "Servir con piña, cebolla y cilantro"
                ]
        ),
        Receta(
            nombre="Guacamole Tradicional",
            tema="mexicana",
            ingredientes=[
                "Aguacates maduros",
                "Jugo de limón",
                "Cebolla picada",
                "Chile serrano",
                "Cilantro",
                "Sal"],
            pasos=[
                "Machacar los aguacates",
                "Mezclar con los demás ingredientes",
                "Servir con totopos"
                ]
        ),
    ],
    "italiana": [
        Receta(
            nombre="Spaghetti a la Carbonara",
            tema="italiana",
            ingredientes=[
                "Spaghetti",
                "Yemas de huevo",
                "Panceta o Guanciale",
                "Queso Pecorino Romano",
                "Pimienta negra"],
            pasos=[
                "Cocinar la pasta",
                "Freír la panceta",
                "Mezclar con la salsa de huevo y queso"
                ]
        ),
        Receta(
            nombre="Pizza Margherita",
            tema="italiana",
            ingredientes=[
                "Masa de pizza",
                "Salsa de tomate",
                "Mozzarella fresca",
                "Albahaca",
                "Aceite de oliva"],
            pasos=[
                "Extender la masa",
                "Agregar salsa, queso y albahaca",
                "Hornear hasta que el queso se derrita"
                ]
        ),
    ],
    "postres": [
        Receta(
            nombre="Brownies de Chocolate",
            tema="postres",
            ingredientes=[
                "Chocolate amargo",
                "Mantequilla",
                "Huevos",
                "Azúcar",
                "Harina",
                "Nueces (opcional)"],
            pasos=[
                "Derretir chocolate con mantequilla",
                "Mezclar los ingredientes húmedos y secos",
                "Hornear a 180°C"]
        ),
    ],
}

# Endpoint para obtener una receta aleatoria por tema
@app.get("/receta/{tema}", response_model=Receta)
async def get_receta_aleatoria(tema: str):
    """
    Devuelve una receta aleatoria del tema especificado.
    """
    tema = tema.lower()
    if tema not in recetas_por_tema:
        return Receta(
            nombre="Receta No Encontrada",
            tema=tema,
            ingredientes=["N/A"],
            pasos=["Lo siento, no tengo recetas para ese tema."]
        )

    # Selecciona una receta aleatoria de la lista del tema
    return random.choice(recetas_por_tema[tema])

# Endpoint para obtener los temas disponibles
@app.get("/temas")
async def get_temas():
    """
    Devuelve la lista de temas de recetas disponibles.
    """
    return {"temas": list(recetas_por_tema.keys())}
