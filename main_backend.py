from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import aiohttp
import asyncio
import json
from typing import List
import os
import uuid
import dotenv

dotenv.load_dotenv(override=True)

groq_api = os.getenv("GROQ_API")
blackbox_api = os.getenv("BLACKBOX_API")
serper_api = os.getenv("SERPER_API")



groq = OpenAI(api_key=groq_api, base_url="https://api.groq.com/openai/v1")

app = FastAPI(title="DevNewsCopilot – Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Items(BaseModel):
    title: str
    category: str
    source_url: str
    full_content: str
    dev_insight: str

class ListOutput(BaseModel):
    articles: List[List[Items]]

class TopicInput(BaseModel):
    prompt: str

try:
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = """You are a senior developer creating practical code examples for tech news articles. 
    Generate working code snippets that demonstrate the concepts discussed in the article.
    Focus on practical, production-ready examples that developers can use."""

BLACKBOX_URL = "https://api.blackbox.ai/chat/completions"
BLACKBOX_API_KEY = blackbox_api
BLACKBOX_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {BLACKBOX_API_KEY}"
}

SERPER_API_KEY = serper_api
SERPER_URL = "https://google.serper.dev/search"
SERPER_HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

session = None

async def get_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()
    return session

def capitalize_category(category: str) -> str:
    category_map = {
        "ai models": "AI Models",
        "research": "Research",
        "tools": "Tools",
        "ethics": "Ethics",
        "performance": "Performance",
        "security": "Security",
        "frameworks": "Frameworks"
    }
    return category_map.get(category.lower(), category.title())

async def search_with_serper(query: str, num_results: int = 5) -> List[dict]:
    session = await get_session()
    
    search_data = {
        "q": f"{query} site:github.com OR site:dev.to OR site:medium.com OR site:techcrunch.com OR site:stackoverflow.com OR site:hackernews.com",
        "num": num_results * 2
    }
    
    try:
        async with session.post(SERPER_URL, headers=SERPER_HEADERS, json=search_data) as response:
            if response.status == 200:
                result = await response.json()
                organic_results = result.get("organic", [])
                
                search_results = []
                for item in organic_results[:num_results]:
                    search_results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
                
                return search_results
            else:
                print(f"Serper API error: {response.status}")
                return []
    except Exception as e:
        print(f"Serper API error: {str(e)}")
        return []

async def generate_content_from_title_and_snippet(title: str, snippet: str, category: str) -> dict:
    content_prompt = f"""
    You are a professional technical writer. Based only on the following article title and snippet, do NOT mix or duplicate content.

    Title: {title}
    Snippet: {snippet}
    Category: {category}

    Generate exactly:
    1. "full_content": A well-structured, detailed article (500-800 words). DO NOT include summary phrases or repetition from the snippet here.
    2. "summary": A concise 2-3 sentence summary, DISTINCT from the full content.
    3. "dev_insight": A one-sentence insight about why the topic matters to developers.

    Return strictly valid JSON with the following keys:
    {{
        "full_content": "Only full article content here. No intro, no summary phrases.",
        "summary": "Distinct 2-3 sentence abstract.",
        "dev_insight": "One practical insight for developers."
    }}
    """

    
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a senior tech journalist who creates detailed technical content from article titles and snippets. Always respond with valid JSON."},
                    {"role": "user", "content": content_prompt}
                ],
                temperature=0.7,
            )
        )
        
        try:
            content_data = json.loads(response.choices[0].message.content)
            return content_data
        except json.JSONDecodeError:
            return {
                "full_content": f"Technical article about {title}. {snippet}",
                "summary": snippet,
                "dev_insight": "This is relevant for developers working with modern technology stacks."
            }
    except Exception as e:
        return {
            "full_content": f"Technical article about {title}. {snippet}",
            "summary": snippet,
            "dev_insight": "This is relevant for developers working with modern technology stacks."
        }

