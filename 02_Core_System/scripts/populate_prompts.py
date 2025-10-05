#!/usr/bin/env python3
"""
Populate detailed properties for all prompts in the Prompt Library
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, '.')

from notion_api_client import NotionTemplateClient
from tools import query_notion_database

print("="*70)
print("  🚀 Populating Prompt Library with Detailed Properties")
print("="*70)

# Initialize client
api_key = os.getenv('NOTION_API_KEY')
parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
PROMPT_LIBRARY_ID = "2830da0a-a5c8-8105-adab-e20090bb6046"

client = NotionTemplateClient(api_key=api_key)

# Get all prompts from the database
print("\n📋 Retrieving existing prompts...")
try:
    # Use client directly to avoid the sorts parameter issue
    prompt_pages = client.query_database(database_id=PROMPT_LIBRARY_ID)
    print(f"✅ Found {len(prompt_pages)} prompts to update")
        
except Exception as e:
    print(f"❌ Error retrieving prompts: {str(e)}")
    sys.exit(1)

# Define comprehensive prompt data
prompt_data = {
    "The LinkedIn Hook Generator": {
        "category": "Hook Generator",
        "template": "Write a LinkedIn post that starts with one of these hooks:\n\n• \"Here's what I wish I knew before...\"\n• \"The biggest mistake I see [audience] making...\"\n• \"After [X years] in [industry], here's what I learned...\"\n• \"This changed everything for me...\"\n\nTopic: [Your topic]\nAudience: [Your target audience]\nTone: [Professional/Conversational/Authoritative]",
        "use_case": "Perfect for grabbing attention in the first line and encouraging people to read your full post. Use when you want to share insights or lessons learned.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Comment Magnet": {
        "category": "Hook Generator", 
        "template": "Create a LinkedIn post that ends with a question designed to generate comments:\n\n• \"What's your experience with [topic]?\"\n• \"Have you tried [method]? What worked for you?\"\n• \"What would you add to this list?\"\n• \"What's your biggest challenge with [topic]?\"\n\nPost content: [Your main content]\nQuestion: [Your specific question]\nCall to action: [What you want people to do]",
        "use_case": "Use when you want to drive engagement and start conversations in the comments. Great for building community and gathering insights.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Question Cascade": {
        "category": "Hook Generator",
        "template": "Write a LinkedIn post that uses a series of questions to build engagement:\n\nOpening question: \"What if I told you [controversial statement]?\"\nFollow-up questions:\n• \"How would that change your approach to [topic]?\"\n• \"What would you do differently?\"\n• \"What's holding you back from trying this?\"\n\nConclusion: [Your insight or recommendation]",
        "use_case": "Ideal for thought leadership posts and challenging conventional thinking. Creates curiosity and encourages interaction.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Value-First Story Framework": {
        "category": "Story Prompts",
        "template": "Structure your LinkedIn post using this story framework:\n\n1. Setup: \"When I first started [situation]...\"\n2. Challenge: \"But then [obstacle/problem] happened...\"\n3. Action: \"So I decided to [what you did]...\"\n4. Result: \"Here's what happened...\"\n5. Lesson: \"The key takeaway is...\"\n\nStory topic: [Your story]\nKey lesson: [Main insight]\nActionable tip: [What readers can do]",
        "use_case": "Perfect for sharing personal experiences, case studies, and lessons learned. Creates emotional connection while delivering value.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Controversy Navigator": {
        "category": "Story Prompts",
        "template": "Write a LinkedIn post that addresses a controversial topic in your industry:\n\nOpening: \"Unpopular opinion: [controversial statement]\"\nSupporting evidence:\n• \"Here's why I believe this...\"\n• \"The data shows...\"\n• \"My experience has been...\"\n\nBalanced perspective: \"Of course, there are exceptions...\"\nCall for discussion: \"What's your take?\"",
        "use_case": "Great for thought leadership and sparking meaningful discussions. Use when you have a strong, well-reasoned position on a hot topic.",
        "effectiveness": "⭐⭐ Medium"
    },
    "The Industry Insight Generator": {
        "category": "Story Prompts",
        "template": "Share an industry insight using this structure:\n\nObservation: \"I've noticed a trend in [industry]...\"\nAnalysis: \"Here's what I think it means...\"\nImplications: \"This could impact [specific outcomes]...\"\nRecommendation: \"Here's what [audience] should do...\"\n\nTopic: [Your insight]\nIndustry: [Your industry]\nAudience: [Who should care]",
        "use_case": "Ideal for positioning yourself as an industry expert. Use when you've identified patterns or trends others might miss.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Behind-the-Scenes Revealer": {
        "category": "Story Prompts",
        "template": "Create a LinkedIn post that shows the real work behind success:\n\nReality check: \"Here's what [success] actually looks like...\"\nBehind the scenes: \"Most people don't see...\"\n• The failures\n• The long hours\n• The setbacks\n• The learning curve\n\nHonest reflection: \"The truth is...\"\nEncouragement: \"If you're in the messy middle...\"",
        "use_case": "Perfect for humanizing your brand and connecting with people who are struggling. Great for building trust and relatability.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Trend Analyzer": {
        "category": "Story Prompts",
        "template": "Analyze a current trend in your industry:\n\nTrend identification: \"Everyone's talking about [trend]...\"\nYour take: \"Here's what I think people are missing...\"\nPros and cons:\n• \"The good: [benefits]\"\n• \"The concerning: [potential issues]\"\n\nPrediction: \"I predict that in [timeframe]...\"\nAdvice: \"My recommendation for [audience]...\"",
        "use_case": "Excellent for thought leadership and showing your analytical skills. Use when you want to add depth to trending conversations.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Success Story Architect": {
        "category": "Story Prompts",
        "template": "Share a success story using this framework:\n\nContext: \"Last [timeframe], I was [situation]...\"\nGoal: \"I wanted to [objective]...\"\nStrategy: \"So I decided to [approach]...\"\nExecution: \"Here's what I did...\"\n• Step 1: [action]\n• Step 2: [action]\n• Step 3: [action]\n\nResults: \"The outcome was...\"\nLessons: \"What I learned...\"",
        "use_case": "Perfect for showcasing achievements and methodologies. Great for building credibility and teaching others your approach.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Data Storyteller": {
        "category": "Story Prompts",
        "template": "Tell a story using data and statistics:\n\nData point: \"[Statistic] of [audience] experience [situation]...\"\nPersonal connection: \"I was part of that [percentage]...\"\nAnalysis: \"Here's what this data reveals...\"\nImplications: \"This means [consequences]...\"\nAction items: \"Here's what we can do about it...\"",
        "use_case": "Ideal for data-driven professionals and researchers. Use when you have compelling statistics that tell a meaningful story.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Vulnerability Balance": {
        "category": "Story Prompts",
        "template": "Share a vulnerable moment while maintaining professionalism:\n\nSituation: \"Last week, I [vulnerable situation]...\"\nFeelings: \"I felt [emotions]...\"\nLearning: \"But then I realized...\"\nGrowth: \"This taught me...\"\nApplication: \"Now I [changed behavior]...\"\n\nKey message: \"The lesson here is...\"",
        "use_case": "Great for building authentic connections and showing growth. Use when you want to be relatable without oversharing.",
        "effectiveness": "⭐⭐ Medium"
    },
    "The Industry Prediction Post": {
        "category": "Story Prompts",
        "template": "Make a prediction about your industry's future:\n\nCurrent state: \"Right now, [industry] is [description]...\"\nTrends I'm seeing: \"But I'm noticing [patterns]...\"\nPrediction: \"I predict that by [date]...\"\nEvidence: \"Here's why I think this...\"\nImplications: \"This means [consequences]...\"\nAdvice: \"For [audience], I recommend...\"",
        "use_case": "Perfect for thought leadership and future-focused content. Use when you have insights about where your industry is heading.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Mistake-to-Lesson Transformer": {
        "category": "Story Prompts",
        "template": "Transform a mistake into a valuable lesson:\n\nMistake: \"I made a big mistake when I [action]...\"\nConsequences: \"This led to [outcome]...\"\nReflection: \"Looking back, I realize...\"\nLesson learned: \"The key lesson is...\"\nPrevention: \"To avoid this, [advice]...\"\n\nApplication: \"Now I always [changed behavior]...\"",
        "use_case": "Excellent for showing growth mindset and helping others avoid similar mistakes. Great for building trust through honesty.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Industry Change Commentator": {
        "category": "Story Prompts",
        "template": "Comment on significant industry changes:\n\nChange: \"[Industry] is changing rapidly...\"\nWhat's different: \"Gone are the days when [old way]...\"\nNew reality: \"Now [current situation]...\"\nImpact: \"This affects [stakeholders] because...\"\nAdaptation: \"To succeed, [audience] need to...\"\n\nOpportunity: \"But this also creates [opportunities]...\"",
        "use_case": "Ideal for industry veterans and change management experts. Use when you want to help others navigate industry shifts.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Personal Brand Story": {
        "category": "Story Prompts",
        "template": "Share your personal brand journey:\n\nOrigin story: \"I didn't always [current expertise]...\"\nTurning point: \"Everything changed when [moment]...\"\nJourney: \"Since then, I've [growth/development]...\"\nCurrent focus: \"Now I [current work]...\"\nMission: \"My goal is to [purpose]...\"\n\nInvitation: \"If this resonates, let's connect...\"",
        "use_case": "Perfect for personal branding and networking. Use when you want to introduce yourself or pivot your professional image.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Carousel Content Creator": {
        "category": "List Posts",
        "template": "Create a LinkedIn carousel post with this structure:\n\nTitle: \"[Number] [Topic] That [Benefit]\"\n\nSlide 1: Hook - \"Here's what most people get wrong about [topic]...\"\nSlide 2-6: Main points - Each slide covers one key point\nSlide 7: Call to action - \"Which point resonates most with you?\"\n\nTopics to cover:\n• [Point 1]\n• [Point 2]\n• [Point 3]\n• [Point 4]\n• [Point 5]",
        "use_case": "Perfect for educational content and how-to guides. Great for driving traffic to your profile and generating saves.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Resource Roundup": {
        "category": "List Posts",
        "template": "Create a resource list post:\n\nIntroduction: \"I've been asked about [topic] resources...\"\n\nHere are my top [number] recommendations:\n\n1. [Resource] - [Why it's valuable]\n2. [Resource] - [Why it's valuable]\n3. [Resource] - [Why it's valuable]\n4. [Resource] - [Why it's valuable]\n5. [Resource] - [Why it's valuable]\n\nBonus: [Additional tip or resource]\n\nQuestion: \"What would you add to this list?\"",
        "use_case": "Excellent for building authority and helping your audience. Great for engagement and establishing yourself as a helpful resource.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Tool Recommendation Engine": {
        "category": "How-To Posts",
        "template": "Recommend tools or resources:\n\nProblem: \"If you're struggling with [problem]...\"\nSolution: \"Here's the tool I use: [tool name]\"\n\nWhy I love it:\n• [Benefit 1]\n• [Benefit 2]\n• [Benefit 3]\n\nHow to use it:\n• Step 1: [action]\n• Step 2: [action]\n• Step 3: [action]\n\nResult: \"This has [positive outcome]...\"\n\nQuestion: \"What tools do you use for [topic]?\"",
        "use_case": "Perfect for product recommendations and sharing practical solutions. Great for building trust and providing immediate value.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Industry Myth Buster": {
        "category": "How-To Posts",
        "template": "Debunk a common industry myth:\n\nMyth: \"Everyone says [common belief]...\"\nReality: \"But here's what actually happens...\"\n\nWhy this myth persists:\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\nWhat to do instead:\n• [Alternative approach 1]\n• [Alternative approach 2]\n• [Alternative approach 3]\n\nResult: \"When you [correct approach], you get [better outcome]...\"",
        "use_case": "Excellent for thought leadership and challenging conventional wisdom. Use when you have evidence that contradicts popular beliefs.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Process Breakdown": {
        "category": "How-To Posts",
        "template": "Break down a complex process:\n\nIntroduction: \"Here's how I [achieve result]...\"\n\nStep-by-step process:\n\nStep 1: [Action] - \"This is crucial because...\"\nStep 2: [Action] - \"Many people skip this, but...\"\nStep 3: [Action] - \"Here's the secret...\"\nStep 4: [Action] - \"This is where most people fail...\"\nStep 5: [Action] - \"Finally...\"\n\nPro tip: \"The key is [insight]...\"\n\nQuestion: \"Which step do you find most challenging?\"",
        "use_case": "Perfect for educational content and sharing methodologies. Great for building authority in your field.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Audience Question Answerer": {
        "category": "How-To Posts",
        "template": "Answer a common audience question:\n\nQuestion: \"I often get asked: '[common question]'\"\n\nShort answer: \"The answer is [brief response]...\"\n\nDetailed explanation:\n• \"Here's why...\"\n• \"What this means is...\"\n• \"The key factors are...\"\n\nPractical application: \"To implement this...\"\n• [Action 1]\n• [Action 2]\n• [Action 3]\n\nResult: \"When you do this, you'll [benefit]...\"",
        "use_case": "Great for addressing FAQs and providing value. Use when you want to help your audience solve common problems.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Industry Insider Tip": {
        "category": "How-To Posts",
        "template": "Share an insider tip:\n\nSetup: \"After [experience] in [industry], here's a tip most people don't know...\"\n\nThe tip: \"[Insider knowledge/technique]\"\n\nWhy it works:\n• \"Most people think [common belief]...\"\n• \"But actually [reality]...\"\n• \"This happens because [explanation]...\"\n\nHow to use it:\n• \"First, [action]...\"\n• \"Then, [action]...\"\n• \"Finally, [action]...\"\n\nResult: \"This will [positive outcome]...\"",
        "use_case": "Perfect for sharing exclusive knowledge and positioning yourself as an insider. Great for building credibility.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Quick Win Sharer": {
        "category": "How-To Posts",
        "template": "Share a quick win or easy tip:\n\nIntroduction: \"Want a quick win for [goal]?\"\n\nThe tip: \"Here's something you can do in [timeframe]...\"\n\nStep-by-step:\n1. [Simple action]\n2. [Simple action]\n3. [Simple action]\n\nWhy it works: \"This is effective because...\"\n\nExpected result: \"You should see [outcome] within [timeframe]...\"\n\nBonus tip: \"Pro tip: [additional insight]...\"",
        "use_case": "Great for providing immediate value and actionable content. Perfect for building engagement with practical tips.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Challenge Issuer": {
        "category": "Engagement Hooks",
        "template": "Issue a challenge to your audience:\n\nSetup: \"I challenge you to [action]...\"\n\nWhy this matters: \"Here's why this challenge is important...\"\n\nRules:\n• \"You have [timeframe] to complete it\"\n• \"The goal is [objective]\"\n• \"Here's how to measure success: [criteria]\"\n\nSupport: \"I'll be sharing tips and encouragement...\"\n\nCall to action: \"Are you in? Comment 'I accept' to join the challenge!\"",
        "use_case": "Excellent for building community and driving engagement. Great for creating accountability and interaction.",
        "effectiveness": "⭐⭐ Medium"
    },
    "The Networking Connection Builder": {
        "category": "Engagement Hooks",
        "template": "Create a networking-focused post:\n\nOpening: \"Looking to connect with [type of people]...\"\n\nYour background: \"I'm [your role/background]...\"\n\nWhat you offer: \"I can help with [your expertise/services]...\"\n\nWhat you're seeking: \"I'm looking for [what you need]...\"\n\nConnection call: \"If this sounds like you, let's connect!\"\n\nSpecific ask: \"Comment below if you [specific criteria]...\"",
        "use_case": "Perfect for networking and building professional relationships. Great for finding mutually beneficial connections.",
        "effectiveness": "⭐⭐ Medium"
    },
    "The Failure-to-Success Transformer": {
        "category": "Engagement Hooks",
        "template": "Transform a failure into a success story:\n\nFailure: \"I failed at [attempt]...\"\n\nWhat went wrong: \"Here's what happened...\"\n• [Mistake 1]\n• [Mistake 2]\n• [Mistake 3]\n\nLearning: \"But I learned [lessons]...\"\n\nNew approach: \"So I tried [different strategy]...\"\n\nSuccess: \"This time, [positive outcome]...\"\n\nQuestion: \"What's a failure that taught you the most?\"",
        "use_case": "Great for building resilience and encouraging others. Perfect for showing growth mindset and vulnerability.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Industry Comparison": {
        "category": "Contrarian Takes",
        "template": "Compare different approaches in your industry:\n\nCommon approach: \"Most people in [industry] do [method A]...\"\n\nAlternative approach: \"But I've found [method B] works better...\"\n\nComparison:\n• \"Method A: [pros and cons]\"\n• \"Method B: [pros and cons]\"\n\nEvidence: \"Here's why I prefer [method B]...\"\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\nQuestion: \"Which approach has worked better for you?\"",
        "use_case": "Perfect for thought leadership and sparking discussion. Great for sharing alternative perspectives.",
        "effectiveness": "⭐⭐ Medium"
    },
    "The Industry Future Vision": {
        "category": "Contrarian Takes",
        "template": "Share your vision for the industry's future:\n\nCurrent state: \"Everyone thinks [industry] will [common prediction]...\"\n\nYour prediction: \"But I think it will actually [different outcome]...\"\n\nWhy this matters: \"Here's why this distinction is crucial...\"\n\nEvidence: \"The signs I'm seeing...\"\n• [Trend 1]\n• [Trend 2]\n• [Trend 3]\n\nImplications: \"This means [consequences]...\"\n\nAdvice: \"For [audience], I recommend [action]...\"",
        "use_case": "Excellent for thought leadership and future planning. Great for positioning yourself as a forward-thinker.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Industry Trend Predictor": {
        "category": "Contrarian Takes",
        "template": "Predict a trend that others aren't seeing:\n\nObservation: \"While everyone focuses on [popular trend]...\"\n\nHidden trend: \"I'm noticing [emerging pattern]...\"\n\nWhy it's significant: \"This matters because...\"\n\nEarly indicators: \"The signs I'm seeing...\"\n• [Indicator 1]\n• [Indicator 2]\n• [Indicator 3]\n\nTimeline: \"I predict this will [happen] by [date]...\"\n\nOpportunity: \"Early adopters can [benefit]...\"",
        "use_case": "Perfect for trend analysis and early insight sharing. Great for establishing yourself as a trend spotter.",
        "effectiveness": "⭐⭐⭐ High"
    },
    "The Productivity Hack Sharer": {
        "category": "Contrarian Takes",
        "template": "Share a productivity counter-intuitive hack:\n\nCommon advice: \"Everyone says to [common productivity tip]...\"\n\nContrarian approach: \"But I actually [different approach]...\"\n\nWhy it works: \"Here's why this is more effective...\"\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\nHow to implement: \"To try this...\"\n• [Step 1]\n• [Step 2]\n• [Step 3]\n\nResult: \"This has [positive outcome] for me...\"",
        "use_case": "Great for sharing unique approaches and challenging conventional wisdom. Perfect for productivity content.",
        "effectiveness": "⭐⭐ Medium"
    }
}

# Update each prompt with detailed properties
print(f"\n🔄 Updating {len(prompt_pages)} prompts with detailed properties...")
print("-" * 70)

updated_count = 0
failed_count = 0

for page in prompt_pages:
    page_id = page["id"]
    prompt_name = ""
    
    # Get the prompt name from the title property
    title_prop = page["properties"].get("Prompt Name", {})
    if title_prop and "title" in title_prop and len(title_prop["title"]) > 0:
        prompt_name = title_prop["title"][0]["plain_text"]
    
    if prompt_name in prompt_data:
        data = prompt_data[prompt_name]
        
        try:
            # Update the page with existing properties only
            client.client.pages.update(
                page_id=page_id,
                properties={
                    "Category": {
                        "select": {"name": data["category"]}
                    },
                    "Use Case": {
                        "rich_text": [
                            {
                                "type": "text", 
                                "text": {"content": data["use_case"]}
                            }
                        ]
                    }
                }
            )
            print(f"✅ Updated: {prompt_name}")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Failed to update {prompt_name}: {str(e)}")
            failed_count += 1
    else:
        print(f"⚠️  No data found for: {prompt_name}")
        failed_count += 1

print("\n" + "="*70)
print(f"  📊 UPDATE COMPLETE!")
print("="*70)
print(f"✅ Successfully updated: {updated_count} prompts")
print(f"❌ Failed updates: {failed_count} prompts")
print(f"📋 Total prompts processed: {len(prompt_pages)}")

if updated_count > 0:
    print(f"\n🎉 Your Prompt Library now has complete information for {updated_count} prompts!")
    print("📝 Each prompt now includes:")
    print("   • Category classification")
    print("   • Specific use case guidance")
    
    print(f"\n🔗 View your updated Prompt Library:")
    print(f"   https://www.notion.so/{PROMPT_LIBRARY_ID.replace('-', '')}")
    
    print(f"\n🚀 Ready to create amazing LinkedIn content!")

else:
    print(f"\n⚠️  No prompts were updated. Please check the error messages above.")

print("="*70)
