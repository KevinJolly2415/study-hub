import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_CREAM = RGBColor(253, 250, 244)
    BOOK_SPINE = RGBColor(38, 55, 75)       # Rich navy
    GOLD_ACCENT = RGBColor(196, 138, 38)    # Storybook gold
    GOLD_LIGHT = RGBColor(254, 248, 230)
    TERRACOTTA = RGBColor(198, 76, 52)      # Warm storybook red
    TERRA_LIGHT = RGBColor(253, 242, 239)
    SAGE_GREEN = RGBColor(56, 115, 82)      # Sage green
    SAGE_LIGHT = RGBColor(240, 248, 242)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 216, 196)  # Subtle book page border
    TEXT_DARK = RGBColor(35, 38, 45)        # Charcoal ink
    TEXT_MUTED = RGBColor(95, 100, 110)
    WHITE = RGBColor(255, 255, 255)
    BLUE_LIGHT = RGBColor(241, 246, 253)
    PURPLE_ACCENT = RGBColor(112, 66, 135)
    PURPLE_LIGHT = RGBColor(247, 242, 251)

    # 15 Slides
    slides = [prs.slides.add_slide(blank_layout) for _ in range(15)]

    def set_slide_background(slide, color=BG_CREAM):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, chapter_tag, title_text, category="LESSON 30: THE GRATEFUL GIRL"):
        # Header banner container
        header_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.7), Inches(0.4), Inches(11.933), Inches(0.85)
        )
        header_card.fill.solid()
        header_card.fill.fore_color.rgb = WHITE
        header_card.line.color.rgb = BORDER_COLOR
        header_card.line.width = Pt(1.5)

        # Left tag pill
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.85), Inches(0.55), Inches(2.5), Inches(0.55)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = BOOK_SPINE
        pill.line.color.rgb = BOOK_SPINE
        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_pill.paragraphs[0]
        p_pill.text = chapter_tag
        p_pill.font.name = "Georgia"
        p_pill.font.size = Pt(12)
        p_pill.font.bold = True
        p_pill.font.color.rgb = WHITE
        p_pill.alignment = PP_ALIGN.CENTER

        # Title text frame
        tb = slide.shapes.add_textbox(Inches(3.5), Inches(0.45), Inches(8.9), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.name = "Georgia"
        p1.font.size = Pt(19)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = category
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = GOLD_ACCENT

    def add_navbar(slide, current_idx):
        # Bottom navigation bar
        nav_y = Inches(6.8)
        nav_h = Inches(0.5)

        # Nav container
        bg = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.7), nav_y, Inches(11.933), nav_h
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = WHITE
        bg.line.color.rgb = BORDER_COLOR
        bg.line.width = Pt(1)

        # Buttons configuration
        buttons = [
            ("📖 Contents", 1, Inches(0.85), Inches(1.3)),
            ("⬅️ Prev", max(0, current_idx - 1), Inches(2.25), Inches(1.1)),
            ("➡️ Next", min(14, current_idx + 1), Inches(3.45), Inches(1.1)),
            ("📜 Memory Verse", 10, Inches(4.7), Inches(1.6)),
            ("🎵 Hymn Space", 11, Inches(6.4), Inches(1.5)),
            ("💡 Moral", 9, Inches(8.0), Inches(1.2)),
            ("❓ Q&A Quiz", 12, Inches(9.3), Inches(1.4)),
            ("🎭 Activity", 13, Inches(10.8), Inches(1.4)),
        ]

        for label, target_idx, btn_x, btn_w in buttons:
            btn = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                btn_x, nav_y + Inches(0.06), btn_w, Inches(0.38)
            )
            is_active = (target_idx == current_idx)
            btn.fill.solid()
            if is_active:
                btn.fill.fore_color.rgb = GOLD_LIGHT
                btn.line.color.rgb = GOLD_ACCENT
                btn.line.width = Pt(1.5)
            else:
                btn.fill.fore_color.rgb = BG_CREAM
                btn.line.color.rgb = BORDER_COLOR
                btn.line.width = Pt(1)

            btn.click_action.target_slide = slides[target_idx]
            tf = btn.text_frame
            tf.word_wrap = False
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = label
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = BOOK_SPINE if not is_active else TERRACOTTA
            run.hyperlink.target_slide = slides[target_idx]

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = slides[0]
    set_slide_background(s1, BG_CREAM)

    # Book border outer
    cover_card = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.0), Inches(0.6), Inches(11.333), Inches(6.3)
    )
    cover_card.fill.solid()
    cover_card.fill.fore_color.rgb = WHITE
    cover_card.line.color.rgb = GOLD_ACCENT
    cover_card.line.width = Pt(3)

    # Book Spine accent strip on left
    spine = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.0), Inches(0.6), Inches(0.6), Inches(6.3)
    )
    spine.fill.solid()
    spine.fill.fore_color.rgb = BOOK_SPINE
    spine.line.color.rgb = BOOK_SPINE

    # Title Banner / Ribbon
    ribbon = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2.2), Inches(1.1), Inches(9.5), Inches(0.6)
    )
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = GOLD_LIGHT
    ribbon.line.color.rgb = GOLD_ACCENT
    ribbon.line.width = Pt(1)
    tf_rib = ribbon.text_frame
    p_rib = tf_rib.paragraphs[0]
    p_rib.alignment = PP_ALIGN.CENTER
    p_rib.text = "✨ LESSON 30 • INTERACTIVE STORYBOOK PRESENTATION ✨"
    p_rib.font.name = "Georgia"
    p_rib.font.size = Pt(12)
    p_rib.font.bold = True
    p_rib.font.color.rgb = GOLD_ACCENT

    # Main Title Box
    title_box = s1.shapes.add_textbox(Inches(2.2), Inches(1.8), Inches(9.5), Inches(1.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.text = "The Grateful Girl"
    p_t1.font.name = "Georgia"
    p_t1.font.size = Pt(46)
    p_t1.font.bold = True
    p_t1.font.color.rgb = BOOK_SPINE

    p_t2 = tf_title.add_paragraph()
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.text = "A Heartwarming Journey of Prayer, Miracles, and Giving Thanks in Everything"
    p_t2.font.name = "Georgia"
    p_t2.font.size = Pt(15)
    p_t2.font.italic = True
    p_t2.font.color.rgb = TEXT_MUTED

    # Memory Verse Scroll Card
    verse_card = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2.5), Inches(3.6), Inches(8.9), Inches(1.2)
    )
    verse_card.fill.solid()
    verse_card.fill.fore_color.rgb = SAGE_LIGHT
    verse_card.line.color.rgb = SAGE_GREEN
    verse_card.line.width = Pt(2)
    tf_v = verse_card.text_frame
    tf_v.word_wrap = True
    p_v1 = tf_v.paragraphs[0]
    p_v1.alignment = PP_ALIGN.CENTER
    p_v1.text = "📖 GOLDEN MEMORY VERSE"
    p_v1.font.name = "Calibri"
    p_v1.font.size = Pt(11)
    p_v1.font.bold = True
    p_v1.font.color.rgb = SAGE_GREEN

    p_v2 = tf_v.add_paragraph()
    p_v2.alignment = PP_ALIGN.CENTER
    p_v2.text = "“In everything give thanks; for this is the will of God in Christ Jesus for you.”"
    p_v2.font.name = "Georgia"
    p_v2.font.size = Pt(15)
    p_v2.font.bold = True
    p_v2.font.color.rgb = TEXT_DARK

    p_v3 = tf_v.add_paragraph()
    p_v3.alignment = PP_ALIGN.CENTER
    p_v3.text = "— 1 Thessalonians 5:18 (Memory Verse Focus: 1 Thess. 5:18a)"
    p_v3.font.name = "Calibri"
    p_v3.font.size = Pt(11)
    p_v3.font.color.rgb = SAGE_GREEN

    # Interactive Feature Badges (Pills)
    features = [
        ("🌸 7 Story Chapters", Inches(2.2), Inches(5.1)),
        ("💡 Moral of the Story", Inches(4.2), Inches(5.1)),
        ("🎵 Hymn & Chords", Inches(6.3), Inches(5.1)),
        ("❓ Interactive Quiz", Inches(8.2), Inches(5.1)),
        ("🎭 Acting Game", Inches(10.1), Inches(5.1)),
    ]
    for text, bx, by in features:
        badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(1.8), Inches(0.42))
        badge.fill.solid()
        badge.fill.fore_color.rgb = BG_CREAM
        badge.line.color.rgb = BORDER_COLOR
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = text
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = BOOK_SPINE

    # Big "Open Storybook" Button
    start_btn = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(4.6), Inches(5.75), Inches(4.7), Inches(0.75)
    )
    start_btn.fill.solid()
    start_btn.fill.fore_color.rgb = TERRACOTTA
    start_btn.line.color.rgb = GOLD_ACCENT
    start_btn.line.width = Pt(2)
    start_btn.click_action.target_slide = slides[1]
    tf_start = start_btn.text_frame
    tf_start.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_start = tf_start.paragraphs[0]
    p_start.alignment = PP_ALIGN.CENTER
    r_start = p_start.add_run()
    r_start.text = "📖 Open Storybook & Table of Contents ➡️"
    r_start.font.name = "Georgia"
    r_start.font.size = Pt(14)
    r_start.font.bold = True
    r_start.font.color.rgb = WHITE
    r_start.hyperlink.target_slide = slides[1]

    # =========================================================================
    # SLIDE 2: TABLE OF CONTENTS (INTERACTIVE MAP)
    # =========================================================================
    s2 = slides[1]
    set_slide_background(s2, BG_CREAM)
    add_header(s2, "STORYBOOK MAP", "Table of Contents & Learning Stations", "CLICK ANY CHAPTER TO JUMP DIRECTLY")
    add_navbar(s2, 1)

    # 12 Interactive Grid Cards
    toc_cards = [
        ("🌸 Chapter 1", "Lily & Her Loving Mummy", "The joy of home, school walks & favorite treats", 2, Inches(0.7), Inches(1.4)),
        ("🌧️ Chapter 2", "The Sudden Storm & Tears", "Grandma arrives, tears at school, hospital news", 3, Inches(3.75), Inches(1.4)),
        ("✝️ Chapter 3", "The Heavenly Great Doctor", "Miss Huang reveals Lord Jesus, the Great Physician", 4, Inches(6.8), Inches(1.4)),
        ("🙏 Chapter 4", "Lily's First Prayer & Miracle", "Praying hand in hand, successful surgery & joy", 5, Inches(9.85), Inches(1.4)),

        ("🌟 Chapter 5", "Giving Thanks in Everything", "Miss Huang's question: Who else to thank?", 6, Inches(0.7), Inches(3.1)),
        ("🕊️ Chapter 6", "The Secret Bedside Prayer", "Mummy discovers Lily kneeling and praying daily", 7, Inches(3.75), Inches(3.1)),
        ("💖 Chapter 7", "Tears of Grace & Believing Home", "Mummy's tears, faith in Christ, spiritual healing", 8, Inches(6.8), Inches(3.1)),
        ("💡 Story Moral", "4 Key Life Lessons", "Childlike prayer, thanksgiving, witness & healing", 9, Inches(9.85), Inches(3.1)),

        ("📜 Memory Verse", "1 Thessalonians 5:18", "Breakdown, word study, and memorization guide", 10, Inches(0.7), Inches(4.8)),
        ("🎵 Hymn Sanctuary", "Song of Thanksgiving", "Lyrics, chords, reflections & custom hymn space", 11, Inches(3.75), Inches(4.8)),
        ("❓ Interactive Quiz", "Story Discussion & Q&A", "4 questions with click-to-reveal answers", 12, Inches(6.8), Inches(4.8)),
        ("🎭 Daily Routine", "Acting Game & Prayer Habit", "Thanksgiving prayer training & classroom drama", 13, Inches(9.85), Inches(4.8)),
    ]

    for ch_tag, title, desc, target_idx, cx, cy in toc_cards:
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(2.8), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)
        card.click_action.target_slide = slides[target_idx]

        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP

        p_tag = tf.paragraphs[0]
        p_tag.text = ch_tag
        p_tag.font.name = "Georgia"
        p_tag.font.size = Pt(10.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TERRACOTTA

        p_tit = tf.add_paragraph()
        p_tit.text = title
        p_tit.font.name = "Georgia"
        p_tit.font.size = Pt(12)
        p_tit.font.bold = True
        p_tit.font.color.rgb = BOOK_SPINE

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = TEXT_MUTED

        p_btn = tf.add_paragraph()
        p_btn.space_before = Pt(4)
        r = p_btn.add_run()
        r.text = "Click to Open ➡️"
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = GOLD_ACCENT
        r.hyperlink.target_slide = slides[target_idx]

    # =========================================================================
    # HELPER FOR STORY CHAPTER SLIDES (SLIDES 3 - 9)
    # =========================================================================
    def build_story_slide(slide_idx, ch_tag, title, story_paragraphs, quote_text, quote_author, insights_list, highlight_box_title, highlight_box_text, current_num):
        sl = slides[slide_idx]
        set_slide_background(sl, BG_CREAM)
        add_header(sl, ch_tag, title)
        add_navbar(sl, slide_idx)

        # LEFT STORYBOOK PAGE (The Narrative)
        left_card = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.7), Inches(1.35), Inches(5.8), Inches(5.3)
        )
        left_card.fill.solid()
        left_card.fill.fore_color.rgb = WHITE
        left_card.line.color.rgb = BORDER_COLOR
        left_card.line.width = Pt(1.5)

        # Left page ribbon banner
        ribbon = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.9), Inches(1.5), Inches(5.4), Inches(0.4)
        )
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = GOLD_LIGHT
        ribbon.line.color.rgb = GOLD_ACCENT
        ribbon.line.width = Pt(1)
        tf_r = ribbon.text_frame
        p_r = tf_r.paragraphs[0]
        p_r.text = f"📖 STORYBOOK READING • PAGE {current_num} OF 7"
        p_r.font.name = "Calibri"
        p_r.font.size = Pt(9.5)
        p_r.font.bold = True
        p_r.font.color.rgb = GOLD_ACCENT
        p_r.alignment = PP_ALIGN.CENTER

        # Story text box
        tb_story = sl.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.4), Inches(4.5))
        tf_story = tb_story.text_frame
        tf_story.word_wrap = True

        for i, para in enumerate(story_paragraphs):
            p = tf_story.paragraphs[0] if i == 0 else tf_story.add_paragraph()
            p.text = para
            p.font.name = "Georgia"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(10)
            p.line_spacing = 1.25

        # RIGHT STORYBOOK PAGE (Dialogue, Insights & Reflection)
        right_card = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.8), Inches(1.35), Inches(5.833), Inches(5.3)
        )
        right_card.fill.solid()
        right_card.fill.fore_color.rgb = WHITE
        right_card.line.color.rgb = BORDER_COLOR
        right_card.line.width = Pt(1.5)

        # Quote Card
        quote_card = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(7.05), Inches(1.5), Inches(5.333), Inches(1.6)
        )
        quote_card.fill.solid()
        quote_card.fill.fore_color.rgb = TERRA_LIGHT
        quote_card.line.color.rgb = TERRACOTTA
        quote_card.line.width = Pt(1.5)

        tf_q = quote_card.text_frame
        tf_q.word_wrap = True
        p_q_tag = tf_q.paragraphs[0]
        p_q_tag.text = "💬 STORYBOOK DIALOGUE"
        p_q_tag.font.name = "Calibri"
        p_q_tag.font.size = Pt(9)
        p_q_tag.font.bold = True
        p_q_tag.font.color.rgb = TERRACOTTA

        p_q = tf_q.add_paragraph()
        p_q.text = f"“{quote_text}”"
        p_q.font.name = "Georgia"
        p_q.font.size = Pt(12.5)
        p_q.font.bold = True
        p_q.font.color.rgb = TEXT_DARK
        p_q.space_before = Pt(4)

        p_qa = tf_q.add_paragraph()
        p_qa.text = f"— {quote_author}"
        p_qa.font.name = "Calibri"
        p_qa.font.size = Pt(10)
        p_qa.font.italic = True
        p_qa.font.color.rgb = TERRACOTTA

        # Insights Container
        insights_card = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(7.05), Inches(3.2), Inches(5.333), Inches(1.75)
        )
        insights_card.fill.solid()
        insights_card.fill.fore_color.rgb = SAGE_LIGHT
        insights_card.line.color.rgb = SAGE_GREEN
        insights_card.line.width = Pt(1.5)

        tf_ins = insights_card.text_frame
        tf_ins.word_wrap = True
        p_in_tag = tf_ins.paragraphs[0]
        p_in_tag.text = "✨ HEART INSIGHTS & THEMES"
        p_in_tag.font.name = "Calibri"
        p_in_tag.font.size = Pt(9)
        p_in_tag.font.bold = True
        p_in_tag.font.color.rgb = SAGE_GREEN

        for ins in insights_list:
            p_in = tf_ins.add_paragraph()
            p_in.text = f"• {ins}"
            p_in.font.name = "Calibri"
            p_in.font.size = Pt(11)
            p_in.font.color.rgb = TEXT_DARK
            p_in.space_before = Pt(3)

        # Highlight Reflection Box
        hl_card = sl.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(7.05), Inches(5.05), Inches(5.333), Inches(1.4)
        )
        hl_card.fill.solid()
        hl_card.fill.fore_color.rgb = BLUE_LIGHT
        hl_card.line.color.rgb = BOOK_SPINE
        hl_card.line.width = Pt(1)

        tf_hl = hl_card.text_frame
        tf_hl.word_wrap = True
        p_hl_tag = tf_hl.paragraphs[0]
        p_hl_tag.text = f"💡 {highlight_box_title}"
        p_hl_tag.font.name = "Calibri"
        p_hl_tag.font.size = Pt(9)
        p_hl_tag.font.bold = True
        p_hl_tag.font.color.rgb = BOOK_SPINE

        p_hl_txt = tf_hl.add_paragraph()
        p_hl_txt.text = highlight_box_text
        p_hl_txt.font.name = "Georgia"
        p_hl_txt.font.size = Pt(11)
        p_hl_txt.font.color.rgb = TEXT_DARK
        p_hl_txt.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: CHAPTER 1
    # =========================================================================
    build_story_slide(
        slide_idx=2,
        ch_tag="CHAPTER 1",
        title="Lily & Her Loving Mummy",
        story_paragraphs=[
            "Lily was a happy little girl because she had a mummy who loved her dearly. Lily liked Mummy best of all, feeling that Mummy was the most capable and wonderful mother in the entire world.",
            "Every morning, Mummy accompanied Lily to school with a warm smile. After school, Mummy was always waiting by the gates to welcome Lily home with open arms.",
            "Back at home, Mummy always prepared Lily's most favorite food. She played joyful games with Lily and told her wonderful stories before bedtime. All of Lily's classmates admired her when they saw how happy Lily looked with her mummy!"
        ],
        quote_text="Mummy is the most capable and the best mummy in the world!",
        quote_author="Lily's Heartfelt Joy",
        insights_list=[
            "Lily was filled with happiness because of her mother's daily selfless love.",
            "Love in action: walks to school, warm meals, playtime, and bedtime stories.",
            "Lily's classmates could clearly see the radiance of a loved, joyful child."
        ],
        highlight_box_title="QUESTION FOR KIDS",
        highlight_box_text="What are some loving things your parents or family do for you every day that bring a smile to your face?",
        current_num=1
    )

    # =========================================================================
    # SLIDE 4: CHAPTER 2
    # =========================================================================
    build_story_slide(
        slide_idx=3,
        ch_tag="CHAPTER 2",
        title="The Sudden Storm & Tears",
        story_paragraphs=[
            "One day when Lily came to school, it was not Mummy but Grandma who walked with her. As soon as Lily entered the classroom, everyone noticed something unusual.",
            "Lily did not greet the other children happily as she always did. Instead, she bowed her head in silence and said nothing. Miss Huang asked with concern, 'Lily, did anything happen to your family?' The classmates gathered around with worry.",
            "Lily's tears came down as she whispered: 'Mummy is ill and in hospital.' After school, Miss Huang said gently, 'Is it OK if I go to the hospital with you to see Mummy?' Lily nodded. Mummy was seriously ill and had to undergo a dangerous surgery. Lily cried in fear, but Miss Huang held her close and comforted her."
        ],
        quote_text="Mummy is ill and in hospital... will Mummy never be able to come home?",
        quote_author="Lily to Miss Huang in Tears",
        insights_list=[
            "Trials and unexpected illnesses can arrive suddenly in any family.",
            "Lily's teacher, Miss Huang, showed Christlike compassion by listening and accompanying her.",
            "A caring teacher and loving classmates stepped in to surround Lily with warmth."
        ],
        highlight_box_title="HEART LESSON",
        highlight_box_text="When someone around us is sad or weeping, a gentle presence, a listening ear, and a warm embrace can bring comfort from God.",
        current_num=2
    )

    # =========================================================================
    # SLIDE 5: CHAPTER 3
    # =========================================================================
    build_story_slide(
        slide_idx=4,
        ch_tag="CHAPTER 3",
        title="The Heavenly Great Doctor",
        story_paragraphs=[
            "'Miss Huang, will Mummy never be able to come home?' Lily asked in fear.",
            "Miss Huang spoke with kind tenderness: 'Lily, I am not a doctor and I don't know Mummy's illness. But I know a Great Doctor from heaven who can heal all our illnesses!'",
            "'Really? Then how am I to find the Great Doctor?' Lily asked with wide-opened eyes.",
            "Miss Huang explained: 'This Great Doctor is called Lord Jesus! He is omnipresent—everywhere with us. The Bible tells us that as long as we call on His name, He will enter into us. We can pray to Him and tell Him all our needs. He will hear and help us!'"
        ],
        quote_text="I know a Great Doctor from heaven who can heal our illnesses. This Great Doctor is called Lord Jesus!",
        quote_author="Miss Huang's Comfort to Lily",
        insights_list=[
            "Jesus is the Heavenly Physician with authority over sickness and sorrow.",
            "Omnipresent: He is not confined to one building; He is near to all who call.",
            "The simplicity of prayer: We can talk to Him anytime and tell Him our deepest fears."
        ],
        highlight_box_title="THE PROMISE OF GOD",
        highlight_box_text="“Call upon Me in the day of trouble; I will deliver you, and you shall glorify Me.” (Psalm 50:15)",
        current_num=3
    )

    # =========================================================================
    # SLIDE 6: CHAPTER 4
    # =========================================================================
    build_story_slide(
        slide_idx=5,
        ch_tag="CHAPTER 4",
        title="Lily's First Prayer & The Miracle",
        story_paragraphs=[
            "After hearing Miss Huang's comforting words, Lily wanted Miss Huang to teach her right away how to pray.",
            "Miss Huang gently held Lily's little hands. Together, they called upon Lord Jesus and prayed. They asked Lord Jesus to give Mummy a successful surgery, to bring her safely home, and also to help Mummy come to know and believe in Lord Jesus.",
            "From that day on, Miss Huang often accompanied Lily to the hospital to visit Mummy. God heard their prayers! Mummy's dangerous surgery was completely successful, and she returned safely home. Lily was overjoyed that Lord Jesus had answered their prayers!"
        ],
        quote_text="Lord Jesus heard our prayer! Mummy had a successful surgery and went back home!",
        quote_author="Lily's Joyful Announcement",
        insights_list=[
            "Lily acted immediately on faith: she asked to learn how to pray right away.",
            "Praying for both physical healing (safe surgery) and spiritual life (believing in Jesus).",
            "God honors childlike faith: the dangerous surgery was a complete success!"
        ],
        highlight_box_title="FAITH MILESTONE",
        highlight_box_text="Lily learned that Lord Jesus is not a distant name in a book, but a living Savior who hears when small children call upon Him.",
        current_num=4
    )

    # =========================================================================
    # SLIDE 7: CHAPTER 5
    # =========================================================================
    build_story_slide(
        slide_idx=6,
        ch_tag="CHAPTER 5",
        title="Giving Thanks in Everything",
        story_paragraphs=[
            "The first thing Lily did when she returned to school was rush to Miss Huang with the wonderful news. Miss Huang waited smilingly and said: 'Lord Jesus answered Lily's prayer. Is Lily happy?' 'Of course I'm happy!' Lily beamed.",
            "'Then, is there anyone Lily wants to thank?' Miss Huang asked gently. 'Yes! I want to thank you, my teacher!' 'Anyone else?' Miss Huang prompted.",
            "'To thank... Lord Jesus!' Lily declared. 'Right!' smiled Miss Huang. 'The Bible tells us not only to pray to the Lord, but also to thank the Lord always, to give thanks in everything!' Together, they knelt and thanked Lord Jesus, praying that Mummy would believe soon."
        ],
        quote_text="The Bible tells us not only to pray to the Lord, but also to thank the Lord always, to give thanks in everything!",
        quote_author="Miss Huang Teaching Thanksgiving",
        insights_list=[
            "It is natural to thank human helpers, but we must never forget the Source: Lord Jesus!",
            "Petition is only half of prayer; the other half is heartfelt Thanksgiving.",
            "1 Thessalonians 5:18 in action: In everything give thanks!"
        ],
        highlight_box_title="THE GOLDEN PRINCIPLE",
        highlight_box_text="When God answers prayer, grateful hearts return with praise. Giving thanks protects our joy and honors our Lord.",
        current_num=5
    )

    # =========================================================================
    # SLIDE 8: CHAPTER 6
    # =========================================================================
    build_story_slide(
        slide_idx=7,
        ch_tag="CHAPTER 6",
        title="The Secret Bedside Prayer",
        story_paragraphs=[
            "Lily's mummy was getting better day by day. As she rested, she often noticed Lily quietly kneeling before the bed alone, softly whispering something.",
            "Curious, Mummy asked: 'Lily, you kneel before the bed alone every day and keep murmuring something. What is it that you are saying?'",
            "Lily looked up with shining eyes: 'I'm talking to Lord Jesus! When Mummy was having surgery, Miss Huang prayed with me to Lord Jesus. When you got better, Miss Huang told me to always give thanks to the Lord. So every day I kneel and say: Thank you, Lord Jesus, for making Mummy recover! Please also make Mummy come to believe in Lord Jesus!'"
        ],
        quote_text="I say, thank you, Lord Jesus, for making Mummy recover. Please also make Mummy come to believe in Lord Jesus!",
        quote_author="Lily's Secret Bedside Prayer",
        insights_list=[
            "Lily didn't just pray at school; prayer became her personal, private daily habit.",
            "She remembered to say 'Thank You' every single day without being reminded.",
            "Her persistent prayer carried two wishes: healing for Mummy's body and salvation for her soul."
        ],
        highlight_box_title="A CHILD'S DEVOTION",
        highlight_box_text="A little girl kneeling beside the bed became the sweetest altar of praise in the home, moving heaven and earth.",
        current_num=6
    )

    # =========================================================================
    # SLIDE 9: CHAPTER 7
    # =========================================================================
    build_story_slide(
        slide_idx=8,
        ch_tag="CHAPTER 7",
        title="Tears of Grace & A Believing Family",
        story_paragraphs=[
            "Mummy's tears came down unconsciously as she was listening to Lily. Her heart was deeply moved to realize that her little daughter had been faithfully praying and giving thanks for her every day.",
            "Lily's mummy totally recovered from her sickness—and she also came to believe in Lord Jesus! The Lord had granted far more than physical healing; He gave their home eternal life and peace.",
            "Every day now, Mummy kneels and prays together with Lily to Lord Jesus, thanking the Lord for having healed them, not only Mummy's illness, but also their spirits! Their home was filled with songs of thanksgiving."
        ],
        quote_text="Every day, Mummy prays with Lily to Lord Jesus, thanking the Lord for having healed not only Mummy's illness, but also their spirits.",
        quote_author="The Fruit of Faith & Gratitude",
        insights_list=[
            "Mummy was melted by Lily's sincere gratitude and faithful prayers.",
            "Double Healing: Physical restoration of the body AND spiritual salvation of the soul.",
            "A transformed home: A praying mother and daughter united in Christ."
        ],
        highlight_box_title="ETERNAL REWARD",
        highlight_box_text="“Believe on the Lord Jesus Christ, and you will be saved, you and your household.” (Acts 16:31)",
        current_num=7
    )

    # =========================================================================
    # SLIDE 10: THE MORAL OF THE STORY (4 KEY PILLARS)
    # =========================================================================
    s10 = slides[9]
    set_slide_background(s10, BG_CREAM)
    add_header(s10, "LIFE LESSONS", "The Moral of the Story • 4 Spiritual Truths", "KEY TAKEAWAYS FOR SUNDAY SCHOOL & DAILY LIFE")
    add_navbar(s10, 9)

    morals = [
        (
            "🌟 1. In Everything Give Thanks",
            "Gratitude as a Lifestyle",
            "Thanksgiving is not just for sunny days or when everything is easy. Miss Huang taught Lily to thank Lord Jesus after prayer was answered. True faith thanks God for who He is, what He has done, and what He will do.",
            GOLD_LIGHT, GOLD_ACCENT, Inches(0.7), Inches(1.4)
        ),
        (
            "🙏 2. The Power of Childlike Prayer",
            "Sincere Faith Touches God",
            "You don't need fancy theological words to pray. Lily simply held hands, called on the Lord Jesus, and asked for Mummy's healing. God hears the earnest cry of children and delights to answer their sincere faith.",
            SAGE_LIGHT, SAGE_GREEN, Inches(6.8), Inches(1.4)
        ),
        (
            "🩺 3. The Heavenly Great Doctor",
            "Healing for Body & Spirit",
            "While earthly doctors and medicine are God-given gifts, Lord Jesus is the Great Physician. He healed Mummy's physical illness and, even greater, healed their spirits, filling their hearts with peace and eternal life.",
            BLUE_LIGHT, BOOK_SPINE, Inches(0.7), Inches(4.0)
        ),
        (
            "🕯️ 4. A Child's Living Witness",
            "Transforming the Family Home",
            "Lily didn't argue or preach; she simply knelt, thanked Jesus, and loved her mother. Her daily bedtime thanksgiving touched Mummy to tears and brought salvation to the whole household. Children can lead others to Christ!",
            TERRA_LIGHT, TERRACOTTA, Inches(6.8), Inches(4.0)
        )
    ]

    for title, subtitle, desc, bg_color, border_col, mx, my in morals:
        m_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, my, Inches(5.833), Inches(2.45))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = bg_color
        m_card.line.color.rgb = border_col
        m_card.line.width = Pt(2)

        tf_m = m_card.text_frame
        tf_m.word_wrap = True

        p_mt = tf_m.paragraphs[0]
        p_mt.text = title
        p_mt.font.name = "Georgia"
        p_mt.font.size = Pt(14)
        p_mt.font.bold = True
        p_mt.font.color.rgb = border_col

        p_sub = tf_m.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(10.5)
        p_sub.font.bold = True
        p_sub.font.italic = True
        p_sub.font.color.rgb = TEXT_DARK
        p_sub.space_before = Pt(2)

        p_txt = tf_m.add_paragraph()
        p_txt.text = desc
        p_txt.font.name = "Calibri"
        p_txt.font.size = Pt(11)
        p_txt.font.color.rgb = TEXT_DARK
        p_txt.space_before = Pt(6)
        p_txt.line_spacing = 1.2

    # =========================================================================
    # SLIDE 11: GOLDEN MEMORY VERSE (1 THESSALONIANS 5:18)
    # =========================================================================
    s11 = slides[10]
    set_slide_background(s11, BG_CREAM)
    add_header(s11, "SCRIPTURE MEMORY", "Golden Memory Verse • 1 Thessalonians 5:18", "GOD'S WORD FOR OUR HEARTS")
    add_navbar(s11, 10)

    # Big Parchment Scroll
    scroll = s11.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.2), Inches(1.35), Inches(10.933), Inches(2.3)
    )
    scroll.fill.solid()
    scroll.fill.fore_color.rgb = GOLD_LIGHT
    scroll.line.color.rgb = GOLD_ACCENT
    scroll.line.width = Pt(2.5)

    tf_sc = scroll.text_frame
    tf_sc.word_wrap = True
    p_sc_tag = tf_sc.paragraphs[0]
    p_sc_tag.alignment = PP_ALIGN.CENTER
    p_sc_tag.text = "📜 SCRIPTURE OF THE WEEK"
    p_sc_tag.font.name = "Calibri"
    p_sc_tag.font.size = Pt(11)
    p_sc_tag.font.bold = True
    p_sc_tag.font.color.rgb = GOLD_ACCENT

    p_sc_v = tf_sc.add_paragraph()
    p_sc_v.alignment = PP_ALIGN.CENTER
    p_sc_v.text = "“In everything give thanks;\nfor this is the will of God in Christ Jesus for you.”"
    p_sc_v.font.name = "Georgia"
    p_sc_v.font.size = Pt(22)
    p_sc_v.font.bold = True
    p_sc_v.font.color.rgb = BOOK_SPINE
    p_sc_v.space_before = Pt(6)

    p_sc_ref = tf_sc.add_paragraph()
    p_sc_ref.alignment = PP_ALIGN.CENTER
    p_sc_ref.text = "— 1 Thessalonians 5:18 (Memory Verse Focus: 1 Thessalonians 5:18a)"
    p_sc_ref.font.name = "Georgia"
    p_sc_ref.font.size = Pt(13)
    p_sc_ref.font.bold = True
    p_sc_ref.font.color.rgb = TERRACOTTA
    p_sc_ref.space_before = Pt(4)

    # 3 Breakdown Columns
    verse_steps = [
        (
            "1. IN EVERYTHING",
            "The Circumstance",
            "Not just when we receive presents or when it's sunny! We thank God in school, at home, during trials, and in sickness, because God is always with us.",
            GOLD_ACCENT, Inches(1.2), Inches(3.85)
        ),
        (
            "2. GIVE THANKS",
            "The Action",
            "Gratitude must be spoken and expressed! Open your mouth, kneel by your bed, sing praises, and declare 'Thank You, Lord Jesus' every single day.",
            TERRACOTTA, Inches(4.9), Inches(3.85)
        ),
        (
            "3. GOD'S WILL FOR YOU",
            "The Purpose",
            "God loves a thankful child. Giving thanks is not a burdensome rule—it is God's will to guard our hearts with joyful peace and eternal life.",
            SAGE_GREEN, Inches(8.6), Inches(3.85)
        )
    ]

    for title, subtitle, exp, color, sx, sy in verse_steps:
        box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, Inches(3.533), Inches(1.75))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tf_b = box.text_frame
        tf_b.word_wrap = True
        p_bt = tf_b.paragraphs[0]
        p_bt.text = title
        p_bt.font.name = "Georgia"
        p_bt.font.size = Pt(13)
        p_bt.font.bold = True
        p_bt.font.color.rgb = color

        p_bs = tf_b.add_paragraph()
        p_bs.text = subtitle
        p_bs.font.name = "Calibri"
        p_bs.font.size = Pt(10)
        p_bs.font.bold = True
        p_bs.font.color.rgb = TEXT_MUTED

        p_be = tf_b.add_paragraph()
        p_be.text = exp
        p_be.font.name = "Calibri"
        p_be.font.size = Pt(10.5)
        p_be.font.color.rgb = TEXT_DARK
        p_be.space_before = Pt(4)

    # Interactive Memorization Activity Bar
    recite_bar = s11.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.2), Inches(5.75), Inches(10.933), Inches(0.85)
    )
    recite_bar.fill.solid()
    recite_bar.fill.fore_color.rgb = SAGE_LIGHT
    recite_bar.line.color.rgb = SAGE_GREEN
    recite_bar.line.width = Pt(1)
    tf_rc = recite_bar.text_frame
    tf_rc.word_wrap = True
    p_rc = tf_rc.paragraphs[0]
    p_rc.alignment = PP_ALIGN.CENTER
    p_rc.text = "🎯 INTERACTIVE MEMORY CHALLENGE FOR SUNDAY SCHOOL"
    p_rc.font.name = "Calibri"
    p_rc.font.size = Pt(10)
    p_rc.font.bold = True
    p_rc.font.color.rgb = SAGE_GREEN

    p_rc2 = tf_rc.add_paragraph()
    p_rc2.alignment = PP_ALIGN.CENTER
    p_rc2.text = "1. Clap hands on 'IN EVERYTHING' 👏 • 2. Hands over heart on 'GIVE THANKS' 💖 • 3. Point up on 'WILL OF GOD' ☝️ • Recite 3 times together!"
    p_rc2.font.name = "Georgia"
    p_rc2.font.size = Pt(11)
    p_rc2.font.bold = True
    p_rc2.font.color.rgb = BOOK_SPINE

    # =========================================================================
    # SLIDE 12: HYMN & WORSHIP SANCTUARY (WITH DEDICATED HYMN SPACE)
    # =========================================================================
    s12 = slides[11]
    set_slide_background(s12, BG_CREAM)
    add_header(s12, "HYMN & PRAISE", "Hymn Sanctuary • Songs of Thanksgiving", "GIVE THANKS WITH A GRATEFUL HEART")
    add_navbar(s12, 11)

    # Left Column: Featured Classic Hymn (Give Thanks)
    hymn1_card = s12.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.7), Inches(1.35), Inches(5.8), Inches(5.3)
    )
    hymn1_card.fill.solid()
    hymn1_card.fill.fore_color.rgb = WHITE
    hymn1_card.line.color.rgb = GOLD_ACCENT
    hymn1_card.line.width = Pt(2)

    tf_h1 = hymn1_card.text_frame
    tf_h1.word_wrap = True

    p_h1_tag = tf_h1.paragraphs[0]
    p_h1_tag.text = "🎵 FEATURED HYMN OF THANKSGIVING"
    p_h1_tag.font.name = "Calibri"
    p_h1_tag.font.size = Pt(10)
    p_h1_tag.font.bold = True
    p_h1_tag.font.color.rgb = GOLD_ACCENT

    p_h1_title = tf_h1.add_paragraph()
    p_h1_title.text = "Give Thanks with a Grateful Heart"
    p_h1_title.font.name = "Georgia"
    p_h1_title.font.size = Pt(18)
    p_h1_title.font.bold = True
    p_h1_title.font.color.rgb = BOOK_SPINE

    p_h1_meta = tf_h1.add_paragraph()
    p_h1_meta.text = "Author: Henry Smith (1978) • Key: F Major • Tempo: Gentle & Joyful"
    p_h1_meta.font.name = "Calibri"
    p_h1_meta.font.size = Pt(9.5)
    p_h1_meta.font.italic = True
    p_h1_meta.font.color.rgb = TEXT_MUTED
    p_h1_meta.space_after = Pt(8)

    lyrics = [
        "Give thanks with a grateful heart,",
        "Give thanks to the Holy One,",
        "Give thanks because He’s given Jesus Christ, His Son.",
        "",
        "And now let the weak say, “I am strong,”",
        "Let the poor say, “I am rich,”",
        "Because of what the Lord has done for us.",
        "",
        "Give thanks! Give thanks!"
    ]
    for line in lyrics:
        p_ly = tf_h1.add_paragraph()
        p_ly.text = line
        p_ly.font.name = "Georgia"
        p_ly.font.size = Pt(12)
        p_ly.font.color.rgb = TEXT_DARK
        p_ly.line_spacing = 1.15

    p_h1_act = tf_h1.add_paragraph()
    p_h1_act.space_before = Pt(8)
    p_h1_act.text = "🎼 Worship Motion: Place both hands over heart during 'Grateful Heart', and lift hands upward during 'Give Thanks!'"
    p_h1_act.font.name = "Calibri"
    p_h1_act.font.size = Pt(9.5)
    p_h1_act.font.bold = True
    p_h1_act.font.color.rgb = TERRACOTTA

    # Right Column Top: Alternative Classic Hymn (Count Your Blessings)
    hymn2_card = s12.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.8), Inches(1.35), Inches(5.833), Inches(2.2)
    )
    hymn2_card.fill.solid()
    hymn2_card.fill.fore_color.rgb = SAGE_LIGHT
    hymn2_card.line.color.rgb = SAGE_GREEN
    hymn2_card.line.width = Pt(1.5)

    tf_h2 = hymn2_card.text_frame
    tf_h2.word_wrap = True
    p_h2_tag = tf_h2.paragraphs[0]
    p_h2_tag.text = "🎶 HYMN REFRAIN • COUNT YOUR BLESSINGS"
    p_h2_tag.font.name = "Calibri"
    p_h2_tag.font.size = Pt(9.5)
    p_h2_tag.font.bold = True
    p_h2_tag.font.color.rgb = SAGE_GREEN

    p_h2_ly = tf_h2.add_paragraph()
    p_h2_ly.text = "“Count your blessings, name them one by one;\nCount your blessings, see what God hath done!\nCount your blessings, name them one by one,\nAnd it will surprise you what the Lord hath done!”"
    p_h2_ly.font.name = "Georgia"
    p_h2_ly.font.size = Pt(11.5)
    p_h2_ly.font.italic = True
    p_h2_ly.font.color.rgb = TEXT_DARK
    p_h2_ly.space_before = Pt(4)

    # Right Column Bottom: DEDICATED SPACE FOR HYMN
    custom_card = s12.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.8), Inches(3.7), Inches(5.833), Inches(2.95)
    )
    custom_card.fill.solid()
    custom_card.fill.fore_color.rgb = GOLD_LIGHT
    custom_card.line.color.rgb = GOLD_ACCENT
    custom_card.line.width = Pt(2)

    tf_c = custom_card.text_frame
    tf_c.word_wrap = True

    p_ct = tf_c.paragraphs[0]
    p_ct.text = "🎼 DEDICATED SPACE FOR CHURCH & FAMILY HYMN"
    p_ct.font.name = "Calibri"
    p_ct.font.size = Pt(10)
    p_ct.font.bold = True
    p_ct.font.color.rgb = GOLD_ACCENT

    p_c_sub = tf_c.add_paragraph()
    p_c_sub.text = "[ Insert Your Sunday School / Congregation Hymn or Chorus Here ]"
    p_c_sub.font.name = "Georgia"
    p_c_sub.font.size = Pt(12)
    p_c_sub.font.bold = True
    p_c_sub.font.color.rgb = BOOK_SPINE
    p_c_sub.space_before = Pt(2)

    prompt_lines = [
        "• Song Title / Hymn No.: _________________________________________",
        "• Tune / Key / Musical Chords: ___________________________________",
        "• Verse 1 / Chorus Lyrics: ______________________________________",
        "  (Space to paste local church song, children's praise tune, or audio link)",
        "• Reflection: Why is this hymn meaningful to sing after Lily's story?"
    ]
    for line in prompt_lines:
        p_l = tf_c.add_paragraph()
        p_l.text = line
        p_l.font.name = "Calibri"
        p_l.font.size = Pt(10.5)
        p_l.font.color.rgb = TEXT_DARK
        p_l.space_before = Pt(3)

    # =========================================================================
    # SLIDE 13: INTERACTIVE STORY DISCUSSION (Q&A QUIZ)
    # =========================================================================
    s13 = slides[12]
    set_slide_background(s13, BG_CREAM)
    add_header(s13, "INTERACTIVE Q&A", "Story Discussion & Comprehension Quiz", "CLICK TO REVEAL KEY INSIGHTS & ANSWERS")
    add_navbar(s13, 12)

    questions = [
        (
            "Q1. Why was Lily such a happy child at the beginning?",
            "REVEAL ANSWER: Because she had a mummy who loved her dearly. Mummy walked her to school, cooked her favorite treats, played games, and told her stories every night.",
            GOLD_ACCENT, Inches(0.7), Inches(1.4)
        ),
        (
            "Q2. Why did Lily enter school crying and upset one day?",
            "REVEAL ANSWER: Her mummy was seriously ill in the hospital, Grandma brought her to school, and the doctor said Mummy needed a dangerous, risky surgery.",
            TERRACOTTA, Inches(6.8), Inches(1.4)
        ),
        (
            "Q3. How did Miss Huang comfort and help Lily?",
            "REVEAL ANSWER: She held Lily close, told her about Lord Jesus—the Heavenly Great Doctor who hears prayer—taught Lily how to pray, and accompanied her to the hospital.",
            SAGE_GREEN, Inches(0.7), Inches(4.0)
        ),
        (
            "Q4. When Mummy recovered, what did Miss Huang teach Lily to do?",
            "REVEAL ANSWER: She taught Lily not only to ask, but to give thanks to Lord Jesus in everything! (1 Thess. 5:18). Lily practiced this daily, leading her mother to faith.",
            BOOK_SPINE, Inches(6.8), Inches(4.0)
        )
    ]

    for q_text, a_text, border_col, qx, qy in questions:
        q_box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, qy, Inches(5.833), Inches(2.45))
        q_box.fill.solid()
        q_box.fill.fore_color.rgb = WHITE
        q_box.line.color.rgb = border_col
        q_box.line.width = Pt(1.5)

        tf_q = q_box.text_frame
        tf_q.word_wrap = True

        p_qt = tf_q.paragraphs[0]
        p_qt.text = q_text
        p_qt.font.name = "Georgia"
        p_qt.font.size = Pt(13)
        p_qt.font.bold = True
        p_qt.font.color.rgb = border_col

        p_btn = tf_q.add_paragraph()
        p_btn.text = "💡 Interactive Teacher / Student Reveal Box:"
        p_btn.font.name = "Calibri"
        p_btn.font.size = Pt(9.5)
        p_btn.font.bold = True
        p_btn.font.color.rgb = GOLD_ACCENT
        p_btn.space_before = Pt(4)

        p_ans = tf_q.add_paragraph()
        p_ans.text = a_text
        p_ans.font.name = "Calibri"
        p_ans.font.size = Pt(11)
        p_ans.font.color.rgb = TEXT_DARK
        p_ans.space_before = Pt(2)
        p_ans.line_spacing = 1.15

    # =========================================================================
    # SLIDE 14: ROUTINE TRAINING & ACTING GAME ACTIVITY
    # =========================================================================
    s14 = slides[13]
    set_slide_background(s14, BG_CREAM)
    add_header(s14, "PRACTICAL ACTION", "Routine Training & The Thanksgiving Acting Game", "LIVING OUT 1 THESSALONIANS 5:18 EVERY DAY")
    add_navbar(s14, 13)

    # Left Column: Routine Training & Daily Prayer
    rt_card = s14.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.7), Inches(1.35), Inches(5.8), Inches(5.3)
    )
    rt_card.fill.solid()
    rt_card.fill.fore_color.rgb = WHITE
    rt_card.line.color.rgb = SAGE_GREEN
    rt_card.line.width = Pt(2)

    tf_rt = rt_card.text_frame
    tf_rt.word_wrap = True

    p_rt_t = tf_rt.paragraphs[0]
    p_rt_t.text = "🙏 ROUTINE TRAINING • GIVE THANKS IN EVERYTHING"
    p_rt_t.font.name = "Calibri"
    p_rt_t.font.size = Pt(10)
    p_rt_t.font.bold = True
    p_rt_t.font.color.rgb = SAGE_GREEN

    p_rt_sub = tf_rt.add_paragraph()
    p_rt_sub.text = "The Teacher Leads Kids in Daily Thanksgiving Prayer"
    p_rt_sub.font.name = "Georgia"
    p_rt_sub.font.size = Pt(14)
    p_rt_sub.font.bold = True
    p_rt_sub.font.color.rgb = BOOK_SPINE
    p_rt_sub.space_before = Pt(2)

    prayer_items = [
        "The daily prayer focuses on giving heartfelt thanks to the Lord:",
        "1. Thank the Lord for giving us a joyful meeting and fellowship.",
        "2. Thank the Lord for keeping our whole family in peace and safety.",
        "3. Thank the Lord for daily food, snacks, clothes, and caring teachers.",
        "",
        "🌟 Daily Practice Prayer Formula:",
        "“Lord Jesus, thank You for giving me a new day so that I can give thanks in everything. Keep our hearts thankful, joyful, and full of Your peace. Amen.”"
    ]
    for p_line in prayer_items:
        p_item = tf_rt.add_paragraph()
        p_item.text = p_line
        p_item.font.name = "Calibri"
        if p_line.startswith("“Lord Jesus"):
            p_item.font.name = "Georgia"
            p_item.font.size = Pt(11.5)
            p_item.font.bold = True
            p_item.font.italic = True
            p_item.font.color.rgb = TERRACOTTA
        elif p_line.startswith("🌟"):
            p_item.font.size = Pt(11)
            p_item.font.bold = True
            p_item.font.color.rgb = GOLD_ACCENT
        else:
            p_item.font.size = Pt(11)
            p_item.font.color.rgb = TEXT_DARK
        p_item.space_before = Pt(2)

    # Right Column: Acting Game Drama Guide
    ag_card = s14.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.8), Inches(1.35), Inches(5.833), Inches(5.3)
    )
    ag_card.fill.solid()
    ag_card.fill.fore_color.rgb = WHITE
    ag_card.line.color.rgb = TERRACOTTA
    ag_card.line.width = Pt(2)

    tf_ag = ag_card.text_frame
    tf_ag.word_wrap = True

    p_ag_t = tf_ag.paragraphs[0]
    p_ag_t.text = "🎭 ACTIVITY • THE THANKSGIVING ACTING GAME"
    p_ag_t.font.name = "Calibri"
    p_ag_t.font.size = Pt(10)
    p_ag_t.font.bold = True
    p_ag_t.font.color.rgb = TERRACOTTA

    p_ag_sub = tf_ag.add_paragraph()
    p_ag_sub.text = "Classroom Roleplay Drama & Improvisation"
    p_ag_sub.font.name = "Georgia"
    p_ag_sub.font.size = Pt(14)
    p_ag_sub.font.bold = True
    p_ag_sub.font.color.rgb = BOOK_SPINE
    p_ag_sub.space_before = Pt(2)

    drama_steps = [
        ("Scene 1: The Heavy Heart", "Lily enters school quiet and crying. Miss Huang and classmates gather around with gentle comfort."),
        ("Scene 2: Praying to the Heavenly Doctor", "Miss Huang holds Lily's hands. They call on Lord Jesus to heal Mummy and make her surgery successful."),
        ("Scene 3: The Good News & Gratitude", "Mummy recovers! Lily thanks Miss Huang, who gently reminds her: 'Who else? To thank Lord Jesus!'"),
        ("Scene 4: Bedside Thanksgiving", "Lily kneels alone murmuring. Mummy asks what she is doing; Lily shares her prayer. Mummy is moved to tears and believes in Jesus!")
    ]
    for s_title, s_desc in drama_steps:
        p_st = tf_ag.add_paragraph()
        p_st.text = f"🎬 {s_title}"
        p_st.font.name = "Georgia"
        p_st.font.size = Pt(11.5)
        p_st.font.bold = True
        p_st.font.color.rgb = TERRACOTTA
        p_st.space_before = Pt(4)

        p_sd = tf_ag.add_paragraph()
        p_sd.text = s_desc
        p_sd.font.name = "Calibri"
        p_sd.font.size = Pt(10.5)
        p_sd.font.color.rgb = TEXT_DARK
        p_sd.space_before = Pt(1)

    # =========================================================================
    # SLIDE 15: STORYBOOK BOOKMARK & CLOSING BLESSING
    # =========================================================================
    s15 = slides[14]
    set_slide_background(s15, BG_CREAM)

    close_card = s15.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.2), Inches(0.8), Inches(10.933), Inches(5.9)
    )
    close_card.fill.solid()
    close_card.fill.fore_color.rgb = WHITE
    close_card.line.color.rgb = GOLD_ACCENT
    close_card.line.width = Pt(3)

    tf_close = close_card.text_frame
    tf_close.word_wrap = True

    p_cl_tag = tf_close.paragraphs[0]
    p_cl_tag.alignment = PP_ALIGN.CENTER
    p_cl_tag.text = "🕊️ LESSON 30 CONCLUSION & BLESSING"
    p_cl_tag.font.name = "Calibri"
    p_cl_tag.font.size = Pt(11)
    p_cl_tag.font.bold = True
    p_cl_tag.font.color.rgb = GOLD_ACCENT

    p_cl_t = tf_close.add_paragraph()
    p_cl_t.alignment = PP_ALIGN.CENTER
    p_cl_t.text = "“Lord Jesus, Give Us a Grateful Heart Like Lily”"
    p_cl_t.font.name = "Georgia"
    p_cl_t.font.size = Pt(28)
    p_cl_t.font.bold = True
    p_cl_t.font.color.rgb = BOOK_SPINE
    p_cl_t.space_before = Pt(6)

    p_cl_b = tf_close.add_paragraph()
    p_cl_b.alignment = PP_ALIGN.CENTER
    p_cl_b.text = "May the fragrance of prayer, thanksgiving, and childlike trust fill your home.\nIn everything give thanks; for this is God's will for you in Christ Jesus!"
    p_cl_b.font.name = "Georgia"
    p_cl_b.font.size = Pt(14)
    p_cl_b.font.italic = True
    p_cl_b.font.color.rgb = TEXT_DARK
    p_cl_b.space_before = Pt(8)

    # 3 Summary Medallions
    medallions = [
        ("🙏 PRAY", "Call upon Lord Jesus in every trial and need.", Inches(2.2), Inches(3.6)),
        ("💖 GIVE THANKS", "Always return to praise God in everything.", Inches(5.4), Inches(3.6)),
        ("🌟 WITNESS", "Let your grateful life bless your family and friends.", Inches(8.6), Inches(3.6)),
    ]
    for m_title, m_desc, mx, my in medallions:
        med = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, my, Inches(2.5), Inches(1.5))
        med.fill.solid()
        med.fill.fore_color.rgb = GOLD_LIGHT
        med.line.color.rgb = GOLD_ACCENT
        med.line.width = Pt(1.5)
        tf_m = med.text_frame
        tf_m.word_wrap = True
        p_mt = tf_m.paragraphs[0]
        p_mt.alignment = PP_ALIGN.CENTER
        p_mt.text = m_title
        p_mt.font.name = "Georgia"
        p_mt.font.size = Pt(13)
        p_mt.font.bold = True
        p_mt.font.color.rgb = BOOK_SPINE
        p_md = tf_m.add_paragraph()
        p_md.alignment = PP_ALIGN.CENTER
        p_md.text = m_desc
        p_md.font.name = "Calibri"
        p_md.font.size = Pt(10)
        p_md.font.color.rgb = TEXT_DARK
        p_md.space_before = Pt(4)

    # Return Navigation Buttons on Slide 15
    ret_btn1 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(5.5), Inches(2.5), Inches(0.55))
    ret_btn1.fill.solid()
    ret_btn1.fill.fore_color.rgb = BOOK_SPINE
    ret_btn1.line.color.rgb = BOOK_SPINE
    ret_btn1.click_action.target_slide = slides[0]
    tf_r1 = ret_btn1.text_frame
    p_r1 = tf_r1.paragraphs[0]
    p_r1.alignment = PP_ALIGN.CENTER
    r1 = p_r1.add_run()
    r1.text = "⏮️ Return to Cover"
    r1.font.name = "Georgia"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = WHITE
    r1.hyperlink.target_slide = slides[0]

    ret_btn2 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.4), Inches(5.5), Inches(2.5), Inches(0.55))
    ret_btn2.fill.solid()
    ret_btn2.fill.fore_color.rgb = TERRACOTTA
    ret_btn2.line.color.rgb = TERRACOTTA
    ret_btn2.click_action.target_slide = slides[1]
    tf_r2 = ret_btn2.text_frame
    p_r2 = tf_r2.paragraphs[0]
    p_r2.alignment = PP_ALIGN.CENTER
    r2 = p_r2.add_run()
    r2.text = "📖 Storybook Map"
    r2.font.name = "Georgia"
    r2.font.size = Pt(11)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    r2.hyperlink.target_slide = slides[1]

    ret_btn3 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(5.5), Inches(2.5), Inches(0.55))
    ret_btn3.fill.solid()
    ret_btn3.fill.fore_color.rgb = SAGE_GREEN
    ret_btn3.line.color.rgb = SAGE_GREEN
    ret_btn3.click_action.target_slide = slides[10]
    tf_r3 = ret_btn3.text_frame
    p_r3 = tf_r3.paragraphs[0]
    p_r3.alignment = PP_ALIGN.CENTER
    r3 = p_r3.add_run()
    r3.text = "📜 Review Verse"
    r3.font.name = "Georgia"
    r3.font.size = Pt(11)
    r3.font.bold = True
    r3.font.color.rgb = WHITE
    r3.hyperlink.target_slide = slides[10]

    # Save to scratch directory
    output_path = r"c:\Users\kevin\.gemini\antigravity\scratch\The_Grateful_Girl_Storybook_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_presentation()