def categorize_article(title: str, snippet: str) -> str:
    title_lower = title.lower()
    snippet_lower = snippet.lower()
    combined = f"{title_lower} {snippet_lower}"
    
    if any(keyword in combined for keyword in ["ai", "machine learning", "llm", "gpt", "model", "neural"]):
        return "ai models"
    elif any(keyword in combined for keyword in ["research", "study", "analysis", "paper"]):
        return "research"
    elif any(keyword in combined for keyword in ["tool", "library", "framework", "sdk"]):
        return "tools"
    elif any(keyword in combined for keyword in ["security", "vulnerability", "breach", "hack"]):
        return "security"
    elif any(keyword in combined for keyword in ["performance", "optimization", "speed", "benchmark"]):
        return "performance"
    elif any(keyword in combined for keyword in ["ethics", "privacy", "bias", "fairness"]):
        return "ethics"
    elif any(keyword in combined for keyword in ["framework", "architecture", "design pattern"]):
        return "frameworks"
    else:
        return "tools"

async def run_researcher_agent(topic: str) -> List[List[str]]:
    search_results = await search_with_serper(topic, 5)
    
    if not search_results:
        return []
    
    articles = []
    for search_item in search_results:
        title = search_item["title"]
        link = search_item["link"]
        snippet = search_item["snippet"]
        
        category = categorize_article(title, snippet)
        
        content_data = await generate_content_from_title_and_snippet(title, snippet, category)
        
        article = [
            title,
            category,
            link,
            content_data["full_content"],
            content_data["summary"],
            content_data["dev_insight"]
        ]
        articles.append(article)
    
    return articles

async def process_with_groq_fallback(content: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content}
                ],
                temperature=0.3,
            )
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Groq API Error: {str(e)}"

async def process_with_blackbox(content: str) -> str:
    session = await get_session()
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [{"role": "user", "content": content}]
    
    data = {
        "model": "blackboxai/meta-llama/llama-3.1-405b-instruct",
        "messages": messages
    }

    try:
        async with session.post(BLACKBOX_URL, headers=BLACKBOX_HEADERS, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status == 402:
                print("BlackBox API payment required, falling back to Groq...")
                return await process_with_groq_fallback(content)
            elif response.status == 429:
                print("BlackBox API rate limited, falling back to Groq...")
                return await process_with_groq_fallback(content)
            elif response.status == 401:
                print("BlackBox API unauthorized, falling back to Groq...")
                return await process_with_groq_fallback(content)
            else:
                print(f"BlackBox API error {response.status}, falling back to Groq...")
                return await process_with_groq_fallback(content)
    except Exception as e:
        print(f"BlackBox API connection error, falling back to Groq: {str(e)}")
        return await process_with_groq_fallback(content)

async def generate_news_optimized(topic: str) -> dict:
    try:
        research_results = await run_researcher_agent(topic)
        
        if not research_results:
            return {"success": False, "message": "No research results found"}
        
        articles = []
        for i, result in enumerate(research_results):
            if len(result) >= 6:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": result[0],
                    "summary": result[4],
                    "insight": result[5],
                    "category": capitalize_category(result[1]),
                    "sourceUrl": result[2],
                    "fullContent": result[3],
                    "code": "// Code example will be generated..."
                }
                articles.append(article)
        
        if articles:
            code_tasks = []
            for article in articles:
                content = article.get("fullContent", "")
                code_tasks.append(process_with_blackbox(content))
            
            try:
                code_results = await asyncio.gather(*code_tasks, return_exceptions=True)
                
                for i, code_result in enumerate(code_results):
                    if i < len(articles):
                        if isinstance(code_result, Exception):
                            articles[i]["code"] = f"// Error generating code: {str(code_result)}"
                        else:
                            articles[i]["code"] = code_result
            except Exception as e:
                for article in articles:
                    article["code"] = f"// Code generation failed: {str(e)}"
        
        return {
            "success": True,
            "data": articles,
            "message": f"Generated {len(articles)} news summaries"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating news: {str(e)}",
            "data": []
        }

@app.post("/generate-news")
async def generate_news(data: TopicInput):
    result = await generate_news_optimized(data.prompt)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "DevNewsCopilot backend is running"}

@app.middleware("http")
async def add_ngrok_headers(request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

async def cleanup():
    global session
    if session:
        await session.close()
        session = None

@app.on_event("startup")
async def startup_event():
    print("🚀 DevNewsCopilot backend starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    await cleanup()
    print("🔄 DevNewsCopilot backend shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
