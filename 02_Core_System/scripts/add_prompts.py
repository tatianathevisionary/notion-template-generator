#!/usr/bin/env python3
"""
Add detailed prompt templates as rich text content to each prompt page
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, '.')

from notion_api_client import NotionTemplateClient
from tools import update_notion_page

print("="*70)
print("  🚀 Adding Detailed Prompt Templates to Prompt Pages")
print("="*70)

# Initialize client
api_key = os.getenv('NOTION_API_KEY')
PROMPT_LIBRARY_ID = "2830da0a-a5c8-8105-adab-e20090bb6046"

client = NotionTemplateClient(api_key=api_key)

# Get all prompts from the database
print("\n📋 Retrieving existing prompts...")
try:
    prompt_pages = client.query_database(database_id=PROMPT_LIBRARY_ID)
    print(f"✅ Found {len(prompt_pages)} prompts to update")
        
except Exception as e:
    print(f"❌ Error retrieving prompts: {str(e)}")
    sys.exit(1)

# Define comprehensive prompt templates (same as before)
prompt_templates = {
    "The LinkedIn Hook Generator": """# 🎣 The LinkedIn Hook Generator

## Template Structure:
Write a LinkedIn post that starts with one of these hooks:

• "Here's what I wish I knew before..."
• "The biggest mistake I see [audience] making..."
• "After [X years] in [industry], here's what I learned..."
• "This changed everything for me..."

## How to Use:
1. **Topic**: [Your specific topic]
2. **Audience**: [Your target audience]
3. **Tone**: [Professional/Conversational/Authoritative]

## Example:
"Here's what I wish I knew before starting my first startup: most successful entrepreneurs don't just have great ideas—they have great systems for validating those ideas quickly and cheaply."

**Effectiveness**: ⭐⭐⭐ High - Perfect for grabbing attention and encouraging people to read your full post.""",

    "The Comment Magnet": """# 💬 The Comment Magnet

## Template Structure:
Create a LinkedIn post that ends with a question designed to generate comments:

• "What's your experience with [topic]?"
• "Have you tried [method]? What worked for you?"
• "What would you add to this list?"
• "What's your biggest challenge with [topic]?"

## How to Use:
1. **Post content**: [Your main content]
2. **Question**: [Your specific question]
3. **Call to action**: [What you want people to do]

## Example:
"After 5 years in marketing, I've learned that the best campaigns aren't about selling—they're about solving real problems. What's the most effective marketing strategy you've used that actually solved a customer problem?"

**Effectiveness**: ⭐⭐⭐ High - Drives engagement and starts conversations.""",

    "The Value-First Story Framework": """# 📖 The Value-First Story Framework

## Template Structure:
1. **Setup**: "When I first started [situation]..."
2. **Challenge**: "But then [obstacle/problem] happened..."
3. **Action**: "So I decided to [what you did]..."
4. **Result**: "Here's what happened..."
5. **Lesson**: "The key takeaway is..."

## How to Use:
1. **Story topic**: [Your specific story]
2. **Key lesson**: [Main insight you want to share]
3. **Actionable tip**: [What readers can do]

## Example:
"When I first started my consulting business, I thought I needed to be everything to everyone. But then I realized I was spreading myself too thin and not delivering real value. So I decided to focus on just one niche. Here's what happened: my revenue tripled and my clients became raving fans. The key takeaway is: depth beats breadth every time."

**Effectiveness**: ⭐⭐⭐ High - Creates emotional connection while delivering value.""",

    "The Industry Insight Generator": """# 🔍 The Industry Insight Generator

## Template Structure:
1. **Observation**: "I've noticed a trend in [industry]..."
2. **Analysis**: "Here's what I think it means..."
3. **Implications**: "This could impact [specific outcomes]..."
4. **Recommendation**: "Here's what [audience] should do..."

## How to Use:
1. **Topic**: [Your specific insight]
2. **Industry**: [Your industry]
3. **Audience**: [Who should care about this]

## Example:
"I've noticed a trend in SaaS: companies are moving away from feature-heavy platforms toward simple, focused solutions. Here's what I think it means: customers are overwhelmed by complexity and just want tools that solve one problem really well. This could impact enterprise software sales dramatically. For B2B companies, I recommend focusing on core functionality and removing everything else."

**Effectiveness**: ⭐⭐⭐ High - Positions you as an industry expert.""",

    "The Behind-the-Scenes Revealer": """# 🎬 The Behind-the-Scenes Revealer

