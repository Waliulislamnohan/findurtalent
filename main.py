import streamlit as st
import numpy as np
import plotly.graph_objects as go
from pymongo import MongoClient
import json
import plotly.io as pio
from datetime import datetime
import random
from dotenv import load_dotenv
import os

# Load environment variables (ensure you have a .env file with MONGODB_URI)
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')  # Securely load your MongoDB URI from environment variables

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

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client['gvprod']  # Ensure 'gvprod' is your actual database name

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

# Career and Department suggestions based on talent profiles
career_suggestions = {
    "Creative": [
        {"title": "Graphic Designer", "description": "Design visual content for brands, advertisements, and products.", "link": "https://www.example.com/graphic-designer"},
        {"title": "Content Creator", "description": "Develop engaging content for various media platforms.", "link": "https://www.example.com/content-creator"},
        {"title": "Marketing Specialist", "description": "Plan and execute marketing campaigns to promote products or services.", "link": "https://www.example.com/marketing-specialist"},
        {"title": "Product Designer", "description": "Design and develop new products from concept to market.", "link": "https://www.example.com/product-designer"},
        {"title": "Art Director", "description": "Lead the visual aspects of creative projects and campaigns.", "link": "https://www.example.com/art-director"},
        # Undergraduate Departments
        {"title": "Bachelor of Arts in Graphic Design", "description": "Focuses on visual communication, typography, and digital media.", "link": "https://daffodilvarsity.edu.bd/programs/graphic-design"},
        {"title": "Bachelor of Arts in Media and Communication", "description": "Covers mass communication, media production, and digital marketing.", "link": "https://daffodilvarsity.edu.bd/programs/media-communication"},
        {"title": "Bachelor of Business Administration (Marketing)", "description": "Emphasizes marketing strategies, consumer behavior, and branding.", "link": "https://daffodilvarsity.edu.bd/programs/bba-marketing"},
        {"title": "Bachelor of Fine Arts", "description": "Explores visual arts, sculpture, painting, and multimedia art.", "link": "https://daffodilvarsity.edu.bd/programs/fine-arts"}
    ],
    "Logical Wizard": [
        {"title": "Software Developer", "description": "Develop and maintain software applications.", "link": "https://www.example.com/software-developer"},
        {"title": "Data Scientist", "description": "Analyze complex data to help make informed business decisions.", "link": "https://www.example.com/data-scientist"},
        {"title": "Systems Analyst", "description": "Evaluate and improve IT systems to meet organizational needs.", "link": "https://www.example.com/systems-analyst"},
        {"title": "Cybersecurity Analyst", "description": "Protect organizational data and systems from cyber threats.", "link": "https://www.example.com/cybersecurity-analyst"},
        {"title": "Database Administrator", "description": "Manage and maintain databases to ensure data integrity and security.", "link": "https://www.example.com/database-administrator"},
        # Undergraduate Departments
        {"title": "Bachelor of Science in Computer Science & Engineering", "description": "Focuses on software development, algorithms, and computer systems.", "link": "https://daffodilvarsity.edu.bd/programs/computer-science-engineering"},
        {"title": "Bachelor of Science in Data Science", "description": "Covers data analysis, machine learning, and big data technologies.", "link": "https://daffodilvarsity.edu.bd/programs/data-science"},
        {"title": "Bachelor of Science in Information Systems", "description": "Emphasizes IT management, systems analysis, and database management.", "link": "https://daffodilvarsity.edu.bd/programs/information-systems"},
        {"title": "Bachelor of Science in Mathematics", "description": "Includes pure and applied mathematics, statistical methods, and modeling.", "link": "https://daffodilvarsity.edu.bd/programs/mathematics"},
        {"title": "Bachelor of Science in Electrical and Electronic Engineering", "description": "Focuses on circuit design, signal processing, and electronics.", "link": "https://daffodilvarsity.edu.bd/programs/electrical-electronic-engineering"}
    ],
    "Leader": [
        {"title": "Project Manager", "description": "Oversee projects from inception to completion, ensuring timely delivery.", "link": "https://www.example.com/project-manager"},
        {"title": "Team Lead", "description": "Guide and support team members to achieve project goals.", "link": "https://www.example.com/team-lead"},
        {"title": "Operations Manager", "description": "Manage daily operations to ensure efficiency and effectiveness.", "link": "https://www.example.com/operations-manager"},
        {"title": "Product Manager", "description": "Lead product development and strategy to meet market demands.", "link": "https://www.example.com/product-manager"},
        {"title": "Human Resources Manager", "description": "Manage HR functions, including recruitment, training, and employee relations.", "link": "https://www.example.com/human-resources-manager"},
        # Undergraduate Departments
        {"title": "Bachelor of Business Administration (BBA)", "description": "Focuses on business management, organizational behavior, and entrepreneurship.", "link": "https://daffodilvarsity.edu.bd/programs/bba"},
        {"title": "Bachelor of Business Administration (Human Resources)", "description": "Emphasizes recruitment, training, and employee relations.", "link": "https://daffodilvarsity.edu.bd/programs/bba-human-resources"},
        {"title": "Bachelor of Business Administration (International Business)", "description": "Covers global trade, international marketing, and cross-cultural management.", "link": "https://daffodilvarsity.edu.bd/programs/bba-international-business"},
        {"title": "Bachelor of Business Administration (Project Management)", "description": "Focuses on project planning, execution, and lifecycle management.", "link": "https://daffodilvarsity.edu.bd/programs/bba-project-management"},
        {"title": "Bachelor of Arts in Public Administration", "description": "Covers public sector management, policy analysis, and governance.", "link": "https://daffodilvarsity.edu.bd/programs/public-administration"}
    ]
}

