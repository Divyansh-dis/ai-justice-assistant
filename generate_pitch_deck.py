import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = os.path.abspath(r"C:\Users\divya\.gemini\antigravity\scratch\ai-justice-assistant\AI_Justice_Assistant_Presentation.pptx")

# Color Palette: Government of India / Ashoka Navy & Gold
NAVY_DARK = RGBColor(15, 32, 98)       # #0F2062
NAVY_DEEP = RGBColor(8, 18, 59)        # #08123B
GOLD = RGBColor(217, 119, 6)           # #D97706
GOLD_LIGHT = RGBColor(251, 191, 36)    # #FBBF24
WHITE = RGBColor(255, 255, 255)
SLATE_50 = RGBColor(248, 250, 252)
SLATE_200 = RGBColor(226, 232, 240)
SLATE_400 = RGBColor(148, 163, 184)
SLATE_700 = RGBColor(51, 65, 85)
SLATE_800 = RGBColor(30, 41, 59)
EMERALD = RGBColor(16, 185, 129)
SAFFRON = RGBColor(255, 153, 51)       # Tri-color saffron
GREEN = RGBColor(19, 136, 8)           # Tri-color green

prs = Presentation()
# Set widescreen 16:9 (13.33 x 7.5 inches)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="AI JUSTICE DEPARTMENT ASSISTANT"):
    # Tri-color top stripe
    stripe_w = prs.slide_width / 3
    s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, stripe_w, Inches(0.08))
    s1.fill.solid()
    s1.fill.fore_color.rgb = SAFFRON
    s1.line.fill.background()

    s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, stripe_w, 0, stripe_w, Inches(0.08))
    s2.fill.solid()
    s2.fill.fore_color.rgb = WHITE
    s2.line.fill.background()

    s3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, stripe_w * 2, 0, stripe_w, Inches(0.08))
    s3.fill.solid()
    s3.fill.fore_color.rgb = GREEN
    s3.line.fill.background()

    # Category pill / banner
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = GOLD_LIGHT
    p_cat.font.name = "Arial"

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Georgia"

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_card(slide, left, top, width, height, bg_color=SLATE_800, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, NAVY_DEEP)

# Decorative emblem bar
bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(3.8))
bar.fill.solid()
bar.fill.fore_color.rgb = GOLD
bar.line.fill.background()

# Title box
tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(4.0))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "REPUBLIC OF INDIA • PUBLIC STATUTES & REGULATIONS RAG"
p_sub.font.size = Pt(12)
p_sub.font.bold = True
p_sub.font.color.rgb = GOLD_LIGHT
p_sub.font.name = "Arial"

p_main = tf1.add_paragraph()
p_main.text = "AI Justice Department Assistant"
p_main.font.size = Pt(40)
p_main.font.bold = True
p_main.font.color.rgb = WHITE
p_main.font.name = "Georgia"

p_desc = tf1.add_paragraph()
p_desc.text = "Democratizing Statutory Legal Intelligence with Zero-Hallucination Retrieval\nOver Bharatiya Nyaya Sanhita (2023), Acts of Parliament & The Indian Constitution"
p_desc.font.size = Pt(16)
p_desc.font.color.rgb = SLATE_200
p_desc.font.name = "Calibri"

# Meta pill container
add_card(slide1, 1.2, 5.5, 10.9, 1.1, bg_color=SLATE_800, border_color=GOLD)
tb_meta = slide1.shapes.add_textbox(Inches(1.4), Inches(5.6), Inches(10.5), Inches(0.9))
tf_meta = tb_meta.text_frame
p_m = tf_meta.paragraphs[0]
p_m.text = "Core Tech Stack: React (Vite) • FastAPI • ChromaDB Vector DB • sentence-transformers • LangChain"
p_m.font.size = Pt(12)
p_m.font.bold = True
p_m.font.color.rgb = GOLD_LIGHT

