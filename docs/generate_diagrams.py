import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color palette - Academic Slate & Navy
    c_user = "#1E293B"
    c_fe = "#2563EB"
    c_be = "#0D9488"
    c_nlp = "#7C3AED"
    c_svc = "#0284C7"
    c_db = "#D97706"
    c_bg = "#F8FAFC"
    c_box = "#FFFFFF"

    # Title
    ax.text(50, 97, "MCA Academic Assistant - System Architecture", fontsize=15, fontweight='bold', ha='center', color='#0F172A', fontfamily='sans-serif')

    # User Tier
    rect_user = patches.FancyBboxPatch((15, 87), 70, 7, boxstyle="round,pad=0.5", ec=c_user, fc="#F1F5F9", lw=1.5)
    ax.add_patch(rect_user)
    ax.text(50, 90.5, "User Tier: Student Web Browser (Desktop / Mobile)", fontsize=10.5, fontweight='bold', ha='center', color=c_user)

    # Arrow User -> Frontend
    ax.annotate("", xy=(50, 81), xytext=(50, 87), arrowprops=dict(arrowstyle="->", lw=1.5, color="#475569"))

    # Presentation Tier
    rect_fe = patches.FancyBboxPatch((10, 68), 80, 13, boxstyle="round,pad=0.5", ec=c_fe, fc="#EFF6FF", lw=1.5)
    ax.add_patch(rect_fe)
    ax.text(50, 78.5, "Presentation Tier: Next.js 16 (React 19 + TypeScript + Tailwind CSS)", fontsize=11, fontweight='bold', ha='center', color=c_fe)
    
    # Next.js components
    fe_boxes = [("Chatbot Page (/)", 13, 70), ("Timetable (/timetable)", 33, 70), ("Calendar (/calendar)", 54, 70), ("Subjects (/subjects)", 73, 70)]
    for title, x, y in fe_boxes:
        b = patches.FancyBboxPatch((x, y), 16, 6, boxstyle="round,pad=0.3", ec="#93C5FD", fc="#FFFFFF", lw=1)
        ax.add_patch(b)
        ax.text(x + 8, y + 3, title, fontsize=8, ha='center', va='center', color="#1E3A8A", fontweight='semibold')

    # Arrow Frontend -> Backend (REST API / HTTP)
    ax.annotate("", xy=(50, 60), xytext=(50, 68), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#0284C7"))
    ax.text(51.5, 64, "HTTP REST API / JSON (/api/chat, /api/timetable, /api/calendar, /api/subjects)", fontsize=8, ha='left', va='center', color="#0369A1", fontweight='bold')

    # Backend Tier
    rect_be = patches.FancyBboxPatch((10, 24), 80, 36, boxstyle="round,pad=0.5", ec=c_be, fc="#F0FDFA", lw=1.5)
    ax.add_patch(rect_be)
    ax.text(50, 57.5, "Application Tier: Python FastAPI Backend (Uvicorn ASGI + Pydantic v2)", fontsize=11, fontweight='bold', ha='center', color=c_be)

    # Inside Backend: API Routers
    rect_routers = patches.FancyBboxPatch((13, 49), 74, 6.5, boxstyle="round,pad=0.3", ec="#5EEAD4", fc="#FFFFFF", lw=1)
    ax.add_patch(rect_routers)
    ax.text(50, 52.2, "API Routers: chat.py | timetable.py | calendar.py | subjects.py | health", fontsize=8.5, ha='center', color="#115E59", fontweight='bold')

    # Inside Backend: NLP Engine
    rect_nlp = patches.FancyBboxPatch((13, 39), 74, 8, boxstyle="round,pad=0.3", ec=c_nlp, fc="#FAF5FF", lw=1.2)
    ax.add_patch(rect_nlp)
    ax.text(50, 44.5, "Rule-Based Natural Language Processing (NLP) Engine (nlp.py)", fontsize=9.5, fontweight='bold', ha='center', color=c_nlp)
    ax.text(50, 41, "Query Normalization (clean_text)  •  Entity Extractor (Regex + Aliases)  •  Intent Classifier (20 Intents)", fontsize=7.5, ha='center', color="#581C87")

    # Inside Backend: Service & ORM Layer
    rect_svc = patches.FancyBboxPatch((13, 26), 74, 10.5, boxstyle="round,pad=0.3", ec=c_svc, fc="#F0F9FF", lw=1)
    ax.add_patch(rect_svc)
    ax.text(50, 34, "Service & Business Logic Layer (chatbot.py, timetable_service.py, calendar_service.py)", fontsize=9, fontweight='bold', ha='center', color=c_svc)
    ax.text(50, 29, "SQLAlchemy 2.0 ORM Engine  •  Declarative Models (Subject, Timetable, CalendarEvent)", fontsize=8, ha='center', color="#0369A1")

    # Arrow Backend -> Database
    ax.annotate("", xy=(50, 17), xytext=(50, 24), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#D97706"))

    # Database Tier
    rect_db = patches.FancyBboxPatch((15, 3), 70, 14, boxstyle="round,pad=0.5", ec=c_db, fc="#FFFBEB", lw=1.5)
    ax.add_patch(rect_db)
    ax.text(50, 14.5, "Persistence Tier: SQLite 3 Database (college_academic.db)", fontsize=11, fontweight='bold', ha='center', color=c_db)

    # Tables inside DB
    tbl_boxes = [("subjects", 20, 5.5, "9 Rows\n(Course Data)"), 
                 ("timetable", 42, 5.5, "39 Rows\n(Days I-VI)"), 
                 ("calendar_events", 64, 5.5, "61 Rows\n(2026-2027)")]
    for t_name, x, y, subtext in tbl_boxes:
        tb = patches.FancyBboxPatch((x, y), 17, 7, boxstyle="round,pad=0.3", ec="#FCD34D", fc="#FFFFFF", lw=1)
        ax.add_patch(tb)
        ax.text(x + 8.5, y + 4.8, t_name, fontsize=8.5, fontweight='bold', ha='center', color="#92400E")
        ax.text(x + 8.5, y + 2, subtext, fontsize=7, ha='center', color="#78350F")

    plt.tight_layout()
    plt.savefig("docs/figures/system_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Architecture diagram created.")


def create_system_workflow():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "MCA Academic Assistant - Query Processing Workflow", fontsize=15, fontweight='bold', ha='center', color='#0F172A')

    steps = [
        ("Step 1: User Query Input", "Student enters question in Next.js web interface\n(e.g., 'When is AI on Day III?')", "#1E293B", "#F1F5F9", 86),
        ("Step 2: Frontend HTTP Dispatch", "Client invokes sendChatMessage() sending JSON payload\nPOST /api/chat with message string", "#2563EB", "#EFF6FF", 73),
        ("Step 3: FastAPI Routing & Validation", "FastAPI receives request; Pydantic validates ChatRequest schema;\ndb session injected via Depends(get_db)", "#0D9488", "#F0FDFA", 60),
        ("Step 4: NLP Preprocessing & Normalization", "clean_text() normalizes case, removes punctuation (? ! .), collapses whitespace", "#7C3AED", "#FAF5FF", 47),
        ("Step 5: Entity Extraction & Intent Classification", "extract_entities() resolves day='Day III', subject='AI';\ndetect_intent() maps query to 'subject_schedule'", "#9333EA", "#FDF4FF", 34),
        ("Step 6: Service Dispatch & Database Retrieval", "chatbot.py calls get_subject_timetable(db, 'AI');\nSQLAlchemy executes filtered SQL query against SQLite", "#0284C7", "#F0F9FF", 21),
        ("Step 7: Response Formatting & UI Display", "Chatbot constructs answer with source attribution pill;\nNext.js displays bubble: 'AI is scheduled on Day III from 3:00 PM to 4:00 PM.'", "#059669", "#ECFDF5", 8),
    ]

    for title, desc, ec, fc, y in steps:
        box = patches.FancyBboxPatch((15, y), 70, 9.5, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.4)
        ax.add_patch(box)
        ax.text(50, y + 6.8, title, fontsize=10, fontweight='bold', ha='center', color=ec)
        ax.text(50, y + 2.8, desc, fontsize=8, ha='center', color="#334155")

        if y > 10:
            ax.annotate("", xy=(50, y - 3.5), xytext=(50, y), arrowprops=dict(arrowstyle="->", lw=1.6, color="#64748B"))

    plt.tight_layout()
    plt.savefig("docs/figures/system_workflow.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Workflow diagram created.")


def create_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "SQLite Database Entity-Relationship (ER) Diagram", fontsize=15, fontweight='bold', ha='center', color='#0F172A')

    # Subject Table Box
    box_sub = patches.FancyBboxPatch((6, 38), 38, 50, boxstyle="round,pad=0.4", ec="#2563EB", fc="#FFFFFF", lw=1.8)
    ax.add_patch(box_sub)
    # Header
    hdr_sub = patches.Rectangle((6, 81), 38, 7, ec="#2563EB", fc="#2563EB")
    ax.add_patch(hdr_sub)
    ax.text(25, 84.5, "subjects", fontsize=11, fontweight='bold', ha='center', color="#FFFFFF")

    sub_cols = [
        ("id", "INTEGER (PK, AUTOINCREMENT)"),
        ("code", "VARCHAR(50) (UNIQUE, NOT NULL)"),
        ("name", "VARCHAR(150) (NOT NULL)"),
        ("description", "TEXT (NULLABLE)"),
        ("class_type", "VARCHAR(50) (NOT NULL)"),
        ("faculty", "VARCHAR(200) (NULLABLE)")
    ]
    curr_y = 75
    for col, ctype in sub_cols:
        ax.text(8, curr_y, col, fontsize=8.5, fontweight='bold', color="#1E293B")
        ax.text(23, curr_y, ctype, fontsize=7.5, color="#64748B")
        curr_y -= 6.5

    # Timetable Table Box
    box_tt = patches.FancyBboxPatch((56, 26), 38, 62, boxstyle="round,pad=0.4", ec="#0D9488", fc="#FFFFFF", lw=1.8)
    ax.add_patch(box_tt)
    # Header
    hdr_tt = patches.Rectangle((56, 81), 38, 7, ec="#0D9488", fc="#0D9488")
    ax.add_patch(hdr_tt)
    ax.text(75, 84.5, "timetable", fontsize=11, fontweight='bold', ha='center', color="#FFFFFF")

    tt_cols = [
        ("id", "INTEGER (PK, AUTOINCREMENT)"),
        ("day_order", "VARCHAR(20) (NOT NULL)"),
        ("start_time", "VARCHAR(20) (NOT NULL)"),
        ("end_time", "VARCHAR(20) (NOT NULL)"),
        ("subject", "VARCHAR(100) (NOT NULL)"),
        ("room", "VARCHAR(50) (NULLABLE)"),
        ("faculty", "VARCHAR(200) (NULLABLE)"),
        ("class_type", "VARCHAR(50) (NOT NULL)"),
        ("subject_id", "INTEGER (FK -> subjects.id)")
    ]
    curr_y = 75
    for col, ctype in tt_cols:
        ax.text(58, curr_y, col, fontsize=8.5, fontweight='bold', color="#1E293B")
        ax.text(71, curr_y, ctype, fontsize=7.2, color="#64748B")
        curr_y -= 5.5

    # Relationship line between subjects and timetable
    ax.annotate("", xy=(56, 32), xytext=(44, 75), arrowprops=dict(arrowstyle="<->", lw=2, color="#2563EB", connectionstyle="arc3,rad=-0.2"))
    ax.text(49, 58, "1 : N\n(One-to-Many)", fontsize=8.5, fontweight='bold', ha='center', color="#1D4ED8", bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec="#93C5FD"))

    # Calendar Events Table Box
    box_cal = patches.FancyBboxPatch((20, 2), 60, 20, boxstyle="round,pad=0.4", ec="#D97706", fc="#FFFFFF", lw=1.8)
    ax.add_patch(box_cal)
    # Header
    hdr_cal = patches.Rectangle((20, 16.5), 60, 5.5, ec="#D97706", fc="#D97706")
    ax.add_patch(hdr_cal)
    ax.text(50, 19.2, "calendar_events", fontsize=11, fontweight='bold', ha='center', color="#FFFFFF")

    ax.text(23, 12, "id (INTEGER PK)  •  date (VARCHAR(20))  •  day (VARCHAR(20))  •  event (VARCHAR(250))", fontsize=8, fontweight='bold', color="#1E293B")
    ax.text(23, 6, "category (VARCHAR(100))  •  semester (VARCHAR(50))  •  is_holiday (BOOLEAN)  •  description (TEXT)", fontsize=8, color="#64748B")

    plt.tight_layout()
    plt.savefig("docs/figures/er_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("ER diagram created.")

if __name__ == "__main__":
    create_system_architecture()
    create_system_workflow()
    create_er_diagram()
