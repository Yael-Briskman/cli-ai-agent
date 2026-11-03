import os
from dotenv import load_dotenv
from google import genai
import gradio as gr

# טעינת מפתח ה-API מקובץ ה-.env
load_dotenv()

# אתחול הלקוח של גוגל
client = genai.Client()


def generate_cli_command(user_input: str) -> str:
    system_instruction = """
       תפקידך להמיר בקשה מילולית מהמשתמש לפקודת cli של windows מותאמת לתוכן הבקשה,
        לדוגמה: המשתמש שואל- "מה כתובת ה-IP של המחשב שלי" והתשובה המבוקשת היא ipconfig
        התוכן החוזר יהיה הפקודה עצמה בלבד, ללא שום טקסט נוסף
        במקרה והמשתמש מבקש פקודה מסוכנת או רגישה כמו format וכדומה יש לסרב במשפט קצר
        במקרה והבקשה אינה מציאותית יש לענות במשפט קצר ותואם
        
    """

    # שליחת הבקשה למודל של גוגל
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{system_instruction}\n\nUser Request: {user_input}",
    )

    return response.text


# ממשק Gradio עם תיאור קצר וממוקד
demo = gr.Interface(
    fn=generate_cli_command,
    inputs=gr.Textbox(label="Enter your request in natural language"),
    outputs=gr.Textbox(label="Generated CLI Command"),
    title="Prompt Engineering - CLI Agent",
    description="המרת שפה טבעית לפקודות טרמינל באמצעות AI.",
)

if __name__ == "__main__":
    demo.launch()