p_m2 = tf_meta.add_paragraph()
p_m2.text = "Live Deployment: Verified Cloud Instance on Railway with Local Persistent Vector Store"
p_m2.font.size = Pt(11)
p_m2.font.color.rgb = SLATE_200

slide1.notes_slide.notes_text_frame.text = (
    "SPEECH (0:00 - 0:30):\n"
    "Respected jury, mentors, and audience: Article 39A of the Constitution of India mandates equal justice "
    "and free legal aid for every citizen. Yet today, for over 1.4 billion people, our laws remain locked "
    "behind dense terminology and inaccessible gazettes. Today, I present the AI Justice Department Assistant: "
    "an autonomous, government-grade Legal RAG system that provides accurate, instant, and strictly "
    "non-hallucinatory statutory answers citing exact Acts, Sections, and Pages."
)

# ==============================================================================
# SLIDE 2: THE PROBLEM STATEMENT
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, NAVY_DARK)
add_header(slide2, "The Crisis of Legal Accessibility & The AI Hallucination Trap", "PROBLEM LANDSCAPE")

# 3 Column Cards
card_w = 3.65
card_h = 5.0
top_pos = 1.7

# Card 1: Court Pendency
add_card(slide2, 0.8, top_pos, card_w, card_h, bg_color=SLATE_800, border_color=RGBColor(239, 68, 68))
tb_c1 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(3.25), Inches(4.5))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True
p = tf_c1.paragraphs[0]
p.text = "5 CRORE+ PENDING CASES"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(248, 113, 113)

bullets_c1 = [
    "Over 50 million cases clogged in District, High Courts, and Supreme Court.",
    "Common citizens and MSMEs cannot afford ₹50,000+ legal retainer fees.",
    "Ignorance of procedural timelines (e.g. RTI 30-day limits) causes loss of rights."
]
for b in bullets_c1:
    p = tf_c1.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_200

# Card 2: 2024 Legal Overhaul
add_card(slide2, 4.8, top_pos, card_w, card_h, bg_color=SLATE_800, border_color=GOLD)
tb_c2 = slide2.shapes.add_textbox(Inches(5.0), Inches(1.9), Inches(3.25), Inches(4.5))
tf_c2 = tb_c2.text_frame
tf_c2.word_wrap = True
p = tf_c2.paragraphs[0]
p.text = "HISTORIC 2024 CODE SHIFT"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = GOLD_LIGHT

bullets_c2 = [
    "Colonial IPC (1860) replaced by Bharatiya Nyaya Sanhita (BNS 2023).",
    "Radical restructuring: Section 302 (Murder) is now Section 103; Theft is Section 303.",
    "Police, lawyers, and citizens are struggling with transition across millions of FIRs."
]
for b in bullets_c2:
    p = tf_c2.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_200

# Card 3: The LLM Danger
add_card(slide2, 8.8, top_pos, card_w, card_h, bg_color=SLATE_800, border_color=RGBColor(59, 130, 246))
tb_c3 = slide2.shapes.add_textbox(Inches(9.0), Inches(1.9), Inches(3.25), Inches(4.5))
tf_c3 = tb_c3.text_frame
tf_c3.word_wrap = True
p = tf_c3.paragraphs[0]
p.text = "THE LLM HALLUCINATION RISK"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(96, 165, 250)

bullets_c3 = [
    "Standard LLMs (ChatGPT) invent fake sections, repealed laws, and incorrect fines.",
    "Probabilistic text generation without grounding is lethal in legal matters.",
    "Need: A system that REFUSES to guess and answers ONLY from verified statutory text."
]
for b in bullets_c3:
    p = tf_c3.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_200

slide2.notes_slide.notes_text_frame.text = (
    "SPEECH (0:30 - 1:45):\n"
    "Why did we build this? Indian courts face an unprecedented 5 crore pending cases. In 2024, Parliament enacted "
    "India's biggest criminal law overhaul in a century, replacing the 1860 IPC with Bharatiya Nyaya Sanhita 2023. "
    "Why not use ChatGPT? Standard LLMs hallucinate fake sections and repealed British laws. In a court of law, "
    "a hallucination isn't just an error—it can cost someone their freedom."
)

# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE & LEGAL RAG ENGINE
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, NAVY_DARK)
add_header(slide3, "System Architecture: How We Eliminate AI Hallucinations", "TECHNICAL ARCHITECTURE")

# Top Workflow Flowchart Card
add_card(slide3, 0.8, 1.7, 11.7, 2.2, bg_color=SLATE_800, border_color=GOLD)
tb_flow = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.0))
tf_flow = tb_flow.text_frame
tf_flow.word_wrap = True
p = tf_flow.paragraphs[0]
p.text = "RELIABLE RETRIEVAL-AUGMENTED GENERATION (RAG) PIPELINE"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GOLD_LIGHT

pipeline_steps = (
    "1. Ingestion: Scan ./legal_data PDF Gazettes (BNS, IT Act, RTI Act, DPDP Act, Constitution)\n"
    "2. Chunking: RecursiveCharacterTextSplitter (Size: 1000, Overlap: 200) anchored on Section & Article headers\n"
    "3. Vectorization: ONNX-compiled all-MiniLM-L6-v2 (384-dimensional dense vectors) stored in local ChromaDB\n"
    "4. Search & Guardrails: Cosine similarity search (Top-4) + Strict Anti-Hallucination Legal System Prompt"
)
p2 = tf_flow.add_paragraph()
p2.text = pipeline_steps
p2.font.size = Pt(12)
p2.font.color.rgb = SLATE_50

# Bottom 2 Feature Breakdown Cards
add_card(slide3, 0.8, 4.2, 5.7, 2.7, bg_color=SLATE_800)
tb_b1 = slide3.shapes.add_textbox(Inches(1.0), Inches(4.35), Inches(5.3), Inches(2.4))
tf_b1 = tb_b1.text_frame
tf_b1.word_wrap = True
p = tf_b1.paragraphs[0]
p.text = "⚡ Zero-Latency Local Vector Storage"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = EMERALD

p = tf_b1.add_paragraph()
p.text = "• Persistent ChromaDB client running entirely locally on-disk.\n• No external embedding API costs or rate-limiting delays.\n• Semantic metadata preserves document title, section tag, and page number with every vector chunk."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

add_card(slide3, 6.8, 4.2, 5.7, 2.7, bg_color=SLATE_800)
tb_b2 = slide3.shapes.add_textbox(Inches(7.0), Inches(4.35), Inches(5.3), Inches(2.4))
tf_b2 = tb_b2.text_frame
tf_b2.word_wrap = True
p = tf_b2.paragraphs[0]
p.text = "🛡️ Strict Anti-Hallucination Directives"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(96, 165, 250)

p = tf_b2.add_paragraph()
p.text = "• System mandate: Answer ONLY from retrieved statutory chunks.\n• Explicit Refusal: If statute does not contain the answer, system declares insufficient information.\n• Exact Citations: Never generates an assertion without Act, Section & Page."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

slide3.notes_slide.notes_text_frame.text = (
    "SPEECH (1:45 - 3:30):\n"
    "To solve this, we built an end-to-end Legal RAG Pipeline. We scan official PDF gazettes and chunk them with "
    "LangChain's RecursiveCharacterTextSplitter structured around Section boundaries. We embed using ONNX "
    "all-MiniLM-L6-v2 in ChromaDB. When a citizen asks a question, we retrieve the top 4 matching provisions. "
    "Our generation engine is under strict directives: if the statute lacks the answer, it declines rather than "
    "fabricates. Every claim is anchored to an exact section and page."
)

# ==============================================================================
# SLIDE 4: SPECIAL FEATURES & UI INNOVATION
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, NAVY_DARK)
add_header(slide4, "Core Innovation: Built for Legal Transparency & Verification", "SPECIAL FEATURES")

grid_w = 5.7
grid_h = 2.45

