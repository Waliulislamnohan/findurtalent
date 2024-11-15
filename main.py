import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Inject Custom CSS
css = """
<style>
/* Background Gradient */
body {
    background: linear-gradient(to bottom, #2c3e50, #bdc3c7);
    color: white;
}

/* Header and Subheader Styling */
h1, h2, h3, h4, h5, h6 {
    color: white;
}

/* Radio Buttons and Selectbox Styling */
.stRadio > label > div > div > label > div {
    color: white;
}

.stSelectbox > label > div > div > div {
    color: white;
}

/* Button Styling */
.css-1q8dd3e.edgvbvh3 {
    background-color: #34495e;
    color: white;
    border: none;
}

.css-1q8dd3e.edgvbvh3:hover {
    background-color: #2c3e50;
}

/* Success Message Styling */
.css-1lsmgbg.egzxvld1 {
    background-color: rgba(52, 73, 94, 0.8);
    color: white;
    border-radius: 5px;
    padding: 10px;
}

/* Subheader Background */
.css-1a539bi.e1fqkh3o3 {
    background-color: rgba(44, 62, 80, 0.8);
    padding: 10px;
    border-radius: 5px;
}

/* Markdown Styling */
.css-1aumxhk.e16nr0p30 {
    color: white;
}

/* Input Widgets Styling */
.css-1fcbmhc.e16nr0p30 {
    background-color: rgba(44, 62, 80, 0.8);
    border: 1px solid #7f8c8d;
    border-radius: 5px;
}

/* Plotly Chart Background */
.css-1aumxhk.e16nr0p30 p {
    color: white;
}

.css-1aumxhk.e16nr0p30 a {
    color: #3498db;
}

/* Progress Bar Styling */
.css-1aumxhk.e16nr0p30 div[role="progressbar"] > div {
    background-color: #3498db;
}

/* Tooltip Styling */
div.tooltip {
    position: relative;
    display: inline-block;
}

div.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #34495e;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;

    /* Position the tooltip */
    position: absolute;
    z-index: 1;
}

div.tooltip:hover .tooltiptext {
    visibility: visible;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Function to map answer options to scores
def map_score(option):
    mapping = {
        "Option A": 1,
        "Option B": 5,
        "Option C": 10
    }
    return mapping.get(option, 0)

# Function to determine talent profile based on scores
def determine_profile(creativity, leadership, logic):
    scores = {
        "Creative": creativity,
        "Logical Wizard": logic,
        "Leader": leadership
    }
    # Find the category with the highest score
    max_category = max(scores, key=scores.get)
    return max_category

# Career suggestions based on talent profiles
career_suggestions = {
    "Creative": [
        {"title": "Graphic Designer", "description": "Design visual content for brands, advertisements, and products.", "link": "https://www.example.com/graphic-designer"},
        {"title": "Content Creator", "description": "Develop engaging content for various media platforms.", "link": "https://www.example.com/content-creator"},
        {"title": "Marketing Specialist", "description": "Plan and execute marketing campaigns to promote products or services.", "link": "https://www.example.com/marketing-specialist"},
        {"title": "Product Designer", "description": "Design and develop new products from concept to market.", "link": "https://www.example.com/product-designer"},
        {"title": "Art Director", "description": "Lead the visual aspects of creative projects and campaigns.", "link": "https://www.example.com/art-director"}
    ],
    "Logical Wizard": [
        {"title": "Software Developer", "description": "Develop and maintain software applications.", "link": "https://www.example.com/software-developer"},
        {"title": "Data Scientist", "description": "Analyze complex data to help make informed business decisions.", "link": "https://www.example.com/data-scientist"},
        {"title": "Systems Analyst", "description": "Evaluate and improve IT systems to meet organizational needs.", "link": "https://www.example.com/systems-analyst"},
        {"title": "Cybersecurity Analyst", "description": "Protect organizational data and systems from cyber threats.", "link": "https://www.example.com/cybersecurity-analyst"},
        {"title": "Database Administrator", "description": "Manage and maintain databases to ensure data integrity and security.", "link": "https://www.example.com/database-administrator"}
    ],
    "Leader": [
        {"title": "Project Manager", "description": "Oversee projects from inception to completion, ensuring timely delivery.", "link": "https://www.example.com/project-manager"},
        {"title": "Team Lead", "description": "Guide and support team members to achieve project goals.", "link": "https://www.example.com/team-lead"},
        {"title": "Operations Manager", "description": "Manage daily operations to ensure efficiency and effectiveness.", "link": "https://www.example.com/operations-manager"},
        {"title": "Product Manager", "description": "Lead product development and strategy to meet market demands.", "link": "https://www.example.com/product-manager"},
        {"title": "Human Resources Manager", "description": "Manage HR functions, including recruitment, training, and employee relations.", "link": "https://www.example.com/human-resources-manager"}
    ]
}

# Streamlit App
st.title("Talent Detector")
st.header("Please answer the following questions:")

# ---------------------
# Creativity Questions
# ---------------------
st.subheader("সৃজনশীলতা")

creativity_q1 = st.radio(
    "১. একটি নতুন প্রকল্পে কাজ শুরু করার সময়, আপনি সাধারণত কীভাবে পরিকল্পনা করেন?",
    ("Option A: পূর্বের অভিজ্ঞতার ওপর নির্ভর করে কাজ শুরু করি।",
     "Option B: বিভিন্ন উৎস থেকে অনুপ্রেরণা সংগ্রহ করে নতুন আইডিয়া তৈরি করি।",
     "Option C: টিমের সঙ্গে আলোচনা করে এবং যৌথভাবে পরিকল্পনা করি।"),
    help="আপনার পরিকল্পনার পদ্ধতি আপনার সৃজনশীলতার মাত্রা নির্ধারণ করে।"
)

creativity_q2 = st.radio(
    "২. যখন আপনি কোনো সৃজনশীল সমস্যার সম্মুখীন হন, তখন আপনি কীভাবে প্রতিক্রিয়া জানান?",
    ("Option A: সমস্যাটির সমাধান এড়িয়ে চলি।",
     "Option B: বিভিন্ন পদ্ধতি ব্যবহার করে সমস্যাটি সমাধানের চেষ্টা করি।",
     "Option C: সমস্যাটি দ্রুত সমাধানের জন্য সহকর্মীদের সাহায্য চাই।"),
    help="আপনি সমস্যার সমাধানে কতটা সৃজনশীল এবং উদ্ভাবনী।"
)

creativity_q3 = st.radio(
    "৩. টিম মিটিংয়ে আপনি কী ধরনের ভূমিকা পালন করেন?",
    ("Option A: শুধুমাত্র শুনি এবং নোট নেয়।",
     "Option B: মাঝে মাঝে কিছু ধারণা শেয়ার করি।",
     "Option C: সক্রিয়ভাবে নতুন আইডিয়া নিয়ে আসি এবং টিমকে উৎসাহিত করি।"),
    help="টিমের মধ্যে আপনার সৃজনশীল অবদান কেমন।"
)

# ---------------------
# Leadership Questions
# ---------------------
st.subheader("নেতৃত্ব")

leadership_q1 = st.radio(
    "১. যখন আপনার টিম বড় ধরনের সমস্যার সম্মুখীন হয়, তখন আপনি কীভাবে পরিচালনা করেন?",
    ("Option A: সমস্যাটির দায়িত্ব নির্দিষ্ট সদস্যদের ওপর চাপিয়ে দিই।",
     "Option B: ইতিবাচক মনোভাব রেখে টিমকে প্রেরণা জোগাই এবং সমাধানের পথ খুঁজে বের করি।",
     "Option C: নিজেকে সমস্যার বাইরে রেখে টিমকে নিজেরাই এটি সমাধান করতে দিই।"),
    help="আপনি সংকটের সময় টিমকে কীভাবে পরিচালনা করেন।"
)

leadership_q2 = st.radio(
    "২. একটি টিমের নেতৃত্ব দেওয়ার সময় আপনি সিদ্ধান্ত গ্রহণের প্রক্রিয়া কীভাবে পরিচালনা করেন?",
    ("Option A: এককভাবে সিদ্ধান্ত নেয়া হয়।",
     "Option B: টিমের সদস্যদের মতামত সংগ্রহ করে এবং সেগুলি বিবেচনা করে সিদ্ধান্ত নেয়।",
     "Option C: সিদ্ধান্ত নেওয়ার জন্য উচ্চতর কর্তৃপক্ষের উপর নির্ভর করা হয়।"),
    help="আপনার সিদ্ধান্ত গ্রহণের পদ্ধতি কেমন।"
)

leadership_q3 = st.radio(
    "৩. কাজ ভাগ করার সময় আপনি কীভাবে টিম মেম্বারদের নির্বাচন করেন?",
    ("Option A: এলোমেলোভাবে কাজ ভাগ করে দিই।",
     "Option B: নিজেকে সবচেয়ে গুরুত্বপূর্ণ কাজগুলো রাখি।",
     "Option C: টিম মেম্বারদের দক্ষতা এবং অভিজ্ঞতার উপর ভিত্তি করে কাজ ভাগ করে দিই।"),
    help="আপনি কাজ ভাগ করার সময় কীভাবে টিম মেম্বারদের নির্বাচন করেন।"
)

# ---------------------
# Logic Building Questions
# ---------------------
st.subheader("যৌক্তিক চিন্তা")

logic_q1 = st.radio(
    "১. জটিল কোডিং সমস্যার মুখোমুখি হলে আপনি কীভাবে এটি সমাধান করেন?",
    ("Option A: সমস্যাটি ছোট ছোট অংশে ভাগ করে প্রতিটি ধাপ পদ্ধতিগতভাবে সমাধান করি।",
     "Option B: ইন্টারনেট থেকে কোড কপি করে সমস্যা সমাধান করার চেষ্টা করি।",
     "Option C: কোনো পরিকল্পনা না করে সরাসরি সমস্যাটির মোকাবিলা করি।"),
    help="আপনি জটিল সমস্যার সমাধানে কতটা বিশ্লেষণাত্মক।"
)

logic_q2 = st.radio(
    "২. আপনার সমাধানটি সঠিক কিনা কীভাবে নিশ্চিত করেন?",
    ("Option A: একবার কাজ করলে সঠিক বুঝে নিই।",
     "Option B: বিভিন্ন পরিস্থিতিতে এটি পরীক্ষা করে এর সঠিকতা যাচাই করি।",
     "Option C: অন্যদের উপর নির্ভর করে কাজের সঠিকতা যাচাই করি।"),
    help="আপনি আপনার সমাধানের সঠিকতা কতটা নিশ্চিত করেন।"
)

logic_q3 = st.radio(
    "৩. নতুন প্রোগ্রামিং কনসেপ্ট শেখার পর আপনি কীভাবে এটি আপনার দক্ষতায় অন্তর্ভুক্ত করেন?",
    ("Option A: শুধুমাত্র সিনট্যাক্স মুখস্থ করি এবং এর মূলনীতি বুঝতে চেষ্টা করি না।",
     "Option B: মূল ধারণাগুলো বুঝে সেগুলি বিভিন্ন সমস্যায় প্রয়োগ করি।",
     "Option C: নতুন কনসেপ্টগুলো এড়িয়ে চলি এবং যা জানি তাই ধরে রাখি।"),
    help="নতুন কনসেপ্টগুলি আপনি কীভাবে আপনার দক্ষতায় অন্তর্ভুক্ত করেন।"
)

# ---------------------
# Additional Question (Problem-Solving)
# ---------------------
st.subheader("অতিরিক্ত প্রশ্ন")

additional_q = st.radio(
    "৪. প্রোগ্রামের বাগ ঠিক করার সময় আপনি কীভাবে এটি করেন?",
    ("Option A: এলোমেলো সমাধান চেষ্টা করে দেখি কিছু কাজ করে কিনা।",
     "Option B: কোডটি পদ্ধতিগতভাবে ট্রেস করে সমস্যাটি খুঁজে বের করি।",
     "Option C: সহকর্মী বা অনলাইন উৎস থেকে সাহায্য খুঁজি।"),
    help="বাগ ঠিক করার সময় আপনার সমস্যার সমাধানের পদ্ধতি।"
)

# ---------------------
# Submit and Process
# ---------------------
if st.button("Submit"):
    # Map all answers to scores
    creativity_scores = [
        map_score(creativity_q1.split(":")[0]),
        map_score(creativity_q2.split(":")[0]),
        map_score(creativity_q3.split(":")[0])
    ]

    leadership_scores = [
        map_score(leadership_q1.split(":")[0]),
        map_score(leadership_q2.split(":")[0]),
        map_score(leadership_q3.split(":")[0])
    ]

    logic_scores = [
        map_score(logic_q1.split(":")[0]),
        map_score(logic_q2.split(":")[0]),
        map_score(logic_q3.split(":")[0])
    ]

    additional_score = map_score(additional_q.split(":")[0])

    # Calculate total scores for each category
    total_creativity = sum(creativity_scores)
    total_leadership = sum(leadership_scores)
    total_logic = sum(logic_scores)

    # Determine the talent profile based on highest score
    talent_profile = determine_profile(total_creativity, total_leadership, total_logic)

    # Display the result
    st.success(f"**প্রত্যাশিত প্রতিভা প্রোফাইল:** {talent_profile}")

    # Career suggestions based on profile
    st.subheader("আপনার জন্য উপযুক্ত ক্যারিয়ার:")
    for job in career_suggestions.get(talent_profile, []):
        st.markdown(f"### {job['title']}")
        st.markdown(f"{job['description']} [আরও জানুন]({job['link']})\n")

    # Prepare data for radar chart
    categories = [
        "Creativity Q1", "Creativity Q2", "Creativity Q3",
        "Leadership Q1", "Leadership Q2", "Leadership Q3",
        "Logic Q1", "Logic Q2", "Logic Q3",
        "Additional Q"
    ]

    user_scores = creativity_scores + leadership_scores + logic_scores + [additional_score]

    # Define average scores for different profiles (adjust these based on your actual data)
    average_profiles = {
        "Creative": [9, 9, 9, 5, 5, 5, 3, 3, 3, 5],
        "Logical Wizard": [3, 3, 3, 5, 5, 5, 9, 9, 9, 5],
        "Leader": [5, 5, 5, 9, 9, 9, 5, 5, 5, 5]
    }

    # Create radar chart
    fig = go.Figure()

    # User's data
    fig.add_trace(go.Scatterpolar(
        r=user_scores,
        theta=categories,
        fill='toself',
        name='আপনি',
        line=dict(color='blue')
    ))

    # Average profiles
    border_colors = {
        "Creative": "rgba(128, 128, 128, 1)",         # Gray
        "Logical Wizard": "rgba(255, 165, 0, 1)",     # Orange
        "Leader": "rgba(255, 69, 0, 1)"               # Red
    }

    fill_colors = {
        "Creative": "rgba(128, 128, 128, 0.2)",
        "Logical Wizard": "rgba(255, 165, 0, 0.2)",
        "Leader": "rgba(255, 69, 0, 0.2)"
    }

    for profile, scores in average_profiles.items():
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name=profile,
            line=dict(color=border_colors[profile]),
            fillcolor=fill_colors[profile]
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title="প্রতিভা প্রোফাইল রাডার চার্ট"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Optional: Add Progress Indicator (if you added it above)
    # st.progress(progress)

    # Optional: User Feedback Section
    st.subheader("আপনার প্রতিভা প্রোফাইল সম্পর্কে মতামত দিন:")
    feedback = st.text_area("আপনার মন্তব্য এখানে লিখুন:")
    if st.button("মতামত জমা দিন"):
        if feedback:
            st.write("ধন্যবাদ আপনার মতামতের জন্য!")
            # Here, you can add code to save the feedback for future analysis
        else:
            st.warning("কমেন্ট লিখুন আগে।")
