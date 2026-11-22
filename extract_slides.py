import os
import sys
import json
import re
import shutil
import subprocess
from pathlib import Path
from PIL import Image

try:
    import pypdfium2 as pdfium
except ImportError:
    print("Error: pypdfium2 is required. Run 'python -m pip install pypdfium2'", flush=True)
    sys.exit(1)

SOURCE_ROOT = r"C:\Users\kevin\Studies\SFIT\5th Sem"
PROJECT_ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = PROJECT_ROOT / "public"
SLIDES_DIR = PUBLIC_DIR / "slides"
DOCS_DIR = PUBLIC_DIR / "docs"
DATA_DIR = PUBLIC_DIR / "data"
SRC_DATA_DIR = PROJECT_ROOT / "src" / "data"

SUBJECT_METADATA = {
    "ADMT": {
        "name": "ADMT",
        "fullName": "Advanced Database Management Technology",
        "description": "Distributed databases, query optimization, concurrency control, NoSQL & Big Data",
        "color": "#6366f1",
        "gradient": "from-indigo-500 to-purple-600",
        "icon": "Database"
    },
    "CNS": {
        "name": "CNS",
        "fullName": "Cryptography & Network Security",
        "description": "Classical ciphers, public-key crypto, RSA, ECC, network protocols & firewalls",
        "color": "#0ea5e9",
        "gradient": "from-sky-500 to-blue-600",
        "icon": "ShieldCheck"
    },
    "IDS": {
        "name": "IDS",
        "fullName": "Information & Data Security / Data Science",
        "description": "Lab experiments, k-means clustering, intrusion detection, analytics & security",
        "color": "#10b981",
        "gradient": "from-emerald-500 to-teal-600",
        "icon": "Activity"
    },
    "IoT": {
        "name": "IoT",
        "fullName": "Internet of Things",
        "description": "Smart architectures, sensor networks, wireless protocols & embedded systems",
        "color": "#f59e0b",
        "gradient": "from-amber-500 to-orange-600",
        "icon": "Cpu"
    },
    "SBIS": {
        "name": "SBIS",
        "fullName": "Software & Business Information Systems",
        "description": "Enterprise architectures, digital governance, case studies & system design",
        "color": "#ec4899",
        "gradient": "from-pink-500 to-rose-600",
        "icon": "Layers"
    },
    "WEB X.0": {
        "name": "Web X.0",
        "fullName": "Web X.0 (Web Technologies & Frameworks)",
        "description": "Modern frontend frameworks (React, Angular), backend architectures, REST & fullstack web",
        "color": "#06b6d4",
        "gradient": "from-cyan-500 to-blue-600",
        "icon": "Globe"
    }
}

def sanitize_id(s):
    s = re.sub(r'[^a-zA-Z0-9_\-]+', '_', s)
    return s.strip('_').lower()