# Grid 1: Source Citation Drawers
add_card(slide4, 0.8, 1.7, grid_w, grid_h, bg_color=SLATE_800, border_color=GOLD)
tb_g1 = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(2.2))
tf_g1 = tb_g1.text_frame
tf_g1.word_wrap = True
p = tf_g1.paragraphs[0]
p.text = "📂 Expandable Source Citation Drawers"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GOLD_LIGHT
p = tf_g1.add_paragraph()
p.text = "• Expandable card beneath EVERY answer.\n• Displays Act Name, Section Badge, Page Number, and Match %.\n• One-click drawer expansion shows the raw verbatim clause from the official gazette."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

# Grid 2: Legal Document Vault
add_card(slide4, 6.8, 1.7, grid_w, grid_h, bg_color=SLATE_800, border_color=EMERALD)
tb_g2 = slide4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(2.2))
tf_g2 = tb_g2.text_frame
tf_g2.word_wrap = True
p = tf_g2.paragraphs[0]
p.text = "🏛️ Dynamic Document Vault & Live Ingestion"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = EMERALD
p = tf_g2.add_paragraph()
p.text = "• Admin/User view of all vectorized Indian statutes.\n• Instant PDF Statute Uploader: Upload any new Act of Parliament or Gazette Notification and vectorize it in seconds.\n• Visual chunk counter and file size auditor."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

# Grid 3: Bookmarks & Research
add_card(slide4, 0.8, 4.45, grid_w, grid_h, bg_color=SLATE_800, border_color=RGBColor(96, 165, 250))
tb_g3 = slide4.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(5.3), Inches(2.2))
tf_g3 = tb_g3.text_frame
tf_g3.word_wrap = True
p = tf_g3.paragraphs[0]
p.text = "📌 Saved Legal Provisions & Annotations"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(96, 165, 250)
p = tf_g3.add_paragraph()
p.text = "• Bookmark answers for rapid reference during court hearings or drafting.\n• Add customized judicial notes to any statutory provision.\n• Dedicated drawer to search and manage saved citations."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

# Grid 4: Export Dossiers
add_card(slide4, 6.8, 4.45, grid_w, grid_h, bg_color=SLATE_800, border_color=RGBColor(244, 63, 94))
tb_g4 = slide4.shapes.add_textbox(Inches(7.0), Inches(4.55), Inches(5.3), Inches(2.2))
tf_g4 = tb_g4.text_frame
tf_g4.word_wrap = True
p = tf_g4.paragraphs[0]
p.text = "📄 Court-Ready Export: Markdown & PDF"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(251, 113, 133)
p = tf_g4.add_paragraph()
p.text = "• Download clean Markdown (.md) transcripts for Obsidian, Notion or research briefs.\n• Official Print-to-PDF formatting complete with timestamps, inquiry history, and verified statutory citations."
p.font.size = Pt(11)
p.font.color.rgb = SLATE_200

slide4.notes_slide.notes_text_frame.text = (
    "SPEECH (3:30 - 5:00):\n"
    "What makes this a production-grade tool? Radical transparency through expandable citation drawers. Users don't "
    "take the AI's word for it; they can click and read the raw gazette clause. Our Document Vault allows instant upload "
    "and vectorization of new Acts. Researchers can bookmark provisions with case notes and export complete dossiers "
    "as Markdown or print-ready PDFs."
)

# ==============================================================================
# SLIDE 5: LIVE DEMO & STATUTORY COVERAGE
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, NAVY_DARK)
add_header(slide5, "Statutory Grounding: Pre-Loaded Indian Enactments", "LIVE DEMO & CAPABILITIES")

