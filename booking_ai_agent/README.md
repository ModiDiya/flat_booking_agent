# Booking AI Agent

### Steps to Run
1. Unzip project into VS Code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your **Groq API key** in `.env`:
   ```
   GROQ_API_KEY=your_groq_key_here
   ```
4. Download Google Cloud credentials JSON and save as `credentials.json` in project root.
   - Enable **Google Calendar API** and **Gmail API** in Google Cloud Console.
   - Create Service Account → Download JSON.
5. Run the app:
   ```bash
   python backend/agent.py
   ```
6. Test endpoints:
   - Chat: `POST http://127.0.0.1:5000/chat`
   - Booking: `POST http://127.0.0.1:5000/book`