def convert_pdf_to_slides(pdf_path, output_dir, force=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_file = output_dir / "meta.json"
    file_mtime = os.path.getmtime(pdf_path)

    if not force and meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if cached.get("mtime") == file_mtime and cached.get("slides"):
                    print(f"  [Cache hit] {pdf_path.name} ({len(cached['slides'])} slides)", flush=True)
                    return cached["slides"], cached.get("aspectRatio", 1.33)
        except Exception:
            pass

    print(f"  [Processing PDF] {pdf_path.name}...", flush=True)
    try:
        doc = pdfium.PdfDocument(str(pdf_path))
    except Exception as e:
        print(f"    Failed to open PDF {pdf_path}: {e}", flush=True)
        return [], 1.33

    slides_info = []
    num_pages = len(doc)
    avg_aspect = 1.33

    for i in range(num_pages):
        page = doc[i]
        slide_num = i + 1
        slide_filename = f"slide_{slide_num:03d}.webp"
        thumb_filename = f"thumb_{slide_num:03d}.webp"
        slide_img_path = output_dir / slide_filename
        thumb_img_path = output_dir / thumb_filename

        text_content = ""
        try:
            textpage = page.get_textpage()
            text_content = textpage.get_text_range().strip()
        except Exception:
            pass

        try:
            pil_img = page.render(scale=2.0).to_pil()
            w, h = pil_img.size
            if h > 0:
                avg_aspect = round(w / h, 2)
            
            pil_img.save(slide_img_path, "WEBP", quality=88)

            thumb_w = 360
            thumb_h = int(h * (thumb_w / w)) if w > 0 else 240
            thumb_img = pil_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            thumb_img.save(thumb_img_path, "WEBP", quality=80)
        except Exception as e:
            print(f"    Error rendering page {slide_num}: {e}", flush=True)
            continue

        slides_info.append({
            "index": slide_num,
            "image": f"/slides/{output_dir.name}/{slide_filename}",
            "thumb": f"/slides/{output_dir.name}/{thumb_filename}",
            "text": text_content,
            "width": w,
            "height": h
        })

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({
            "mtime": file_mtime,
            "aspectRatio": avg_aspect,
            "slides": slides_info
        }, f, indent=2)

    print(f"    Extracted {len(slides_info)} slides from PDF.", flush=True)
    return slides_info, avg_aspect

def convert_ppt_to_slides(ppt_path, output_dir, force=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_file = output_dir / "meta.json"
    file_mtime = os.path.getmtime(ppt_path)
    
    if not force and meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if cached.get("mtime") == file_mtime and cached.get("slides"):
                    print(f"  [Cache hit] {ppt_path.name} ({len(cached['slides'])} slides)", flush=True)
                    return cached["slides"], cached.get("aspectRatio", 1.33)
        except Exception:
            pass

    print(f"  [Processing PPT via COM] {ppt_path.name}...", flush=True)
    temp_png_dir = output_dir / "_temp_png"
    if temp_png_dir.exists():
        shutil.rmtree(temp_png_dir)
    temp_png_dir.mkdir(parents=True, exist_ok=True)

    ps_cmd = f"""
$ErrorActionPreference = 'Stop'
$pptApp = New-Object -ComObject PowerPoint.Application
try {{
    $pres = $pptApp.Presentations.Open('{str(ppt_path)}', 1, 0, 0)
    $pres.SaveAs('{str(temp_png_dir)}', 18)
    
    for ($i = 1; $i -le $pres.Slides.Count; $i++) {{
        $slide = $pres.Slides.Item($i)
        $t = ""
        foreach ($sh in $slide.Shapes) {{
            if ($sh.HasTextFrame -and $sh.TextFrame.HasText) {{
                $t += " " + $sh.TextFrame.TextRange.Text
            }}
        }}
        [System.IO.File]::WriteAllText("$('{str(temp_png_dir)}')\\Slide$i.txt", $t, [System.Text.Encoding]::UTF8)
    }}

    $pres.Close()
}} catch {{
    Write-Error $_.Exception.Message
    exit 1
}} finally {{
    $pptApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pptApp) | Out-Null
}}
"""
    ps_file = output_dir / "_export.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_cmd)

    try:
        proc = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)],
            capture_output=True,
            text=True,
            timeout=240
        )
        if proc.returncode != 0:
            print(f"    PowerPoint export error: {proc.stderr}", flush=True)
            return [], 1.33
    except Exception as e:
        print(f"    PowerPoint export failed: {e}", flush=True)
        return [], 1.33
    finally:
        if ps_file.exists():
            ps_file.unlink()

    def get_slide_num(p):
        m = re.search(r'Slide(\d+)', p.stem, re.IGNORECASE)
        return int(m.group(1)) if m else 0

    # Deduplicate strictly by slide number so duplicate files (e.g. Slide1.PNG and slide_1.png) never double slide counts
    slide_dict = {}
    for p in temp_png_dir.glob("Slide*.*"):
        if p.suffix.lower() == ".png":
            s_num = get_slide_num(p)
            if s_num > 0 and s_num not in slide_dict:
                slide_dict[s_num] = p

    png_files = [slide_dict[k] for k in sorted(slide_dict.keys())]

    # Clean up any previously extracted webp files in output_dir so no orphaned/duplicated slides remain
    for old_webp in output_dir.glob("*.webp"):
        try:
            old_webp.unlink()
        except Exception:
            pass

    slides_info = []
    avg_aspect = 1.33

    for idx, png_p in enumerate(png_files):
        orig_slide_num = get_slide_num(png_p)
        slide_num = idx + 1
        slide_filename = f"slide_{slide_num:03d}.webp"
        thumb_filename = f"thumb_{slide_num:03d}.webp"
        slide_img_path = output_dir / slide_filename
        thumb_img_path = output_dir / thumb_filename

        text_file = temp_png_dir / f"Slide{orig_slide_num}.txt"
        text_content = ""
        if text_file.exists():
            try:
                with open(text_file, "r", encoding="utf-8", errors="ignore") as tf:
                    text_content = tf.read().strip()
            except Exception:
                pass

        if not text_content:
            text_content = f"{ppt_path.stem} Slide {slide_num}"

        try:
            with Image.open(png_p) as pil_img:
                pil_img = pil_img.convert("RGB")
                w, h = pil_img.size
                if h > 0:
                    avg_aspect = round(w / h, 2)
                pil_img.save(slide_img_path, "WEBP", quality=88)

                thumb_w = 360
                thumb_h = int(h * (thumb_w / w)) if w > 0 else 240
                thumb_img = pil_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                thumb_img.save(thumb_img_path, "WEBP", quality=80)

            slides_info.append({
                "index": slide_num,
                "image": f"/slides/{output_dir.name}/{slide_filename}",
                "thumb": f"/slides/{output_dir.name}/{thumb_filename}",
                "text": text_content,
                "width": w,
                "height": h
            })
        except Exception as e:
            print(f"    Error converting slide PNG {png_p.name}: {e}", flush=True)

    if temp_png_dir.exists():
        shutil.rmtree(temp_png_dir)

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({
            "mtime": file_mtime,
            "aspectRatio": avg_aspect,
            "slides": slides_info
        }, f, indent=2)

    print(f"    Extracted {len(slides_info)} slides from PPT.", flush=True)
    return slides_info, avg_aspect