statutes = [
    ("Bharatiya Nyaya Sanhita (BNS 2023)", "Act No. 45 of 2023", "Section 103 (Murder), Section 303 (Theft & Community Service), Section 115 (Hurt)"),
    ("Information Technology Act (IT Act 2000)", "Act No. 21 of 2000", "Section 43 (Computer Damage), Section 66C (Identity Theft), Section 79 (Intermediary Safe Harbour)"),
    ("Right to Information Act (RTI Act 2005)", "Act No. 22 of 2005", "Section 3 (Citizen Right), Section 7 (30-day/48-hr timeline), Section 20 (Rs 250/day penalty)"),
    ("Constitution of India - Fundamental Rights", "Articles 12 to 35", "Article 14 (Equality), Article 19 (Freedoms), Article 20 (Self-incrimination), Article 21 (Life & Privacy)"),
    ("Digital Personal Data Protection Act (DPDP 2023)", "Act No. 22 of 2023", "Section 4 (Grounds), Section 6 (Consent notice), Section 33 (Penalties up to Rs 250 Crore)")
]

top_offset = 1.7
for name, act_no, provisions in statutes:
    add_card(slide5, 0.8, top_offset, 11.7, 0.95, bg_color=SLATE_800)
    tb = slide5.shapes.add_textbox(Inches(1.0), Inches(top_offset + 0.05), Inches(11.3), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{name} • {act_no}"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GOLD_LIGHT
    
    p2 = tf.add_paragraph()
    p2.text = f"Key Ingested Provisions: {provisions}"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = SLATE_200
    top_offset += 1.05

slide5.notes_slide.notes_text_frame.text = (
    "SPEECH (5:00 - 7:30 - Live Demo transition):\n"
    "Switching to our live deployment: Let's test a real question under the new criminal code: 'What are the punishments "
    "for theft under BNS 2023?' The system immediately identifies Section 303, explains the imprisonment, and highlights "
    "the new community service provision for petty theft. Look at the citation drawer: it provides the verbatim clause "
    "from Page 1 of the official gazette with a 70% match score."
)

# ==============================================================================
# SLIDE 6: REAL-WORLD SOCIO-ECONOMIC IMPACT
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, NAVY_DARK)
add_header(slide6, "Real-World Impact: Democratizing Access to Justice", "VALUE PROPOSITION")

impact_cols = [
    ("CITIZENS & MSMEs", "Instant Legal Literacy", [
        "Enforces RTI rights with exact timelines & penalties.",
        "Understands cyber rights & online identity theft recourse.",
        "Zero legal fees for first-line statutory understanding."
    ], GOLD_LIGHT),
    ("LAW ENFORCEMENT", "FIR Accuracy & Speed", [
        "Instant transition bridge between old IPC and new BNS.",
        "Accurate section application prevents procedural quashing.",
        "Fast reference during late-night station filings."
    ], EMERALD),
    ("ADVOCATES & COURTS", "80% Time Reduction", [
        "Reduces manual searching across hundreds of statute pages.",
        "Exportable dossiers for instant client consultation.",
        "Reduces frivolous litigation by clarifying law upfront."
    ], RGBColor(96, 165, 250))
]

