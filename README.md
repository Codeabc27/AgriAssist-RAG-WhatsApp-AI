# AgriAssist-RAG-WhatsApp-AI
AI-powered WhatsApp chatbot using RAG (FAISS + Groq LLM) to deliver real-time, context-aware agricultural insights.
=======
# 🌱 AgriAssist – Smart Farming Assistant (RAG + WhatsApp AI)

## 🚀 Overview

AgriAssist is an AI-powered WhatsApp chatbot that provides intelligent, context-aware agricultural guidance using Retrieval-Augmented Generation (RAG). It retrieves relevant information from a custom agricultural knowledge base and generates accurate, real-time responses for farmers.

## 🎯 Key Features

- 📱 WhatsApp-based chatbot for easy farmer access
- 🧠 Context-aware responses using RAG pipeline
- 🔍 Semantic search with vector embeddings (FAISS)
- ⚡ Fast LLM inference using Groq
- 🌾 Domain-specific agricultural knowledge integration
- 🌍 Scalable backend using FastAPI

## 🧠 System Architecture

User (WhatsApp)
      ↓
Meta WhatsApp Cloud API
      ↓
FastAPI Backend (Webhook)
      ↓
RAG Pipeline:
   - Query Embedding
   - Document Retrieval (FAISS)
   - Context Injection
      ↓
LLM (Groq)
      ↓
Response → WhatsApp User

## 🛠️ Tech Stack

- Backend: Python, FastAPI
- LLM: Groq (Mixtral / LLaMA models)
- Messaging API: Meta Platforms (WhatsApp Cloud API)
- Vector Database: FAISS
- Embeddings: SentenceTransformers
- Deployment: Render / Railway / AWS

## 📁 Project Structure

```text
AgriAssist-RAG/
│
├── app/
│   ├── main.py              # FastAPI server
│   ├── whatsapp.py          # WhatsApp webhook & messaging
│   ├── rag_pipeline.py      # RAG logic
│   ├── vector_store.py      # FAISS vector database
│   ├── llm.py               # Groq API integration
│
├── data/
│   └── agriculture_docs.txt
│
├── embeddings/
│   ├── faiss_index.bin
│   └── docs.pkl
│
├── requirements.txt
├── .env
├── README.md
```

## ⚙️ Setup Instructions

1️⃣ Clone the Repository

```bash
git clone https://github.com/Codeabc27/AgriAssist-RAG-WhatsApp-AI.git
cd AgriAssist-RAG-WhatsApp-AI
```

2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Configure Environment Variables

Create a `.env` file with the following values:

```env
GROQ_API_KEY=your_groq_api_key
WHATSAPP_ACCESS_TOKEN=your_meta_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
VERIFY_TOKEN=your_verify_token
```

4️⃣ Prepare Knowledge Base

Add agricultural data to `data/agriculture_docs.txt`.

Example:

```text
Use drip irrigation to conserve water.
Apply urea fertilizer in small quantities.
Rice grows best in warm and humid climates.
```

5️⃣ Create Vector Store

```bash
python app/vector_store.py
```

6️⃣ Run the Server

```bash
uvicorn app.main:app --reload
```

7️⃣ Configure Webhook

Go to Meta Platforms Developer Dashboard and set the webhook URL to:

```text
https://your-domain.com/webhook
```

## 💬 Example Queries

- “Best fertilizer for rice?”
- “How to improve soil fertility?”
- “Which crop is suitable for summer?”

## 📈 How It Works (RAG)

1. User sends query via WhatsApp
2. Query is converted into embeddings
3. FAISS retrieves relevant documents
4. Context + query sent to LLM
5. LLM generates accurate response

## 🔥 Future Enhancements

- 🌐 Multi-language support (Tamil + English)
- 🌦️ Weather-based recommendations
- 📸 Crop disease detection (Computer Vision)
- 📊 Farmer dashboard (analytics + insights)
- 🧠 Fine-tuned agriculture LLM

## 💼 Resume Value

This project demonstrates:

- Real-world Generative AI application
- RAG pipeline implementation
- API integration (WhatsApp + LLM)
- Scalable backend development
- Domain-specific AI solution

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

SASI R
AI/ML Developer