# Helper function to shuffle options and store in session state
def get_shuffled_options(question_key, options_with_scores):
    shuffle_key = f"shuffled_{question_key}"
    if shuffle_key not in st.session_state:
        shuffled = options_with_scores.copy()
        random.shuffle(shuffled)
        st.session_state[shuffle_key] = shuffled
    return st.session_state[shuffle_key]

# Streamlit App
st.title("Talent Detector")
st.header("Please answer the following questions:")

# Email input field
email = st.text_input(
    "Enter your email (required)",
    help="Your email is used only to personalize the results and will not be sent anywhere.",
)

if email:
    st.info(f"Welcome, {email.split('@')[0].capitalize()}! Let's discover your talents.")

# ---------------------
# Creativity Questions
# ---------------------
st.subheader("সৃজনশীলতা")

# Define Creativity Questions with options and associated scores
creativity_questions = [
    {
        "question": "১. একটি নতুন প্রকল্পে কাজ শুরু করার সময়, আপনি সাধারণত কীভাবে পরিকল্পনা করেন?",
        "options": [
            ("পূর্বের অভিজ্ঞতার ওপর নির্ভর করে কাজ শুরু করি।", 1),
            ("বিভিন্ন উৎস থেকে অনুপ্রেরণা সংগ্রহ করে নতুন আইডিয়া তৈরি করি।", 5),
            ("টিমের সঙ্গে আলোচনা করে এবং যৌথভাবে পরিকল্পনা করি।", 10)
        ],
        "key": "creativity_q1"
    },
    {
        "question": "২. যখন আপনি কোনো সৃজনশীল সমস্যার সম্মুখীন হন, তখন আপনি কীভাবে প্রতিক্রিয়া জানান?",
        "options": [
            ("সমস্যাটির সমাধান এড়িয়ে চলি।", 1),
            ("বিভিন্ন পদ্ধতি ব্যবহার করে সমস্যাটি সমাধানের চেষ্টা করি।", 5),
            ("সমস্যাটি দ্রুত সমাধানের জন্য সহকর্মীদের সাহায্য চাই।", 10)
        ],
        "key": "creativity_q2"
    },
    {
        "question": "৩. টিম মিটিংয়ে আপনি কী ধরনের ভূমিকা পালন করেন?",
        "options": [
            ("শুধুমাত্র শুনি এবং নোট নেয়।", 1),
            ("মাঝে মাঝে কিছু ধারণা শেয়ার করি।", 5),
            ("সক্রিয়ভাবে নতুন আইডিয়া নিয়ে আসি এবং টিমকে উৎসাহিত করি।", 10)
        ],
        "key": "creativity_q3"
    }
]

creativity_scores = []

for q in creativity_questions:
    shuffled_options = get_shuffled_options(q["key"], q["options"])
    option_texts = [option[0] for option in shuffled_options]
    selection = st.radio(
        q["question"],
        option_texts,
        key=f"selection_{q['key']}",
        help="আপনার পরিকল্পনার পদ্ধতি আপনার সৃজনশীলতার মাত্রা নির্ধারণ করে।"
    )
    # Retrieve the score based on the selected option
    selected_score = next(option[1] for option in shuffled_options if option[0] == selection)
    creativity_scores.append(selected_score)

# ---------------------
# Leadership Questions
# ---------------------
st.subheader("নেতৃত্ব")

