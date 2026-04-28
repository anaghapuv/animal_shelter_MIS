import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PawHaven Shelter MIS",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════
# DESIGN SYSTEM: Green & Peach High-Contrast Theme
# ══════════════════════════════════════════════════════════
THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Hide Streamlit Default Elements safely */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header { background-color: transparent !important; }
.stApp > header [data-testid="stToolbar"] { display: none !important; }

html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
.stApp { background-color: #FDF8F5 !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #2A3C33 !important;
    border-right: none !important;
    box-shadow: 4px 0 15px rgba(0,0,0,0.05);
}
section[data-testid="stSidebar"] * { color: #E8ECEA !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 8px; }
section[data-testid="stSidebar"] .stRadio label {
    background: transparent !important; border-radius: 8px !important;
    padding: 12px 16px !important; margin: 0 !important; cursor: pointer !important;
    transition: all 0.3s ease !important; border: 1px solid rgba(255,255,255,0.05) !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(224, 122, 95, 0.15) !important; border-color: #E07A5F !important;
}
section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p {
    font-size: 0.95rem !important; font-weight: 500 !important;
}
section[data-testid="stSidebar"] .stRadio input[type="radio"], 
section[data-testid="stSidebar"] .stRadio div[data-testid="stRadio"] > div > div > div > div:first-child {
    display: none !important;
}

/* Headings */
h1 { color: #1E2B25 !important; font-weight: 700 !important; letter-spacing: -0.5px; }
h2 { color: #2A3C33 !important; font-weight: 600 !important; letter-spacing: -0.5px; }
h3 { color: #405B4D !important; font-weight: 600 !important; }
p, span, label { color: #364940 !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF !important; border-radius: 16px !important; padding: 20px 24px !important;
    border: 1px solid #F0E6DF !important; box-shadow: 0 4px 12px rgba(42, 60, 51, 0.04) !important;
    border-left: 5px solid #E07A5F !important;
}
[data-testid="stMetricLabel"] { color: #728A7E !important; font-size: 0.85rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px; }
[data-testid="stMetricValue"] { color: #1E2B25 !important; font-size: 2.2rem !important; font-weight: 700 !important; }

/* Buttons */
.stButton > button[kind="primary"] {
    background-color: #E07A5F !important; color: #FFFFFF !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important; padding: 10px 24px !important;
    transition: all 0.3s ease !important; box-shadow: 0 4px 14px rgba(224, 122, 95, 0.3) !important;
}
.stButton > button[kind="primary"]:hover { background-color: #D36649 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(224, 122, 95, 0.4) !important; }
.stButton > button:not([kind="primary"]) {
    background-color: transparent !important; color: #405B4D !important; border: 2px solid #405B4D !important;
    border-radius: 8px !important; font-weight: 600 !important; transition: all 0.3s ease !important;
}
.stButton > button:not([kind="primary"]):hover { background-color: #405B4D !important; color: #FFFFFF !important; }

/* Forms, Tabs, Expanders */
div[data-testid="stForm"] { background: #FFFFFF !important; border-radius: 16px !important; padding: 24px !important; border: 1px solid #F0E6DF !important; box-shadow: 0 4px 16px rgba(42, 60, 51, 0.03) !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input {
    background: #FCF9F7 !important; color: #1E2B25 !important; border: 1.5px solid #E8DFD8 !important; border-radius: 8px !important; padding: 10px !important;
}
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 2px solid #F0E6DF !important; gap: 24px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #728A7E !important; font-weight: 500 !important; border: none !important; padding: 10px 0 !important; }
.stTabs [aria-selected="true"] { color: #E07A5F !important; font-weight: 600 !important; border-bottom: 3px solid #E07A5F !important; }
.streamlit-expanderHeader { background: #FFFFFF !important; color: #2A3C33 !important; border-radius: 10px !important; font-weight: 600 !important; border: 1px solid #F0E6DF !important; }
.streamlit-expanderContent { background: #FFFFFF !important; border: 1px solid #F0E6DF !important; border-top: none !important; border-radius: 0 0 10px 10px !important; color: #1E2B25 !important; }
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid #F0E6DF !important; box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important; }

/* Cards & Pills */
.info-card { background: #FFFFFF; color: #1E2B25 !important; border-radius: 16px; padding: 20px; border: 1px solid #F0E6DF; box-shadow: 0 4px 12px rgba(42, 60, 51, 0.04); margin-bottom: 16px; transition: transform 0.2s ease; }
.info-card strong { color: #1E2B25 !important; }
.info-card h4 { color: #1E2B25 !important; margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 600;}
.pill { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.3px; text-transform: uppercase; }
.pill-green  { background: #E6F0EA; color: #2A5A3B; border: 1px solid #CDE1D4; }
.pill-peach  { background: #FDECE7; color: #B3482A; border: 1px solid #FAD1C6; }
.pill-sage   { background: #E8EEEA; color: #405B4D; border: 1px solid #D1DDD6; }
.pill-amber  { background: #FFF4E5; color: #925D0E; border: 1px solid #FEE3B8; }
.pill-blue   { background: #E8F0FE; color: #1A4B9C; border: 1px solid #C4D9FD; }
.sec-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #8C9E94; margin-bottom: 12px; margin-top: 24px; border-bottom: 2px solid #F0E6DF; padding-bottom: 8px; }
</style>
"""
st.markdown(THEME, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# DATA INITIALIZATION & LIFECYCLE MANAGEMENT
# ══════════════════════════════════════════════════════════
def init_state():
    now = datetime.now()

    if 'logged_in_user' not in st.session_state: 
        st.session_state.logged_in_user = None
    
    if 'audit_log' not in st.session_state: 
        st.session_state.audit_log = []

    if 'users' not in st.session_state:
        st.session_state.users = [
            {"user_id": 1, "username": "vet",       "password": "123", "role": "Veterinarian",         "full_name": "Dr. Priya Sharma"},
            {"user_id": 2, "username": "coord",     "password": "123", "role": "Volunteer Coordinator","full_name": "Rahul Mehta"},
            {"user_id": 3, "username": "counselor", "password": "123", "role": "Adoption Counselor",   "full_name": "Anita Desai"},
            {"user_id": 4, "username": "manager",   "password": "123", "role": "Manager",              "full_name": "Suresh Kumar"},
            {"user_id": 5, "username": "volunteer", "password": "123", "role": "Volunteer",            "full_name": "Sarah Johnson"},
        ]

    # LOGICAL LIFECYCLE: Awaiting Medical -> Available -> Adoption Pending -> Adopted
    if 'animals' not in st.session_state:
        st.session_state.animals = [
            # Adopted (3 animals)
            {"id": 1001, "species": "Dog",    "breed": "Labrador (Bella)",   "age_months": 24, "weight_kg": 22.5, "sex": "Female", "arrival_date": (now-timedelta(days=40)).date(), "status": "Adopted"},
            {"id": 1002, "species": "Cat",    "breed": "Shorthair (Luna)",   "age_months": 12, "weight_kg": 4.2,  "sex": "Female", "arrival_date": (now-timedelta(days=35)).date(), "status": "Adopted"},
            {"id": 1003, "species": "Dog",    "breed": "Beagle (Max)",       "age_months": 36, "weight_kg": 14.0, "sex": "Male",   "arrival_date": (now-timedelta(days=30)).date(), "status": "Adopted"},
            
            # Adoption Pending (2 animals)
            {"id": 1004, "species": "Rabbit", "breed": "Holland Lop (Daisy)","age_months": 8,  "weight_kg": 1.8,  "sex": "Female", "arrival_date": (now-timedelta(days=20)).date(), "status": "Adoption Pending"},
            {"id": 1005, "species": "Dog",    "breed": "Retriever (Charlie)","age_months": 18, "weight_kg": 28.0, "sex": "Male",   "arrival_date": (now-timedelta(days=18)).date(), "status": "Adoption Pending"},
            
            # Available / Medically Cleared (2 animals)
            {"id": 1006, "species": "Cat",    "breed": "Persian (Milo)",     "age_months": 48, "weight_kg": 5.0,  "sex": "Male",   "arrival_date": (now-timedelta(days=15)).date(), "status": "Available"},
            {"id": 1007, "species": "Dog",    "breed": "Poodle Mix (Rocky)", "age_months": 60, "weight_kg": 9.5,  "sex": "Male",   "arrival_date": (now-timedelta(days=12)).date(), "status": "Available"},
            
            # Awaiting Medical / Failed Medical (2 animals)
            {"id": 1008, "species": "Cat",    "breed": "Siamese (Oliver)",   "age_months": 6,  "weight_kg": 2.8,  "sex": "Male",   "arrival_date": (now-timedelta(days=3)).date(),  "status": "Awaiting Medical"},
            {"id": 1009, "species": "Dog",    "breed": "Shepherd (Leo)",     "age_months": 30, "weight_kg": 35.0, "sex": "Male",   "arrival_date": now.date(),                      "status": "Awaiting Medical"},
        ]

    if 'medical_records' not in st.session_state:
        st.session_state.medical_records = [
            {"record_id": 1, "animal_id": 1004, "veterinarian_name": "Dr. Priya", "exam_date": now-timedelta(days=18), "diagnosis": "Healthy", "vaccinations": "RVHD2",  "medications": "None", "notes": "Clear", "is_cleared": True},
            {"record_id": 2, "animal_id": 1005, "veterinarian_name": "Dr. Priya", "exam_date": now-timedelta(days=15), "diagnosis": "Healthy", "vaccinations": "Rabies", "medications": "None", "notes": "Clear", "is_cleared": True},
            {"record_id": 3, "animal_id": 1006, "veterinarian_name": "Dr. Priya", "exam_date": now-timedelta(days=13), "diagnosis": "Healthy", "vaccinations": "FVRCP",  "medications": "None", "notes": "Clear", "is_cleared": True},
            {"record_id": 4, "animal_id": 1007, "veterinarian_name": "Dr. Priya", "exam_date": now-timedelta(days=10), "diagnosis": "Healthy", "vaccinations": "Rabies", "medications": "None", "notes": "Clear", "is_cleared": True},
            {"record_id": 5, "animal_id": 1008, "veterinarian_name": "Dr. Priya", "exam_date": now-timedelta(days=2),  "diagnosis": "URI",     "vaccinations": "None",   "medications": "Doxy", "notes": "Not clear", "is_cleared": False},
        ]

    if 'applications' not in st.session_state:
        st.session_state.applications = [
            {"app_id": 401, "animal_id": 1004, "adopter_name": "John Smith",   "adopter_contact": "john@example.com", "home_type": "House", "other_pets": "None", "application_date": now-timedelta(hours=24), "review_date": None, "status": "Pending", "counselor_id": 3},
            {"app_id": 402, "animal_id": 1005, "adopter_name": "Sarah Connor", "adopter_contact": "sarah@example.com","home_type": "House", "other_pets": "Dog",  "application_date": now-timedelta(hours=49), "review_date": None, "status": "Pending", "counselor_id": 3},
            {"app_id": 403, "animal_id": 1005, "adopter_name": "Kyle Reese",   "adopter_contact": "kyle@example.com", "home_type": "Apt",   "other_pets": "None", "application_date": now-timedelta(hours=10), "review_date": None, "status": "Pending", "counselor_id": 3},
        ]

    if 'adoptions' not in st.session_state:
        st.session_state.adoptions = [
            {"adoption_id": 501, "application_id": 301, "animal_id": 1001, "adoption_date": (now-timedelta(days=35)).date(), "adopter_name": "Vikram Nair", "adopter_signature": "V.Nair"},
            {"adoption_id": 502, "application_id": 302, "animal_id": 1002, "adoption_date": (now-timedelta(days=30)).date(), "adopter_name": "Sandra Lee",  "adopter_signature": "S.Lee"},
            {"adoption_id": 503, "application_id": 303, "animal_id": 1003, "adoption_date": (now-timedelta(days=25)).date(), "adopter_name": "Amit Patel",  "adopter_signature": "A.Patel"},
        ]

    if 'volunteers' not in st.session_state:
        st.session_state.volunteers = [
            {"id": 201, "name": "Sarah Johnson", "email": "sarah@example.com", "phone": "555-0101", "skills": ["Dog Walking","Cleaning"], "availability": ["Weekday AM"], "total_hours": 48, "joined": (now-timedelta(days=120)).date()},
            {"id": 202, "name": "Mike Chen",     "email": "mike@example.com",  "phone": "555-0102", "skills": ["Administrative"], "availability": ["Weekday PM"], "total_hours": 32, "joined": (now-timedelta(days=90)).date()},
            {"id": 203, "name": "David Kim",     "email": "david@example.com", "phone": "555-0103", "skills": ["Event Support","Dog Walking"], "availability": ["Weekend AM", "Weekend PM"], "total_hours": 115, "joined": (now-timedelta(days=200)).date()},
            {"id": 204, "name": "Elena Garcia",  "email": "elena@example.com", "phone": "555-0104", "skills": ["Cat Socialization","Cleaning"], "availability": ["Weekday PM"], "total_hours": 12, "joined": (now-timedelta(days=15)).date()},
            {"id": 205, "name": "Frank Castle",  "email": "frank@example.com", "phone": "555-0105", "skills": ["Vet Assistance","Cleaning"], "availability": ["Weekday AM", "Weekend AM"], "total_hours": 210, "joined": (now-timedelta(days=365)).date()},
            {"id": 206, "name": "Grace Lee",     "email": "grace@example.com", "phone": "555-0106", "skills": ["Administrative","Event Support"], "availability": ["Weekday PM", "Weekend PM"], "total_hours": 60, "joined": (now-timedelta(days=150)).date()},
            {"id": 207, "name": "Henry Cavill",  "email": "henry@example.com", "phone": "555-0107", "skills": ["Dog Walking"], "availability": ["Weekend AM"], "total_hours": 5, "joined": (now-timedelta(days=5)).date()},
        ]

    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {"id": 301, "description": "Deep clean kennels", "required_skills": ["Cleaning"], "task_date": now.date(), "start_time": "08:00", "duration": 2.0, "status": "Completed", "coordinator_id": 2},
            {"id": 302, "description": "Update intake DB",   "required_skills": ["Administrative"], "task_date": now.date(), "start_time": "10:00", "duration": 1.5, "status": "In Progress", "coordinator_id": 2},
            {"id": 303, "description": "Walk Charlie (Dog)", "required_skills": ["Dog Walking"], "task_date": now.date(), "start_time": "14:00", "duration": 1.0, "status": "Assigned", "coordinator_id": 2},
            {"id": 304, "description": "Filing paperwork",   "required_skills": ["Administrative"], "task_date": now.date(), "start_time": "15:00", "duration": 1.0, "status": "Open", "coordinator_id": 2},
        ]

    if 'assignments' not in st.session_state:
        st.session_state.assignments = [
            {"assignment_id": 601, "task_id": 301, "volunteer_id": 201, "assigned_date": now.date(), "check_in_time": now-timedelta(hours=4), "check_out_time": now-timedelta(hours=2), "hours_worked": 2.0},
            {"assignment_id": 602, "task_id": 302, "volunteer_id": 202, "assigned_date": now.date(), "check_in_time": now-timedelta(hours=1), "check_out_time": None, "hours_worked": 0},
            {"assignment_id": 603, "task_id": 303, "volunteer_id": 201, "assigned_date": now.date(), "check_in_time": None, "check_out_time": None, "hours_worked": 0},
        ]

init_state()

# ══════════════════════════════════════════════════════════
# HELPERS & AUDIT LOGGING
# ══════════════════════════════════════════════════════════
def log_audit(action_desc):
    user = st.session_state.logged_in_user
    user_str = f"{user['full_name']} ({user['role']})" if user else "System Auth"
    st.session_state.audit_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_str,
        "action": action_desc
    })

STATUS_PILL = {
    "Awaiting Medical": ("pill-amber",  "Awaiting Medical"),
    "Available":        ("pill-green",  "Available"),
    "Adoption Pending": ("pill-blue",   "Adoption Pending"),
    "Adopted":          ("pill-peach",  "Adopted"),
    "Open":             ("pill-sage",   "Open"),
    "Assigned":         ("pill-blue",   "Assigned"),
    "In Progress":      ("pill-amber",  "In Progress"),
    "Completed":        ("pill-green",  "Completed")
}

def pill(status):
    cls, label = STATUS_PILL.get(status, ("pill-sage", status))
    return f'<span class="pill {cls}">{label}</span>'

def sec(label):
    st.markdown(f'<div class="sec-label">{label}</div>', unsafe_allow_html=True)

def animal_label(a):
    return f"#{a['id']} — {a['breed']} ({a['species']})"


# ══════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════
def login_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div style="background:#FFFFFF; border-radius:24px; padding:40px;
                    border:1px solid #F0E6DF; box-shadow:0 10px 40px rgba(224, 122, 95, 0.08);
                    text-align:center; margin-bottom:20px;">
          <div style="font-size:3.5rem; margin-bottom:12px;">🐾</div>
          <h2 style="color:#1E2B25 !important; margin:0; font-size:1.8rem; font-weight:700;">PawHaven MIS</h2>
          <p style="color:#728A7E; margin:8px 0 24px 0; font-size:0.95rem;">Secure Access Portal</p>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="e.g. manager")
        password = st.text_input("Password", type="password", placeholder="Password is 123 for all users")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Authenticate", use_container_width=True, type="primary"):
            user = next((u for u in st.session_state.users
                         if u["username"] == username and u["password"] == password), None)
            if user:
                st.session_state.logged_in_user = user
                log_audit("Logged into the system.")
                st.rerun()
            else:
                st.error("Authentication failed. Please check credentials.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔑 Access Demo Credentials"):
            rows = [
                ("Veterinarian",          "vet",         "123"),
                ("Volunteer Coordinator", "coord",       "123"),
                ("Adoption Counselor",    "counselor",   "123"),
                ("Manager",              "manager",     "123"),
                ("Volunteer",            "volunteer",   "123"),
            ]
            for role, u, p in rows:
                st.markdown(f"<span style='color:#E07A5F;font-weight:600'>{role}</span>&nbsp;—&nbsp;`{u}` / `{p}`", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════
def dashboard_page():
    user     = st.session_state.logged_in_user
    now      = datetime.now()
    animals  = st.session_state.animals
    vols     = st.session_state.volunteers
    apps     = st.session_state.applications
    adoptions= st.session_state.adoptions

    # STRICT METRIC CALCULATIONS
    pending    = [a for a in apps if a["status"] == "Pending"]
    overdue    = [a for a in pending if (now - a["application_date"]).total_seconds()/3600 >= 48]
    
    in_shelter = [a for a in animals if a["status"] != "Adopted"]
    available  = [a for a in animals if a["status"] == "Available"]
    open_tasks = [t for t in st.session_state.tasks if t["status"] == "Open"]
    total_hrs  = sum(v["total_hours"] for v in vols)

    st.markdown(f"<h1>🏠 Operations Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#728A7E;margin-top:-10px; font-size:1.05rem;'>Welcome back, <strong style='color:#E07A5F'>{user['full_name']}</strong> &nbsp;·&nbsp; {now.strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🐾 Animals in Care",    len(in_shelter))
    c2.metric("✨ Ready to Adopt",      len(available))
    c3.metric("📋 Unassigned Tasks",   len(open_tasks))
    c4.metric("🏠 Total Adoptions",    len(adoptions))
    c5.metric("🚨 Overdue Alerts",     len(overdue))

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.15, 1])

    with left:
        sec("ANIMAL STATUS BREAKDOWN")
        status_order = ["Awaiting Medical", "Available", "Adoption Pending", "Adopted"]
        counts = {s: sum(1 for a in animals if a["status"] == s) for s in status_order}
        max_c  = max(counts.values()) if any(counts.values()) else 1

        for status, count in counts.items():
            pct   = count / max_c
            cols_ = st.columns([0.35, 0.50, 0.08])
            cols_[0].markdown(f"<span style='font-size:0.85rem;color:#405B4D; font-weight:500;'>{status}</span>", unsafe_allow_html=True)
            cols_[1].progress(pct)
            cols_[2].markdown(f"<span style='font-weight:700;color:#1E2B25;font-size:0.95rem'>{count}</span>", unsafe_allow_html=True)

        sec("RECENT ANIMAL ARRIVALS")
        recent = sorted(animals, key=lambda x: x["arrival_date"], reverse=True)[:4]
        for a in recent:
            st.markdown(
                f"""<div class="info-card">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <div style="font-weight:600;color:#1E2B25; font-size:1.05rem;">#{a['id']}&nbsp;{a['breed']}</div>
                      <div style="color:#728A7E;font-size:0.85rem;margin-top:2px;">{a['species']} &nbsp;·&nbsp; {a['age_months']}mo</div>
                    </div>
                    {pill(a['status'])}
                  </div>
                </div>""",
                unsafe_allow_html=True
            )

    with right:
        sec("48-HOUR APPLICATION ALERTS (FR8)")
        if pending:
            for app in pending:
                elapsed_h  = (now - app["application_date"]).total_seconds() / 3600
                animal_obj = next((a for a in animals if a["id"] == app["animal_id"]), {})
                breed      = animal_obj.get("breed", "Unknown")
                remaining  = 48 - elapsed_h
                
                if elapsed_h >= 48:
                    st.error(f"🚨 **{app['adopter_name']}** → {breed}\n\nOverdue by **{elapsed_h-48:.0f}h**. Alert repeating every 12h.")
                elif elapsed_h >= 36:
                    st.warning(f"⚠️ **{app['adopter_name']}** → {breed}\n\n{remaining:.1f}h until alert triggers.")
                else:
                    st.info(f"📋 **{app['adopter_name']}** → {breed}\n\n{remaining:.1f}h remaining.")
        else:
            st.success("✅ All applications reviewed — no pending alerts.")

        sec("VOLUNTEER LEADERBOARD")
        top_vols = sorted(vols, key=lambda x: x["total_hours"], reverse=True)
        max_h    = top_vols[0]["total_hours"] if top_vols else 1
        medals   = ["🏆","🥈","🥉"]
        for i, v in enumerate(top_vols[:5]):
            badge = medals[i] if i < 3 else "🔸"
            c_a, c_b, c_c = st.columns([0.10, 0.48, 0.12])
            c_a.markdown(f"<span style='font-size:1.1rem'>{badge}</span>", unsafe_allow_html=True)
            c_b.progress(v["total_hours"] / max_h)
            c_c.markdown(f"<span style='font-weight:700;color:#E07A5F;font-size:0.9rem'>{v['total_hours']}h</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.85rem;color:#5C746A;margin-left:36px'>{v['name']}</span>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# FR1 — Animal Intake
# ══════════════════════════════════════════════════════════
def animal_intake_page():
    st.markdown("<h1>📝 Animal Intake</h1>", unsafe_allow_html=True)
    
    left, right = st.columns([1, 1.3])
    with left:
        sec("REGISTER NEW ARRIVAL")
        with st.form("intake_form", clear_on_submit=True):
            species   = st.selectbox("Species", ["Dog","Cat","Rabbit","Bird","Other"])
            breed     = st.text_input("Breed / Description")
            c1, c2    = st.columns(2)
            sex       = c1.selectbox("Sex", ["Male","Female","Unknown"])
            age       = c2.number_input("Age (months)", min_value=0, step=1, value=12)
            weight    = st.number_input("Weight (kg)", min_value=0.1, step=0.5, value=5.0)
            arrival   = st.date_input("Arrival Date", value=datetime.now().date())

            if st.form_submit_button("🐾 Register Animal", use_container_width=True, type="primary"):
                if not breed.strip(): 
                    st.error("Please enter a breed.")
                else:
                    new_id = max((a["id"] for a in st.session_state.animals), default=1000) + 1
                    # New animals are ALWAYS "Awaiting Medical"
                    st.session_state.animals.append({
                        "id": new_id, "species": species, "breed": breed.strip(),
                        "age_months": age, "weight_kg": weight, "sex": sex,
                        "arrival_date": arrival, "status": "Awaiting Medical"
                    })
                    log_audit(f"Intake: {species} ({breed.strip()}) assigned ID #{new_id}")
                    st.success(f"✅ Registered — Auto ID: **{new_id}** | Status: **Awaiting Medical**")
                    st.rerun()

    with right:
        sec("ALL ANIMALS IN CARE")
        in_care = [a for a in st.session_state.animals if a["status"] != "Adopted"]
        if in_care:
            df = pd.DataFrame(in_care)[["id", "species", "breed", "age_months", "weight_kg", "status"]]
            st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
# FR2 & FR3 — Medical Records
# ══════════════════════════════════════════════════════════
def medical_page():
    st.markdown("<h1>🩺 Medical Records & Clearance</h1>", unsafe_allow_html=True)
    
    animals = st.session_state.animals
    
    # Vets only evaluate animals that are NOT adopted and NOT currently pending adoption
    non_adopted = [a for a in animals if a["status"] in ["Awaiting Medical", "Available"]]
    
    if not non_adopted:
        st.warning("No animals currently require medical evaluation.")
        return

    left, right = st.columns([1, 1.1])
    with left:
        sec("EXAMINATION FORM")
        opts   = {f"#{a['id']} — {a['breed']}": a for a in non_adopted}
        sel    = st.selectbox("Select Animal", list(opts.keys()))
        
        # Get the actual animal object from session state
        animal = opts[sel]

        st.markdown(f"<div style='margin-bottom:12px; font-size:0.9rem;'>Current status:&nbsp;{pill(animal['status'])}</div>", unsafe_allow_html=True)

        with st.form("medical_form", clear_on_submit=True):
            vet_name  = st.text_input("Veterinarian Name", value=st.session_state.logged_in_user.get("full_name",""))
            diagnosis = st.text_area("Diagnosis", height=90)
            c1, c2    = st.columns(2)
            vax       = c1.text_input("Vaccinations")
            meds      = c2.text_input("Medications")
            cleared   = st.checkbox("✅ Mark as Medically Cleared (Available for Adoption)")

            if st.form_submit_button("💾 Save Medical Record", use_container_width=True, type="primary"):
                rec_id = max((r["record_id"] for r in st.session_state.medical_records), default=0) + 1
                
                st.session_state.medical_records.append({
                    "record_id": rec_id, "animal_id": animal["id"], "veterinarian_name": vet_name,
                    "diagnosis": diagnosis, "vaccinations": vax, "medications": meds,
                    "exam_date": datetime.now(), "is_cleared": cleared
                })
                
                # STATE MUTATION: Update animal status based on vet decision
                if cleared:
                    for anim in st.session_state.animals:
                        if anim["id"] == animal["id"]:
                            anim["status"] = "Available"
                            break
                    log_audit(f"Medically cleared animal #{animal['id']} for adoption.")
                    st.success("🎉 Status → **Available**. Visible for adoption! (FR3)")
                else:
                    for anim in st.session_state.animals:
                        if anim["id"] == animal["id"]:
                            anim["status"] = "Awaiting Medical"
                            break
                    log_audit(f"Logged exam for animal #{animal['id']} (Not Cleared).")
                    st.success("📋 Record saved. Status → **Awaiting Medical**.")
                
                st.rerun()

    with right:
        sec(f"RECORD HISTORY — Animal #{animal['id']}")
        recs = [r for r in st.session_state.medical_records if r["animal_id"] == animal["id"]]
        if recs:
            for r in reversed(recs):
                with st.expander(f"📋 Record #{r['record_id']} — {r['exam_date'].strftime('%d %b %Y')}"):
                    st.markdown(f"**Diagnosis:** {r['diagnosis'] or '—'} | **Vax:** {r['vaccinations'] or '—'} | **Meds:** {r['medications'] or '—'}")
                    st.markdown(f"**Clearance:** {'✅ Yes' if r['is_cleared'] else '❌ No'}")
        else:
            st.info("No records for this animal yet.")


# ══════════════════════════════════════════════════════════
# FR4 — Volunteer Registration
# ══════════════════════════════════════════════════════════
def volunteer_registration_page():
    st.markdown("<h1>🙋 Volunteer Management</h1>", unsafe_allow_html=True)
    
    SKILLS = ["Dog Walking","Cat Socialization","Cleaning","Administrative","Event Support","Vet Assistance"]
    left, right = st.columns([1, 1.2])

    with left:
        sec("NEW VOLUNTEER PROFILE")
        with st.form("vol_form", clear_on_submit=True):
            name   = st.text_input("Full Name")
            email  = st.text_input("Email Address")
            skills = st.multiselect("Skills", SKILLS)
            
            if st.form_submit_button("📝 Register", use_container_width=True, type="primary"):
                if not name.strip() or not email.strip(): 
                    st.error("Name and email are required.")
                else:
                    new_id = max((v["id"] for v in st.session_state.volunteers), default=200) + 1
                    st.session_state.volunteers.append({
                        "id": new_id, "name": name.strip(), "email": email.strip(),
                        "skills": skills, "total_hours": 0, "joined": datetime.now().date()
                    })
                    log_audit(f"Registered new volunteer: {name.strip()} (ID: {new_id})")
                    st.success(f"✅ Registered **{name}**")
                    st.rerun()

    with right:
        sec("REGISTERED VOLUNTEERS")
        if st.session_state.volunteers:
            df = pd.DataFrame(st.session_state.volunteers)[["id", "name", "email", "total_hours"]]
            st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
# FR5 — Task Management
# ══════════════════════════════════════════════════════════
def task_management_page():
    st.markdown("<h1>📋 Task Allocation</h1>", unsafe_allow_html=True)
    
    SKILLS = ["Dog Walking","Cat Socialization","Cleaning","Administrative","Event Support","Vet Assistance"]
    left, right = st.columns([1, 1.2])

    with left:
        sec("CREATE NEW TASK")
        with st.form("task_form", clear_on_submit=True):
            desc       = st.text_area("Task Description", height=90)
            req_skills = st.multiselect("Required Skills", SKILLS)
            duration   = st.number_input("Duration (hours)", min_value=0.5, step=0.5, value=1.0)

            if st.form_submit_button("📌 Create Task", use_container_width=True, type="primary"):
                if not desc.strip() or not req_skills: 
                    st.error("Description and at least one skill are required.")
                else:
                    new_id = max((t["id"] for t in st.session_state.tasks), default=300) + 1
                    st.session_state.tasks.append({
                        "id": new_id, "description": desc.strip(), "required_skills": req_skills, 
                        "task_date": datetime.now().date(), "duration": duration, "status": "Open",
                    })
                    log_audit(f"Created task #{new_id}")
                    st.success("✅ Task created!")
                    st.rerun()

    with right:
        sec("ALL TASKS")
        for task in sorted(st.session_state.tasks, key=lambda x: x["task_date"], reverse=True):
            
            # Plain text in expander title
            with st.expander(f"📌 Task #{task['id']} — {task['description'][:48]} ({task['status']})", expanded=(task['status'] == 'Open')):
                
                # HTML pill inside the expander
                st.markdown(f"{pill(task['status'])}", unsafe_allow_html=True)
                st.write(f"**Required Skills:** {', '.join(task['required_skills'])} | **Duration:** {task['duration']}h")

                if task["status"] == "Open":
                    # Task Matching Algorithm
                    matched = [v for v in st.session_state.volunteers if any(s in v["skills"] for s in task["required_skills"])]
                    if matched:
                        st.markdown(f"**Matched ({len(matched)}):** " + ", ".join(v["name"] for v in matched))
                        sel_v = st.selectbox("Assign to", [v["name"] for v in matched], key=f"sel_{task['id']}")
                        
                        if st.button("✅ Assign", key=f"asgn_{task['id']}", type="primary"):
                            vol_obj = next(v for v in matched if v["name"] == sel_v)
                            
                            # Create new assignment
                            st.session_state.assignments.append({
                                "assignment_id": len(st.session_state.assignments)+601,
                                "task_id": task["id"], "volunteer_id": vol_obj["id"],
                                "assigned_date": datetime.now().date(),
                                "check_in_time": None, "check_out_time": None, "hours_worked": 0
                            })
                            
                            # State Mutation!
                            for t in st.session_state.tasks:
                                if t["id"] == task["id"]:
                                    t["status"] = "Assigned"
                                    break
                            
                            log_audit(f"Assigned task #{task['id']} to {sel_v}.")
                            st.success(f"Assigned to {sel_v}!")
                            st.rerun()
                    else:
                        st.warning("No volunteers match the required skills.")
                else:
                    # Task is already assigned
                    asgn = next((a for a in st.session_state.assignments if a["task_id"] == task["id"]), None)
                    if asgn:
                        vol = next((v for v in st.session_state.volunteers if v["id"] == asgn["volunteer_id"]), {})
                        st.info(f"Assigned to: **{vol.get('name','?')}**")


# ══════════════════════════════════════════════════════════
# FR6 — Volunteer Check-In
# ══════════════════════════════════════════════════════════
def volunteer_checkin_page():
    st.markdown("<h1>✅ Attendance</h1>", unsafe_allow_html=True)
    
    user = st.session_state.logged_in_user
    vol  = next((v for v in st.session_state.volunteers if v["name"].lower() == user["full_name"].lower()), None)
    
    if not vol:
        st.error("No profile linked to this user account.")
        return

    left, right = st.columns([1, 1.1])
    with left:
        st.metric("Total Hours Contributed", f"{vol['total_hours']}h")
        sec("MY ACTIVE ASSIGNMENTS")
        
        my_asgns = [a for a in st.session_state.assignments if a["volunteer_id"] == vol["id"]]
        my_tasks = [t for t in st.session_state.tasks if t["id"] in [a["task_id"] for a in my_asgns] and t["status"] in ["Assigned", "In Progress"]]

        if not my_tasks: 
            st.info("You have no active assignments right now.")
        
        for task in my_tasks:
            asgn = next(a for a in my_asgns if a["task_id"] == task["id"])
            
            # Plain text in expander title
            with st.expander(f"📌 Task #{task['id']} — {task['description'][:48]} ({task['status']})", expanded=True):
                
                # HTML pill inside the expander
                st.markdown(f"{pill(task['status'])}", unsafe_allow_html=True)
                st.caption(f"Date: {task['task_date']} | Scheduled Duration: {task['duration']}h")
                
                if task["status"] == "Assigned":
                    if st.button("🟢 Check In", key=f"ci_{task['id']}", type="primary"):
                        for t in st.session_state.tasks:
                            if t["id"] == task["id"]: t["status"] = "In Progress"
                        
                        for a in st.session_state.assignments:
                            if a["assignment_id"] == asgn["assignment_id"]: a["check_in_time"] = datetime.now().strftime("%H:%M:%S")
                            
                        log_audit(f"{vol['name']} checked in to task #{task['id']}")
                        st.rerun()
                        
                elif task["status"] == "In Progress":
                    st.info(f"⏱ Checked in at {asgn['check_in_time']}")
                    
                    if st.button("🔴 Check Out & Complete", key=f"co_{task['id']}", type="primary"):
                        now_  = datetime.now()
                        cin   = datetime.strptime(asgn["check_in_time"], "%H:%M:%S").replace(year=now_.year, month=now_.month, day=now_.day)
                        hrs   = max(round((now_ - cin).total_seconds() / 3600, 2), 0)
                        
                        # Demo override: If they click too fast, give them the minimum duration
                        if hrs < 0.1: hrs = task["duration"] 
                        
                        # Mutate all states
                        for t in st.session_state.tasks:
                            if t["id"] == task["id"]: t["status"] = "Completed"
                            
                        for a in st.session_state.assignments:
                            if a["assignment_id"] == asgn["assignment_id"]:
                                a["check_out_time"] = now_.strftime("%H:%M:%S")
                                a["hours_worked"]   = hrs
                                
                        for v in st.session_state.volunteers:
                            if v["id"] == vol["id"]: v["total_hours"] += hrs
                        
                        log_audit(f"{vol['name']} completed task #{task['id']}. Logged {hrs}h.")
                        st.success(f"✅ Task Completed! +{hrs}h added to your profile.")
                        st.rerun()

    with right:
        sec("ASSIGNMENT HISTORY")
        if my_asgns:
            rows = []
            for a in my_asgns:
                t = next((t for t in st.session_state.tasks if t["id"]==a["task_id"]), {})
                rows.append({
                    "Task": t.get("description","?")[:36],
                    "Status": t.get("status", ""),
                    "Check In":  a.get("check_in_time") or "—",
                    "Check Out": a.get("check_out_time") or "—",
                    "Hours": a.get("hours_worked", 0)
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
# FR7, FR8, FR9 — Adoption Processing
# ══════════════════════════════════════════════════════════
def adoption_page():
    st.markdown("<h1>🏠 Adoption Processing</h1>", unsafe_allow_html=True)
    
    now = datetime.now()
    animals = st.session_state.animals
    apps = st.session_state.applications

    tab1, tab2, tab3 = st.tabs(["📝 New Application", "⏰ Review Queue", "✅ Final Decisions"])

    with tab1:
        # Only medically cleared animals can be applied for
        available = [a for a in animals if a["status"] == "Available"]
        
        if not available: 
            st.warning("No animals are currently 'Available'. Check back after vet evaluations.")
        else:
            left, right = st.columns([1, 1])
            with left:
                sec("SUBMIT APPLICATION")
                with st.form("app_form", clear_on_submit=True):
                    opts   = {animal_label(a): a for a in available}
                    animal = opts[st.selectbox("Select Animal", list(opts.keys()))]
                    name   = st.text_input("Adopter Full Name")
                    
                    if st.form_submit_button("📬 Submit Application", use_container_width=True, type="primary"):
                        if name.strip():
                            new_id = max((a["app_id"] for a in apps), default=400) + 1
                            st.session_state.applications.append({
                                "app_id": new_id, "animal_id": animal["id"], "adopter_name": name.strip(),
                                "application_date": now, "review_date": None, "status": "Pending"
                            })
                            
                            # STATE MUTATION: Animal is no longer just "Available"
                            for anim in st.session_state.animals:
                                if anim["id"] == animal["id"]:
                                    anim["status"] = "Adoption Pending"
                                    break
                                    
                            log_audit(f"App #{new_id} submitted for Animal #{animal['id']}.")
                            st.success("✅ Application submitted.")
                            st.rerun()

            with right:
                sec("AVAILABLE ANIMALS")
                for a in available:
                    # FIX: Safely wrap text in dark color so it doesn't get hidden by Streamlit base theme
                    st.markdown(
                        f"""<div class='info-card'>
                            <div style='font-weight:600;color:#1E2B25; font-size:1.05rem;'>{animal_label(a)}</div>
                            <div style='color:#728A7E;font-size:0.85rem;margin-top:6px'>{a['age_months']}mo &nbsp;·&nbsp; {a['weight_kg']}kg</div>
                        </div>""", 
                        unsafe_allow_html=True
                    )

    with tab2:
        pending = [a for a in apps if a["status"] == "Pending"]
        if not pending: 
            st.success("✅ All applications reviewed.")
        
        for app in pending:
            elapsed_h = (now - app["application_date"]).total_seconds() / 3600
            animal    = next((a for a in animals if a["id"] == app["animal_id"]), {})
            
            label = f"{'🚨' if elapsed_h>=48 else '⏳'} App #{app['app_id']} — {app['adopter_name']} → {animal.get('breed','?')}"
            
            with st.expander(label):
                st.markdown(f"**Submitted:** {app['application_date'].strftime('%d %b %H:%M')}")
                if elapsed_h >= 48: 
                    st.error(f"🚨 Overdue by {elapsed_h-48:.0f}h")
                else: 
                    st.info(f"⏳ {48 - elapsed_h:.1f}h remaining")

    with tab3:
        pending = [a for a in apps if a["status"] == "Pending"]
        if not pending: 
            st.success("✅ No applications awaiting a decision.")
            
        for app in pending:
            animal = next((a for a in animals if a["id"] == app["animal_id"]), {})
            st.markdown(f"<div class='info-card'><h4 style='color:#E07A5F !important;'>App #{app['app_id']} — {app['adopter_name']}</h4><p style='color:#1E2B25 !important;'>Animal: <strong>{animal_label(animal) if animal else '—'}</strong></p></div>", unsafe_allow_html=True)
            
            c1, c2, _ = st.columns([1, 1, 3])
            
            if c1.button("✅ Approve", key=f"appr_{app['app_id']}", type="primary"):
                # 1. Update Application Status
                for a in st.session_state.applications:
                    if a["app_id"] == app["app_id"]: 
                        a["status"] = "Approved"
                        a["review_date"] = now
                
                # 2. Update Animal Status
                for anim in st.session_state.animals:
                    if anim["id"] == animal["id"]:
                        anim["status"] = "Adopted"
                        
                # 3. Create Ledger Record
                st.session_state.adoptions.append({
                    "adoption_id": len(st.session_state.adoptions)+500, 
                    "application_id": app["app_id"], 
                    "animal_id": animal["id"], 
                    "adoption_date": now.date()
                })
                
                # 4. Conflict Resolution (Reject other apps for same animal)
                for a in st.session_state.applications:
                    if a["animal_id"] == animal["id"] and a["status"] == "Pending" and a["app_id"] != app["app_id"]:
                        a["status"] = "Auto-Rejected (Adopted)"
                
                log_audit(f"App #{app['app_id']} APPROVED. Animal #{animal['id']} Adopted!")
                st.balloons()
                st.rerun() # FORCE DASHBOARD UPDATE
                
            if c2.button("❌ Reject", key=f"rej_{app['app_id']}"):
                
                # Update App status
                for a in st.session_state.applications:
                    if a["app_id"] == app["app_id"]:
                        a["status"] = "Rejected"
                        a["review_date"] = now
                
                # Check if there are ANY OTHER pending apps for this animal
                other_p = [a for a in st.session_state.applications if a["animal_id"] == animal["id"] and a["status"] == "Pending"]
                
                # If no other apps are pending, the animal goes back to Available
                if len(other_p) == 0:
                    for anim in st.session_state.animals:
                        if anim["id"] == animal["id"]:
                            anim["status"] = "Available"
                
                log_audit(f"App #{app['app_id']} manually rejected.")
                st.rerun() # FORCE DASHBOARD UPDATE
            
            st.markdown("<hr style='border-color:#F0E6DF;'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# FR10 — Manager Reports
# ══════════════════════════════════════════════════════════
def reports_page():
    st.markdown("<h1>📊 Manager Reports</h1>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🐾 Analytics", "💾 Data Exports", "🔐 System Audit"])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            sec("INTAKE BY SPECIES")
            st.bar_chart(pd.Series([a["species"] for a in st.session_state.animals]).value_counts(), color="#81B29A")
        with c2:
            sec("STATUS DISTRIBUTION")
            st.bar_chart(pd.Series([a["status"] for a in st.session_state.animals]).value_counts(), color="#E07A5F")

    with t2:
        sec("EXPORT DATA TO CSV")
        st.download_button("💾 Download Animals DB", data=pd.DataFrame(st.session_state.animals).to_csv(index=False), file_name="animals.csv", mime="text/csv")
        st.download_button("💾 Download Volunteers DB", data=pd.DataFrame(st.session_state.volunteers).to_csv(index=False), file_name="volunteers.csv", mime="text/csv")
        st.download_button("💾 Download Applications DB", data=pd.DataFrame(st.session_state.applications).to_csv(index=False), file_name="applications.csv", mime="text/csv")

    with t3:
        sec("SECURE SYSTEM AUDIT TRAIL")
        if st.session_state.audit_log:
            df_log = pd.DataFrame(st.session_state.audit_log)
            st.dataframe(df_log.iloc[::-1], use_container_width=True, hide_index=True) # Show newest first
        else:
            st.info("No system events logged yet.")


# ══════════════════════════════════════════════════════════
# SIDEBAR + MAIN
# ══════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in_user:
        login_page()
        return

    user = st.session_state.logged_in_user
    role = user["role"]

    with st.sidebar:
        st.markdown(f"<div style='text-align:center; padding:10px;'><h3>👤 {user['full_name']}</h3><p>{role}</p></div>", unsafe_allow_html=True)
        
        nav = ["🏠  Dashboard"]
        if role in ["Veterinarian","Manager"]:          nav += ["📝  Animal Intake","🩺  Medical Records"]
        if role in ["Volunteer Coordinator","Manager"]: nav += ["🙋  Volunteer Registry","📋  Task Management"]
        if role == "Volunteer":                         nav.append("✅  Attendance")
        if role in ["Adoption Counselor","Manager"]:    nav.append("🏠  Adoption Flow")
        if role == "Manager":                           nav.append("📊  Reports")

        choice = st.radio("nav", nav, label_visibility="collapsed")
        
        if st.button("Sign Out", use_container_width=True):
            log_audit("Logged out of the system.")
            st.session_state.logged_in_user = None
            st.rerun()

    page = choice.split("  ", 1)[-1].strip()
    
    if page == "Dashboard":            dashboard_page()
    elif page == "Animal Intake":      animal_intake_page()
    elif page == "Medical Records":    medical_page()
    elif page == "Volunteer Registry": volunteer_registration_page()
    elif page == "Task Management":    task_management_page()
    elif page == "Attendance":         volunteer_checkin_page()
    elif page == "Adoption Flow":      adoption_page()
    elif page == "Reports":            reports_page()

if __name__ == "__main__":
    main()