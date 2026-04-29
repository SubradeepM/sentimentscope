from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Sample articles database
sample_articles = {
    "technology": [
        {"text": "AI breakthrough revolutionizes healthcare with early disease detection. Amazing progress!", "source": "TechCrunch"},
        {"text": "New smartphone release disappoints users with battery issues. Poor performance.", "source": "The Verge"},
        {"text": "Cloud computing continues to grow rapidly. Companies adopting faster than expected.", "source": "Wired"},
        {"text": "Machine learning algorithms are transforming how businesses operate.", "source": "Forbes"},
    ],
    "cricket": [
        {"text": "India wins thrilling match against Australia! Fantastic performance by Kohli.", "source": "ESPN Cricinfo"},
        {"text": "Rain interrupts crucial World Cup semi-final. Fans disappointed.", "source": "BBC Sport"},
        {"text": "Young batsman breaks world record with incredible innings. Historic moment!", "source": "Cricket Today"},
        {"text": "Team celebrates victory after intense final match of the season.", "source": "Sports News"},
    ],
    "business": [
        {"text": "Stock market reaches all-time high. Economic recovery strong.", "source": "Bloomberg"},
        {"text": "Company announces layoffs amid restructuring. 5000 employees affected.", "source": "WSJ"},
        {"text": "New startup raises $100M funding. AI sector booming.", "source": "TechCrunch"},
        {"text": "Small businesses showing resilience despite economic challenges.", "source": "Business Today"},
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    topic = data.get('topic', '').strip().lower()
    
    if not topic:
        return jsonify({"error": "Please enter a topic"}), 400
    
    # Determine category
    if any(word in topic for word in ['tech', 'ai', 'phone', 'computer', 'software', 'cyber']):
        category = "technology"
    elif any(word in topic for word in ['cricket', 'sport', 'match', 'world cup', 'football']):
        category = "cricket"
    else:
        category = "business"
    
    articles = sample_articles.get(category, sample_articles["business"])
    
    analyzed_articles = []
    for article in articles:
        text = article["text"]
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'amazing', 'excellent', 'fantastic', 'wonderful', 'breakthrough', 'growing', 'booming', 'incredible', 'historic', 'win', 'wins', 'transforming']
        negative_words = ['bad', 'poor', 'disappointing', 'fail', 'failure', 'crisis', 'issue', 'problem', 'concern', 'interrupts', 'layoffs']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            sentiment = "Positive 😊"
            confidence = random.randint(75, 95)
            color = "#10b981"
        elif neg_count > pos_count:
            sentiment = "Negative 😞"
            confidence = random.randint(70, 90)
            color = "#ef4444"
        else:
            sentiment = "Neutral 😐"
            confidence = random.randint(50, 70)
            color = "#6b7280"
        
        analyzed_articles.append({
            "text": text,
            "source": article["source"],
            "sentiment": sentiment,
            "confidence": confidence,
            "color": color
        })
    
    pos_count = sum(1 for a in analyzed_articles if "Positive" in a["sentiment"])
    neg_count = sum(1 for a in analyzed_articles if "Negative" in a["sentiment"])
    neutral_count = sum(1 for a in analyzed_articles if "Neutral" in a["sentiment"])
    
    insights = [
        f"📊 Analyzed {len(articles)} recent articles about '{topic}'.",
        f"📈 Found {pos_count} positive, {neg_count} negative, and {neutral_count} neutral articles.",
    ]
    
    if pos_count > neg_count:
        insights.append("✅ Overall sentiment is POSITIVE - good public reception.")
        insights.append("💡 Continue building on this positive momentum.")
    elif neg_count > pos_count:
        insights.append("⚠️ Overall sentiment is NEGATIVE - concerns need attention.")
        insights.append("💡 Consider addressing the key issues raised.")
    else:
        insights.append("📊 Overall sentiment is MIXED - public opinion is divided.")
        insights.append("💡 Monitor trends and gather more data.")
    
    return jsonify({
        "topic": topic,
        "articles": analyzed_articles,
        "overall": {
            "positive": f"{pos_count}/{len(articles)}",
            "negative": f"{neg_count}/{len(articles)}",
            "neutral": f"{neutral_count}/{len(articles)}"
        },
        "insights": insights
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)