# Define Leadership Questions with options and associated scores
leadership_questions = [
    {
        "question": "১. যখন আপনার টিম বড় ধরনের সমস্যার সম্মুখীন হয়, তখন আপনি কীভাবে পরিচালনা করেন?",
        "options": [
            ("সমস্যাটির দায়িত্ব নির্দিষ্ট সদস্যদের ওপর চাপিয়ে দিই।", 1),
            ("ইতিবাচক মনোভাব রেখে টিমকে প্রেরণা জোগাই এবং সমাধানের পথ খুঁজে বের করি।", 5),
            ("নিজেকে সমস্যার বাইরে রেখে টিমকে নিজেরাই এটি সমাধান করতে দিই।", 10)
        ],
        "key": "leadership_q1"
    },
    {
        "question": "২. একটি টিমের নেতৃত্ব দেওয়ার সময় আপনি সিদ্ধান্ত গ্রহণের প্রক্রিয়া কীভাবে পরিচালনা করেন?",
        "options": [
            ("এককভাবে সিদ্ধান্ত নেয়া হয়।", 1),
            ("টিমের সদস্যদের মতামত সংগ্রহ করে এবং সেগুলি বিবেচনা করে সিদ্ধান্ত নেয়।", 5),
            ("সিদ্ধান্ত নেওয়ার জন্য উচ্চতর কর্তৃপক্ষের উপর নির্ভর করা হয়।", 10)
        ],
        "key": "leadership_q2"
    },
    {
        "question": "৩. কাজ ভাগ করার সময় আপনি কীভাবে টিম মেম্বারদের নির্বাচন করেন?",
        "options": [
            ("এলোমেলোভাবে কাজ ভাগ করে দিই।", 1),
            ("নিজেকে সবচেয়ে গুরুত্বপূর্ণ কাজগুলো রাখি।", 5),
            ("টিম মেম্বারদের দক্ষতা এবং অভিজ্ঞতার উপর ভিত্তি করে কাজ ভাগ করে দিই।", 10)
        ],
        "key": "leadership_q3"
    }
]

leadership_scores = []

for q in leadership_questions:
    shuffled_options = get_shuffled_options(q["key"], q["options"])
    option_texts = [option[0] for option in shuffled_options]
    selection = st.radio(
        q["question"],
        option_texts,
        key=f"selection_{q['key']}",
        help="আপনি সংকটের সময় টিমকে কীভাবে পরিচালনা করেন।"
    )
    # Retrieve the score based on the selected option
    selected_score = next(option[1] for option in shuffled_options if option[0] == selection)
    leadership_scores.append(selected_score)

# ---------------------
# Logic Building Questions
# ---------------------
st.subheader("যৌক্তিক চিন্তা")

# Define Logic Questions with options and associated scores
logic_questions = [
    {
        "question": "১. জটিল কোডিং সমস্যার মুখোমুখি হলে আপনি কীভাবে এটি সমাধান করেন?",
        "options": [
            ("সমস্যাটি ছোট ছোট অংশে ভাগ করে প্রতিটি ধাপ পদ্ধতিগতভাবে সমাধান করি।", 1),
            ("ইন্টারনেট থেকে কোড কপি করে সমস্যা সমাধান করার চেষ্টা করি।", 5),
            ("কোনো পরিকল্পনা না করে সরাসরি সমস্যাটির মোকাবিলা করি।", 10)
        ],
        "key": "logic_q1"
    },
    {
        "question": "২. আপনার সমাধানটি সঠিক কিনা কীভাবে নিশ্চিত করেন?",
        "options": [
            ("একবার কাজ করলে সঠিক বুঝে নিই।", 1),
            ("বিভিন্ন পরিস্থিতিতে এটি পরীক্ষা করে এর সঠিকতা যাচাই করি।", 5),
            ("অন্যদের উপর নির্ভর করে কাজের সঠিকতা যাচাই করি।", 10)
        ],
        "key": "logic_q2"
    },
    {
        "question": "৩. নতুন প্রোগ্রামিং কনসেপ্ট শেখার পর আপনি কীভাবে এটি আপনার দক্ষতায় অন্তর্ভুক্ত করেন?",
        "options": [
            ("শুধুমাত্র সিনট্যাক্স মুখস্থ করি এবং এর মূলনীতি বুঝতে চেষ্টা করি না।", 1),
            ("মূল ধারণাগুলো বুঝে সেগুলি বিভিন্ন সমস্যায় প্রয়োগ করি।", 5),
            ("নতুন কনসেপ্টগুলো এড়িয়ে চলি এবং যা জানি তাই ধরে রাখি।", 10)
        ],
        "key": "logic_q3"
    }
]

logic_scores = []