def convert_single_image_to_slide(img_path, output_dir, force=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_file = output_dir / "meta.json"
    file_mtime = os.path.getmtime(img_path)

    if not force and meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if cached.get("mtime") == file_mtime and cached.get("slides"):
                    return cached["slides"], cached.get("aspectRatio", 1.33)
        except Exception:
            pass

    slide_filename = "slide_001.webp"
    thumb_filename = "thumb_001.webp"
    slide_img_path = output_dir / slide_filename
    thumb_img_path = output_dir / thumb_filename

    with Image.open(img_path) as pil_img:
        pil_img = pil_img.convert("RGB")
        w, h = pil_img.size
        # WebP hard limit is 16,383 pixels in width and height
        if max(w, h) > 16000:
            scale = 16000 / max(w, h)
            w, h = int(w * scale), int(h * scale)
            pil_img = pil_img.resize((w, h), Image.Resampling.LANCZOS)
            
        avg_aspect = round(w / h, 2) if h > 0 else 1.33
        pil_img.save(slide_img_path, "WEBP", quality=90)
        
        thumb_w = 360
        thumb_h = int(h * (thumb_w / w)) if w > 0 else 240
        thumb_img = pil_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        thumb_img.save(thumb_img_path, "WEBP", quality=80)

    slides_info = [{
        "index": 1,
        "image": f"/slides/{output_dir.name}/{slide_filename}",
        "thumb": f"/slides/{output_dir.name}/{thumb_filename}",
        "text": img_path.stem.replace("_", " "),
        "width": w,
        "height": h
    }]

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({"mtime": file_mtime, "aspectRatio": avg_aspect, "slides": slides_info}, f, indent=2)

    return slides_info, avg_aspect

def ensure_interactive_docs(decks):
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ppts_to_convert = []

    for d in decks:
        deck_id = d["id"]
        pdf_dest = DOCS_DIR / f"{deck_id}.pdf"
        src = Path(d["originalFile"])
        d["pdfUrl"] = f"/docs/{deck_id}.pdf"

        if pdf_dest.exists() and pdf_dest.stat().st_size > 0:
            continue

        if d["fileType"] == "PDF":
            shutil.copy2(src, pdf_dest)
        elif d["fileType"] == "PNG":
            with Image.open(src) as img:
                img = img.convert("RGB")
                if max(img.size) > 16000:
                    scale = 16000 / max(img.size)
                    img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)), Image.Resampling.LANCZOS)
                img.save(pdf_dest, "PDF", resolution=100.0)
        elif d["fileType"] in ["PPT", "PPTX"]:
            ppts_to_convert.append((str(src), str(pdf_dest)))

    if ppts_to_convert:
        ps_script = [
            "$ErrorActionPreference = 'Stop'",
            "$ppt = New-Object -ComObject PowerPoint.Application",
            "try {"
        ]
        for src, dest in ppts_to_convert:
            ps_script.append(f"    $p = $ppt.Presentations.Open('{src}', 1, 0, 0)")
            ps_script.append(f"    $p.SaveAs('{dest}', 32)")
            ps_script.append(f"    $p.Close()")
        ps_script.extend([
            "} finally {",
            "    $ppt.Quit()",
            "    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null",
            "}"
        ])
        tmp_ps = PROJECT_ROOT / "_conv_tmp.ps1"
        with open(tmp_ps, "w", encoding="utf-8") as pf:
            pf.write("\n".join(ps_script))
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(tmp_ps)], capture_output=True)
        if tmp_ps.exists():
            tmp_ps.unlink()

