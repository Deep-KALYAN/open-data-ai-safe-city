# utils/chatbot.py
# Chatbot IA pour SafeCity avec Anthropic

import pandas as pd
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()


class SafeCityChatbot:
    """Chatbot IA pour SafeCity utilisant Claude via Anthropic."""
    
    def __init__(self, merged_df: pd.DataFrame):
        """
        Initialise le chatbot.
        
        Args:
            merged_df: DataFrame avec donnees crimes
        """
        self.data = merged_df
        self.client = Anthropic()
        self.conversation_history = []
        
        # Construire le contexte
        self.context = self._build_context()
    
    def _build_context(self) -> str:
        """
        Construit le contexte pour le chatbot.
        
        Returns:
            String avec les informations sur les donnees
        """
        years = sorted(self.data["annee"].unique().tolist())
        depts = sorted(self.data["nom_departement"].unique().tolist())
        crimes = sorted(self.data["indicateur"].unique().tolist())
        
        total_crimes = self.data["nombre"].sum()
        avg_per_dept = self.data.groupby("nom_departement")["nombre"].sum().mean()
        
        context = f"""
Vous etes un expert en criminalite et securite urbaine pour SafeCity, une application d'analyse de criminalite en France.

DONNEES DISPONIBLES :
- Periode : {years[0]} - {years[-1]}
- Departements : {len(depts)} (ex: Paris, Lyon, Marseille, etc.)
- Types de crimes : {len(crimes)}
- Total crimes enregistres : {total_crimes:,}
- Moyenne par departement : {avg_per_dept:,.0f} crimes

TYPES DE CRIMES :
{', '.join(crimes)}

PRINCIPAUX DEPARTEMENTS :
{', '.join(depts[:10])}... et {len(depts)-10} autres

INSTRUCTIONS :
1. Repondez en francais
2. Utilisez les donnees pour justifier vos reponses
3. Soyez objectif et analytique
4. Proposez des insights sur les tendances criminelles
5. Si vous ne savez pas, dites-le clairement

QUESTIONS TYPIQUES QUE VOUS POUVEZ TRAITER :
- Quels departements ont le plus de crimes?
- Comment evolue la criminalite au fil du temps?
- Quel type de crime est le plus courant?
- Comparaison entre deux departements
- Tendances et predictions
"""
        return context
    
    def chat(self, user_message: str) -> str:
        """
        Envoie un message au chatbot et recoit une reponse.
        
        Args:
            user_message: Message de l'utilisateur
        
        Returns:
            Reponse du chatbot
        """
        # Ajouter le message a l'historique
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Construire les messages pour l'API
        messages = self.conversation_history.copy()
        
        try:
            # Appeler l'API Anthropic
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                system=self.context,
                messages=messages
            )
            
            # Extraire la reponse
            assistant_message = response.content[0].text
            
            # Ajouter la reponse a l'historique
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"❌ Erreur chatbot : {str(e)}"
            print(error_msg)
            return error_msg
    
    def reset(self):
        """Reinitialise la conversation."""
        self.conversation_history = []
        print("✅ Conversation reinitialisee")
    
    def get_history(self) -> list:
        """Retourne l'historique de la conversation."""
        return self.conversation_history