for q in logic_questions:
    shuffled_options = get_shuffled_options(q["key"], q["options"])
    option_texts = [option[0] for option in shuffled_options]
    selection = st.radio(
        q["question"],
        option_texts,
        key=f"selection_{q['key']}",
        help="আপনি জটিল সমস্যার সমাধানে কতটা বিশ্লেষণাত্মক।"
    )
    # Retrieve the score based on the selected option
    selected_score = next(option[1] for option in shuffled_options if option[0] == selection)
    logic_scores.append(selected_score)

# ---------------------
# Additional Question (Problem-Solving)
# ---------------------
st.subheader("অতিরিক্ত প্রশ্ন")

# Define Additional Question with options and associated scores
additional_question = {
    "question": "৪. প্রোগ্রামের বাগ ঠিক করার সময় আপনি কীভাবে এটি করেন?",
    "options": [
        ("এলোমেলো সমাধান চেষ্টা করে দেখি কিছু কাজ করে কিনা।", 1),
        ("কোডটি পদ্ধতিগতভাবে ট্রেস করে সমস্যাটি খুঁজে বের করি।", 5),
        ("সহকর্মী বা অনলাইন উৎস থেকে সাহায্য খুঁজি।", 10)
    ],
    "key": "additional_q"
}

additional_scores = []

shuffled_options = get_shuffled_options(additional_question["key"], additional_question["options"])
option_texts = [option[0] for option in shuffled_options]
selection = st.radio(
    additional_question["question"],
    option_texts,
    key=f"selection_{additional_question['key']}",
    help="বাগ ঠিক করার সময় আপনার সমস্যার সমাধানের পদ্ধতি।"
)
# Retrieve the score based on the selected option
selected_score = next(option[1] for option in shuffled_options if option[0] == selection)
additional_scores.append(selected_score)

# ---------------------
# Submit and Process
# ---------------------
if st.button("Submit"):
    # Calculate total scores for each category
    total_creativity = sum(creativity_scores)
    total_leadership = sum(leadership_scores)
    total_logic = sum(logic_scores)
    total_additional = sum(additional_scores)  # Not used in profile determination

    # Determine the talent profile based on highest score
    talent_profile = determine_profile(total_creativity, total_leadership, total_logic)

    # Display the result
    st.success(f"**প্রত্যাশিত প্রতিভা প্রোফাইল:** {talent_profile}")

    # Career and Department suggestions based on profile
    st.subheader("আপনার জন্য উপযুক্ত ক্যারিয়ার এবং ডিপার্টমেন্ট:")
    for suggestion in career_suggestions.get(talent_profile, []):
        st.markdown(f"### {suggestion['title']}")
        st.markdown(f"{suggestion['description']} [আরও জানুন]({suggestion['link']})\n")

    # Prepare data for radar chart
    categories = [
        "Creativity Q1", "Creativity Q2", "Creativity Q3",
        "Leadership Q1", "Leadership Q2", "Leadership Q3",
        "Logic Q1", "Logic Q2", "Logic Q3",
        "Additional Q"
    ]

    user_scores = creativity_scores + leadership_scores + logic_scores + additional_scores

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

    # Save chart to MongoDB if email is provided
    if email:
        user_collection = db['users']
        user = user_collection.find_one({'email': email})
        if user:
            # Serialize the chart to JSON
            chart_json = pio.to_json(fig)
            charts_collection = db['charts']
            chart_data = {
                'email': email,
                'timestamp': datetime.utcnow(),
                'talent_profile': talent_profile,
                'scores': {
                    'creativity_scores': creativity_scores,
                    'leadership_scores': leadership_scores,
                    'logic_scores': logic_scores,
                    'additional_score': additional_scores,
                },
                'chart_json': chart_json,
            }
            try:
                # Use replace_one with upsert=True to overwrite existing data or insert new
                charts_collection.replace_one({'email': email}, chart_data, upsert=True)
                st.success("Your results have been saved.")
            except Exception as e:
                st.error(f"An error occurred while saving your results: {e}")
        else:
            st.warning("Email not found in the database.")
    else:
        st.warning("Please enter your email to save your results.")

    # Optional: User Feedback Section
    st.subheader("আপনার প্রতিভা প্রোফাইল সম্পর্কে মতামত দিন:")
    feedback = st.text_area("আপনার মন্তব্য এখানে লিখুন:")
    if st.button("মতামত জমা দিন"):
        if feedback:
            try:
                feedback_collection = db['feedback']
                feedback_data = {
                    'email': email,
                    'timestamp': datetime.utcnow(),
                    'feedback': feedback
                }
                feedback_collection.insert_one(feedback_data)
                st.write("ধন্যবাদ আপনার মতামতের জন্য!")
            except Exception as e:
                st.error(f"An error occurred while saving your feedback: {e}")
        else:
            st.warning("কমেন্ট লিখুন আগে।")