def main():
    force = "--force" in sys.argv
    target_subject = None
    for arg_idx, arg in enumerate(sys.argv):
        if arg in ["--subject", "-s"] and arg_idx + 1 < len(sys.argv):
            target_subject = sys.argv[arg_idx + 1].strip().upper()

    print(f"=== SFIT 5th Sem Slide Deck Extractor ===", flush=True)
    if target_subject:
        print(f"Filter: Only processing subject '{target_subject}'", flush=True)
    print(f"Source Directory: {SOURCE_ROOT}", flush=True)
    print(f"Target Public Directory: {PUBLIC_DIR}", flush=True)

    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)

    source_path = Path(SOURCE_ROOT)
    if not source_path.exists():
        print(f"Error: Source directory {source_path} does not exist!", flush=True)
        sys.exit(1)

    def norm_key(k):
        return re.sub(r'[^A-Z0-9]', '', str(k).upper().replace('O', '0'))

    subjects = {}
    norm_target = norm_key(target_subject) if target_subject else None
    
    # If targeting a specific subject, load existing other subjects from manifest so they are preserved
    manifest_json_path = DATA_DIR / "manifest.json"
    if norm_target and manifest_json_path.exists():
        try:
            with open(manifest_json_path, "r", encoding="utf-8") as f:
                existing_manifest = json.load(f)
                for s in existing_manifest.get("subjects", []):
                    if norm_key(s.get("code", "")) != norm_target:
                        subjects[s["code"]] = s
        except Exception as e:
            print(f"Note: Could not preload existing manifest: {e}", flush=True)

    all_decks = []
    total_decks = 0
    total_slides = 0

    scan_dir = source_path
    if norm_target:
        for child in source_path.iterdir():
            if child.is_dir() and norm_key(child.name) == norm_target:
                scan_dir = child
                break

    for root, dirs, files in os.walk(scan_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in [".pdf", ".ppt", ".pptx", ".png"]:
                continue

            full_file_path = Path(root) / f
            rel_path = full_file_path.relative_to(source_path)
            parts = rel_path.parts

            subject_code = parts[0].upper() if len(parts) > 0 else "GENERAL"
            if norm_target and norm_key(subject_code) != norm_target:
                continue
            sub_info = SUBJECT_METADATA.get(subject_code) or SUBJECT_METADATA.get(subject_code.replace('O', '0')) or {
                "name": subject_code,
                "fullName": subject_code,
                "description": "Course materials",
                "color": "#06b6d4",
                "gradient": "from-cyan-500 to-blue-600",
                "icon": "BookOpen"
            }

            if len(parts) > 2:
                category = " / ".join(parts[1:-1])
            elif len(parts) == 2:
                category = "General"
            else:
                category = "Overview"

            deck_title = full_file_path.stem.replace("_", " ").strip()
            deck_id = sanitize_id(f"{subject_code}_{rel_path.as_posix()}")
            output_dir = SLIDES_DIR / deck_id

            slides = []
            aspect_ratio = 1.33

            try:
                if ext == ".pdf":
                    slides, aspect_ratio = convert_pdf_to_slides(full_file_path, output_dir, force=force)
                elif ext in [".ppt", ".pptx"]:
                    slides, aspect_ratio = convert_ppt_to_slides(full_file_path, output_dir, force=force)
                elif ext == ".png":
                    slides, aspect_ratio = convert_single_image_to_slide(full_file_path, output_dir, force=force)
            except Exception as e:
                print(f"  [ERROR] Processing {full_file_path}: {e}", flush=True)

            if not slides:
                continue

            total_decks += 1
            total_slides += len(slides)

            deck_obj = {
                "id": deck_id,
                "title": deck_title,
                "subject": subject_code,
                "category": category,
                "originalFile": str(full_file_path),
                "fileType": ext.lstrip(".").upper(),
                "fileSize": os.path.getsize(full_file_path),
                "slideCount": len(slides),
                "aspectRatio": aspect_ratio,
                "pdfUrl": f"/docs/{deck_id}.pdf",
                "slides": slides
            }

            all_decks.append(deck_obj)

            if subject_code not in subjects:
                subjects[subject_code] = {
                    "id": subject_code.lower(),
                    "code": subject_code,
                    "name": sub_info["fullName"],
                    "shortName": sub_info["name"],
                    "description": sub_info["description"],
                    "color": sub_info["color"],
                    "gradient": sub_info["gradient"],
                    "icon": sub_info["icon"],
                    "decks": []
                }

            subjects[subject_code]["decks"].append(deck_obj)

    ensure_interactive_docs(all_decks)

    for s_code in subjects:
        subjects[s_code]["decks"].sort(key=lambda d: (d["category"], d["title"]))

    calculated_total_decks = sum(len(s.get("decks", [])) for s in subjects.values())
    calculated_total_slides = sum(len(d.get("slides", [])) for s in subjects.values() for d in s.get("decks", []))

    manifest = {
        "generatedAt": os.path.getmtime(source_path),
        "sourceRoot": str(source_path),
        "totalDecks": calculated_total_decks,
        "totalSlides": calculated_total_slides,
        "subjects": list(subjects.values())
    }

    manifest_json_path = DATA_DIR / "manifest.json"
    with open(manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    src_manifest_json_path = SRC_DATA_DIR / "manifest.json"
    with open(src_manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n==========================================", flush=True)
    print(f"SUCCESS: Extracted {total_decks} decks with {total_slides} total slides & interactive documents!", flush=True)
    print(f"Manifest written to: {manifest_json_path}", flush=True)
    print("==========================================", flush=True)

if __name__ == "__main__":
    main()