## Template Structure:
1. **Reality check**: "Here's what [success] actually looks like..."
2. **Behind the scenes**: "Most people don't see..."
   • The failures
   • The long hours
   • The setbacks
   • The learning curve
3. **Honest reflection**: "The truth is..."
4. **Encouragement**: "If you're in the messy middle..."

## How to Use:
1. **Success story**: [What you achieved]
2. **Hidden struggles**: [What people don't see]
3. **Encouraging message**: [What you want to tell others]

## Example:
"Here's what building a successful startup actually looks like: 18-hour days, constant rejection, and more failures than wins. Most people don't see the 47 investor meetings that led to 'no,' the nights I questioned everything, or the pivot that almost killed us. The truth is: success is messy, uncertain, and requires more resilience than talent. If you're in the messy middle, keep going—you're exactly where you need to be."

**Effectiveness**: ⭐⭐⭐ High - Humanizes your brand and builds trust.""",

    "The Carousel Content Creator": """# 🎠 The Carousel Content Creator

## Template Structure:
**Title**: "[Number] [Topic] That [Benefit]"

**Slide 1**: Hook - "Here's what most people get wrong about [topic]..."
**Slide 2-6**: Main points - Each slide covers one key point
**Slide 7**: Call to action - "Which point resonates most with you?"

## How to Use:
1. **Topic**: [Your main subject]
2. **Number**: [How many points you'll cover]
3. **Benefit**: [What readers will gain]

## Example:
"5 LinkedIn Mistakes That Kill Your Engagement"

Slide 1: "Here's what most people get wrong about LinkedIn: they treat it like Facebook."
Slide 2: "Mistake #1: Posting only about yourself"
Slide 3: "Mistake #2: Ignoring comments on your posts"
Slide 4: "Mistake #3: Using generic connection requests"
Slide 5: "Mistake #4: Not engaging with others' content"
Slide 6: "Mistake #5: Focusing on followers instead of connections"
Slide 7: "Which mistake are you most guilty of? Comment below!"

**Effectiveness**: ⭐⭐⭐ High - Perfect for educational content and drives saves.""",

    "The Tool Recommendation Engine": """# 🛠️ The Tool Recommendation Engine

## Template Structure:
1. **Problem**: "If you're struggling with [problem]..."
2. **Solution**: "Here's the tool I use: [tool name]"
3. **Why I love it**:
   • [Benefit 1]
   • [Benefit 2]
   • [Benefit 3]
4. **How to use it**:
   • Step 1: [action]
   • Step 2: [action]
   • Step 3: [action]
5. **Result**: "This has [positive outcome]..."
6. **Question**: "What tools do you use for [topic]?"

## How to Use:
1. **Problem**: [Common pain point]
2. **Tool**: [Specific tool/technique]
3. **Steps**: [How to implement]

## Example:
"If you're struggling with time management, here's the tool I use: the 2-minute rule. If a task takes less than 2 minutes, do it immediately. If it takes longer, schedule it. Why I love it: it prevents small tasks from piling up, keeps my inbox clean, and reduces mental overhead. This has helped me save 2+ hours per day. What tools do you use for productivity?"

**Effectiveness**: ⭐⭐⭐ High - Provides immediate value and builds trust.""",

    "The Industry Myth Buster": """# 🚫 The Industry Myth Buster

## Template Structure:
1. **Myth**: "Everyone says [common belief]..."
2. **Reality**: "But here's what actually happens..."
3. **Why this myth persists**:
   • [Reason 1]
   • [Reason 2]
   • [Reason 3]
4. **What to do instead**:
   • [Alternative approach 1]
   • [Alternative approach 2]
   • [Alternative approach 3]
5. **Result**: "When you [correct approach], you get [better outcome]..."

## How to Use:
1. **Myth**: [Common industry belief]
2. **Evidence**: [Why it's wrong]
3. **Better approach**: [What actually works]

## Example:
"Everyone says you need 10,000 hours to master a skill. But here's what actually happens: most people plateau after 20-50 hours of deliberate practice. Why this myth persists: it sounds impressive, it excuses inaction, and it makes expertise seem unattainable. What to do instead: focus on the 20% of skills that drive 80% of results, practice with feedback loops, and apply immediately. When you focus on high-impact skills with immediate application, you get results in weeks, not years."

**Effectiveness**: ⭐⭐⭐ High - Challenges conventional wisdom with evidence.""",

    "The Challenge Issuer": """# 🎯 The Challenge Issuer

## Template Structure:
1. **Setup**: "I challenge you to [action]..."
2. **Why this matters**: "Here's why this challenge is important..."
3. **Rules**:
   • "You have [timeframe] to complete it"
   • "The goal is [objective]"
   • "Here's how to measure success: [criteria]"
4. **Support**: "I'll be sharing tips and encouragement..."
5. **Call to action**: "Are you in? Comment 'I accept' to join the challenge!"

## How to Use:
1. **Challenge**: [Specific action you want people to take]
2. **Timeframe**: [How long they have]
3. **Support**: [How you'll help them]

## Example:
"I challenge you to post one piece of valuable content every day for the next 30 days. Here's why this challenge is important: consistent content creation builds your personal brand, establishes your expertise, and creates opportunities you never expected. Rules: You have 30 days, the goal is to provide value (not self-promotion), measure success by engagement and connections made. I'll be sharing daily tips and encouragement. Are you in? Comment 'I accept' to join the challenge!"

**Effectiveness**: ⭐⭐ Medium - Great for building community and engagement.""",

    "The Networking Connection Builder": """# 🤝 The Networking Connection Builder

## Template Structure:
1. **Opening**: "Looking to connect with [type of people]..."
2. **Your background**: "I'm [your role/background]..."
3. **What you offer**: "I can help with [your expertise/services]..."
4. **What you're seeking**: "I'm looking for [what you need]..."
5. **Connection call**: "If this sounds like you, let's connect!"
6. **Specific ask**: "Comment below if you [specific criteria]..."

## How to Use:
1. **Your value**: [What you can offer others]
2. **Your needs**: [What you're looking for]
3. **Target audience**: [Who you want to connect with]

## Example:
"Looking to connect with other startup founders who are scaling their teams. I'm a startup CEO who's grown from 2 to 50 employees in 18 months. I can help with hiring strategies, culture building, and scaling operations. I'm looking for founders who've successfully scaled through the 10-50 employee phase. If this sounds like you, let's connect! Comment below if you've scaled a team through this phase—I'd love to learn from your experience."

**Effectiveness**: ⭐⭐ Medium - Perfect for networking and building relationships.""",

    "The Failure-to-Success Transformer": """# 🔄 The Failure-to-Success Transformer

## Template Structure:
1. **Failure**: "I failed at [attempt]..."
2. **What went wrong**:
   • [Mistake 1]
   • [Mistake 2]
   • [Mistake 3]
3. **Learning**: "But I learned [lessons]..."
4. **New approach**: "So I tried [different strategy]..."
5. **Success**: "This time, [positive outcome]..."
6. **Question**: "What's a failure that taught you the most?"

## How to Use:
1. **Failure**: [Specific failure you experienced]
2. **Lessons**: [What you learned]
3. **Success**: [How you applied the lessons]

## Example:
"I failed at my first product launch—terribly. What went wrong: I built in isolation without customer feedback, I assumed people wanted what I wanted, and I launched to everyone instead of a specific niche. But I learned that validation beats assumptions every time. So I tried customer interviews, built an MVP, and tested with a small group first. This time, we hit 80% of our launch goals in the first month. What's a failure that taught you the most?"

**Effectiveness**: ⭐⭐⭐ High - Shows growth mindset and encourages others.""",

    "The Industry Comparison": """# ⚖️ The Industry Comparison

## Template Structure:
1. **Common approach**: "Most people in [industry] do [method A]..."
2. **Alternative approach**: "But I've found [method B] works better..."
3. **Comparison**:
   • "Method A: [pros and cons]"
   • "Method B: [pros and cons]"
4. **Evidence**: "Here's why I prefer [method B]..."
   • [Reason 1]
   • [Reason 2]
   • [Reason 3]
5. **Question**: "Which approach has worked better for you?"

## How to Use:
1. **Method A**: [Common industry practice]
2. **Method B**: [Your preferred approach]
3. **Evidence**: [Why your approach works better]

## Example:
"Most people in marketing do broad targeting to reach more people. But I've found narrow targeting works better. Method A: Broad targeting—reaches many people but low engagement and conversion. Method B: Narrow targeting—reaches fewer people but high engagement and conversion. Here's why I prefer narrow targeting: higher quality leads, better customer relationships, and more sustainable growth. Which approach has worked better for you?"

**Effectiveness**: ⭐⭐ Medium - Great for thought leadership and discussion.""",

    "The Industry Future Vision": """# 🔮 The Industry Future Vision

## Template Structure:
1. **Current state**: "Everyone thinks [industry] will [common prediction]..."
2. **Your prediction**: "But I think it will actually [different outcome]..."
3. **Why this matters**: "Here's why this distinction is crucial..."
4. **Evidence**: "The signs I'm seeing..."
   • [Trend 1]
   • [Trend 2]
   • [Trend 3]
5. **Implications**: "This means [consequences]..."
6. **Advice**: "For [audience], I recommend [action]..."

## How to Use:
1. **Common prediction**: [What most people think will happen]
2. **Your prediction**: [What you think will actually happen]
3. **Evidence**: [Signs that support your view]

## Example:
"Everyone thinks AI will replace human workers. But I think it will actually make human creativity more valuable. Here's why this distinction is crucial: if you prepare for replacement, you'll compete with machines. If you prepare for augmentation, you'll work alongside them. The signs I'm seeing: AI excels at pattern recognition, humans excel at creative problem-solving; companies are investing in human-AI collaboration tools; creative roles are growing faster than technical ones. This means the future belongs to those who can think creatively with AI as their tool. For professionals, I recommend developing creative skills that complement AI capabilities."

**Effectiveness**: ⭐⭐⭐ High - Positions you as a forward-thinker.""",

    "The Productivity Hack Sharer": """# ⚡ The Productivity Hack Sharer

## Template Structure:
1. **Common advice**: "Everyone says to [common productivity tip]..."
2. **Contrarian approach**: "But I actually [different approach]..."
3. **Why it works**: "Here's why this is more effective..."
   • [Reason 1]
   • [Reason 2]
   • [Reason 3]
4. **How to implement**: "To try this..."
   • [Step 1]
   • [Step 2]
   • [Step 3]
5. **Result**: "This has [positive outcome] for me..."

## How to Use:
1. **Common tip**: [What most people recommend]
2. **Your approach**: [What you actually do]
3. **Evidence**: [Why your way works better]

## Example:
"Everyone says to wake up at 5 AM for maximum productivity. But I actually wake up at 7 AM and work in 90-minute focused blocks. Here's why this is more effective: I'm naturally alert at 7 AM, 90-minute blocks match natural attention cycles, and I avoid the exhaustion of forcing early mornings. To try this: find your natural peak hours, set 90-minute timers, eliminate distractions during blocks, and take 20-minute breaks between sessions. This has increased my daily output by 40% while reducing stress."

**Effectiveness**: ⭐⭐ Medium - Shares unique approaches and challenges conventional wisdom."""
}

# Update each prompt with detailed template content
print(f"\n🔄 Adding detailed templates to {len(prompt_pages)} prompts...")
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
    
    if prompt_name in prompt_templates:
        template_content = prompt_templates[prompt_name]
        
        try:
            # Add the template as content blocks to the page
            content = {
                "children": [
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": template_content}
                                }
                            ]
                        }
                    }
                ]
            }
            
            result = update_notion_page(
                page_id=page_id,
                content=content,
                api_key=api_key
            )
            
            if result.get("status") == "success":
                print(f"✅ Added template to: {prompt_name}")
                updated_count += 1
            else:
                print(f"❌ Failed to add template to {prompt_name}: {result.get('error')}")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Failed to add template to {prompt_name}: {str(e)}")
            failed_count += 1
    else:
        print(f"⚠️  No template found for: {prompt_name}")
        failed_count += 1

print("\n" + "="*70)
print(f"  📊 TEMPLATE ADDITION COMPLETE!")
print("="*70)
print(f"✅ Successfully added templates to: {updated_count} prompts")
print(f"❌ Failed additions: {failed_count} prompts")
print(f"📋 Total prompts processed: {len(prompt_pages)}")

if updated_count > 0:
    print(f"\n🎉 Your Prompt Library now has detailed templates for {updated_count} prompts!")
    print("📝 Each prompt now includes:")
    print("   • Category classification")
    print("   • Specific use case guidance")
    print("   • Detailed prompt template with examples")
    print("   • Step-by-step instructions")
    print("   • Effectiveness ratings")
    
    print(f"\n🔗 View your complete Prompt Library:")
    print(f"   https://www.notion.so/{PROMPT_LIBRARY_ID.replace('-', '')}")
    
    print(f"\n🚀 Your LinkedIn Content OS is now fully equipped!")

else:
    print(f"\n⚠️  No templates were added. Please check the error messages above.")

print("="*70)