col_w = 3.65
for idx, (title, sub, bullets, color) in enumerate(impact_cols):
    c_left = 0.8 + idx * 4.0
    add_card(slide6, c_left, 1.7, col_w, 5.0, bg_color=SLATE_800, border_color=color)
    tb = slide6.shapes.add_textbox(Inches(c_left + 0.2), Inches(1.9), Inches(col_w - 0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = SLATE_400
    
    for b in bullets:
        p_b = tf.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = SLATE_200

slide6.notes_slide.notes_text_frame.text = (
    "SPEECH (7:30 - 8:45):\n"
    "What is the tangible impact? For police officers, it prevents procedural dismissal of FIRs by applying correct "
    "BNS sections. For citizens, it turns obscure legal rights into actionable knowledge—like knowing an RTI officer "
    "can be penalized Rs 250 a day under Section 20 for delays. For advocates, it reduces routine statutory search time by 80%."
)

# ==============================================================================
# SLIDE 7: SCALABILITY & FUTURE ROADMAP
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, NAVY_DARK)
add_header(slide7, "Future Roadmap: Scalable Public Digital Infrastructure", "ENGINEERING VISION")

roadmap = [
    ("PHASE 1: INDIC VOICE RAG (BHASHINI)", "Integration with Govt. of India's Bhashini AI to support voice legal inquiries across 22 scheduled Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi) for rural citizens."),
    ("PHASE 2: JUDICIAL PRECEDENT VAULT", "Indexing landmark judgments of the Supreme Court of India and High Courts from eCourts repositories to link statutory sections with leading judicial case laws."),
    ("PHASE 3: CITIZEN WHATSAPP / TELEGRAM BOT", "Zero-barrier citizen access to legal queries via messaging channels, backed by the same anti-hallucination RAG backend."),
    ("PHASE 4: AUTOMATED LEGAL NOTICE DRAFTING", "Drafting structured RTI applications, consumer complaints, and legal notices with human-in-the-loop attorney verification.")
]

r_top = 1.7
for p_title, p_desc in roadmap:
    add_card(slide7, 0.8, r_top, 11.7, 1.15, bg_color=SLATE_800, border_color=GOLD)
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(r_top + 0.08), Inches(11.3), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = p_title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GOLD_LIGHT
    
    p2 = tf.add_paragraph()
    p2.text = p_desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = SLATE_200
    r_top += 1.3

slide7.notes_slide.notes_text_frame.text = (
    "SPEECH (8:45 - 9:30):\n"
    "Our future engineering roadmap has four pillars: Indic language voice queries through Bhashini integration, "
    "indexing Supreme Court landmark judgments from eCourts, WhatsApp bot integration for rural India, and "
    "automated drafting of legal notices with human-in-the-loop validation."
)

# ==============================================================================
# SLIDE 8: CONCLUSION & Q&A
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, NAVY_DEEP)

# Large quote card
add_card(slide8, 1.5, 1.8, 10.33, 3.8, bg_color=SLATE_800, border_color=GOLD)
tb_end = slide8.shapes.add_textbox(Inches(1.8), Inches(2.1), Inches(9.7), Inches(3.2))
tf_end = tb_end.text_frame
tf_end.word_wrap = True

p = tf_end.paragraphs[0]
p.text = '"JUSTICE DELAYED IS JUSTICE DENIED.\nJUSTICE OBSCURED IS JUSTICE DENIED."'
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = GOLD_LIGHT
p.font.name = "Georgia"
p.alignment = PP_ALIGN.CENTER

p2 = tf_end.add_paragraph()
p2.text = "\nAI Justice Department Assistant makes Indian law verifiable, transparent, and accessible to every citizen."
p2.font.size = Pt(14)
p2.font.color.rgb = WHITE
p2.alignment = PP_ALIGN.CENTER

p3 = tf_end.add_paragraph()
p3.text = "\nRepository: https://github.com/Divyansh-dis/ai-justice-assistant"
p3.font.size = Pt(12)
p3.font.color.rgb = SLATE_400
p3.alignment = PP_ALIGN.CENTER

tb_qa = slide8.shapes.add_textbox(Inches(1.5), Inches(5.9), Inches(10.33), Inches(0.8))
tf_qa = tb_qa.text_frame
p_qa = tf_qa.paragraphs[0]
p_qa.text = "Thank You! We are now open for Questions & Discussion."
p_qa.font.size = Pt(18)
p_qa.font.bold = True
p_qa.font.color.rgb = WHITE
p_qa.alignment = PP_ALIGN.CENTER

slide8.notes_slide.notes_text_frame.text = (
    "SPEECH (9:30 - 10:00):\n"
    "Ladies and gentlemen, the legal maxim says: 'Ignorance of the law is no excuse.' But in a modern democracy, "
    "ignorance of the law should never be the consequence of inaccessible systems. The AI Justice Department Assistant "
    "ensures that every citizen, lawyer, and student can access the laws of the Republic of India with total accuracy, "
    "zero hallucination, and complete transparency. Thank you very much. I am now open to your questions."
)

prs.save(OUTPUT_PPTX)
print(f"Presentation PPTX created successfully at: {OUTPUT_PPTX}")
