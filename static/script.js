async function analyzeSentiment() {
    const topic = document.getElementById('topicInput').value.trim();
    
    if (!topic) {
        alert('Please enter a topic to analyze');
        return;
    }
    
    // Show loading, hide results
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze sentiment. Please try again.');
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

function displayResults(data) {
    document.getElementById('topicDisplay').innerText = data.topic;
    
    // Display sentiment meter (visual bar)
    const sentimentMeter = document.getElementById('sentimentMeter');
    sentimentMeter.innerHTML = `
        <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
            <div style="flex: 2;">
                <div style="background: #e0e0e0; border-radius: 10px; overflow: hidden; height: 30px;">
                    <div style="background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981); 
                                width: 100%; height: 100%; position: relative;">
                        <div style="position: absolute; left: ${data.avg_confidence}%; transform: translateX(-50%);
                                    top: -25px; font-weight: bold; color: #333;">
                            ▼ AI Confidence: ${data.avg_confidence}%
                        </div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; text-align: center; font-size: 1.5rem;">
                ${data.dominant_icon} ${data.dominant} Sentiment
            </div>
        </div>
    `;
    
    // Display stats
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-value" style="color: #10b981;">${data.overall.positive}</div>
            <div class="stat-label">Positive Articles</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: #ef4444;">${data.overall.negative}</div>
            <div class="stat-label">Negative Articles</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: #6b7280;">${data.overall.neutral}</div>
            <div class="stat-label">Neutral Articles</div>
        </div>
    `;
    
    // Display insights
    const insightsList = document.getElementById('insightsList');
    insightsList.innerHTML = data.insights.map(insight => `<li>${insight}</li>`).join('');
    
    // Display articles
    const articlesGrid = document.getElementById('articlesGrid');
    articlesGrid.innerHTML = data.articles.map(article => `
        <div class="article-card">
            <div class="article-text">"${article.text}"</div>
            <div class="article-source">📰 Source: ${article.source}</div>
            <div class="article-sentiment" style="background: ${article.color}20; color: ${article.color};">
                ${article.sentiment} (${article.confidence}% confident)
            </div>
        </div>
    `).join('');
    
    // Show results
    document.getElementById('results').style.display = 'block';
    
    // Smooth scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        analyzeSentiment();
    }
}

// Example topics for demonstration
const exampleTopics = ['Tesla', 'iPhone 15', 'AI Technology', 'Climate Change', 'Cricket World Cup'];
const inputElement = document.getElementById('topicInput');
let exampleIndex = 0;

function rotateExample() {
    inputElement.placeholder = `e.g., ${exampleTopics[exampleIndex]}`;
    exampleIndex = (exampleIndex + 1) % exampleTopics.length;
}

setInterval(rotateExample, 3000);
rotateExample();