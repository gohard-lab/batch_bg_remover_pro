import os
import time
import csv
from pathlib import Path
from rembg import remove, new_session
from PIL import Image, ImageColor

def process_images(input_paths, output_folder, settings, progress_callback=None):
    """
    settings: {
        'bg_color': 'transparent' 또는 '#ffffff',
        'canvas_size': (width, height) 또는 None,
        'mirror_structure': bool
    }
    """
    output_root = Path(output_folder)
    review_folder = output_root / "_review_needed"
    output_root.mkdir(parents=True, exist_ok=True)

    valid_extensions = {'.jpg', '.jpeg', '.png'}
    tasks = []

    # 1. 작업 큐 생성 (폴더 구조 분석 포함)
    for path_str in input_paths:
        p = Path(path_str)
        if p.is_dir():
            for root, dirs, files in os.walk(p):
                for file in files:
                    if Path(file).suffix.lower() in valid_extensions:
                        full_path = Path(root) / file
                        # 상대 경로 계산 (폴더 미러링용)
                        rel_path = full_path.relative_to(p.parent if settings['mirror_structure'] else root)
                        tasks.append((full_path, rel_path))
        elif p.is_file() and p.suffix.lower() in valid_extensions:
            tasks.append((p, Path(p.name)))

    if not tasks: return False

    session = new_session()
    stats = []
    start_time = time.time()

    for idx, (img_path, rel_path) in enumerate(tasks, start=1):
        item_start = time.time()
        success = False
        error_msg = ""
        
        try:
            # 출력 경로 설정 (미러링 반영)
            final_output_path = output_root / rel_path
            final_output_path = final_output_path.with_name(f"{img_path.stem}_rmbg.png")
            final_output_path.parent.mkdir(parents=True, exist_ok=True)

            # 이미지 처리
            input_image = Image.open(img_path).convert("RGBA")
            # rembg 실행
            out_alpha = remove(input_image, session=session)

            # 배경색 및 캔버스 적용
            if settings['bg_color'] != 'transparent':
                bg = Image.new("RGBA", out_alpha.size, ImageColor.getrgb(settings['bg_color']))
                out_alpha = Image.alpha_composite(bg, out_alpha)

            if settings.get('canvas_size'):
                # 비율 유지하며 캔버스 중앙에 배치
                new_canvas = Image.new("RGBA", settings['canvas_size'], (0,0,0,0) if settings['bg_color']=='transparent' else ImageColor.getrgb(settings['bg_color']))
                out_alpha.thumbnail(settings['canvas_size'], Image.Resampling.LANCZOS)
                offset = ((settings['canvas_size'][0] - out_alpha.size[0]) // 2, (settings['canvas_size'][1] - out_alpha.size[1]) // 2)
                new_canvas.paste(out_alpha, offset)
                out_alpha = new_canvas

            out_alpha.convert("RGB" if settings['bg_color'] != 'transparent' else "RGBA").save(final_output_path)
            success = True
            
        except Exception as e:
            error_msg = str(e)
            # 실패한 파일은 따로 복사 (리뷰용)
            # Isolate failed images to a separate folder for review
            review_folder.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(img_path, review_folder / img_path.name)
        
        item_duration = time.time() - item_start
        stats.append([img_path.name, "Success" if success else "Failed", f"{item_duration:.2f}s", error_msg])

        if progress_callback:
            progress_callback(idx, len(tasks))

    # 2. 통계 CSV 저장
    with open(output_root / "process_stats.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Status", "Duration", "Error Message"])
        writer.writerows(stats)
        writer.writerow([])
        writer.writerow(["Total Items", len(tasks)])
        writer.writerow(["Total Time", f"{time.time() - start_time:.2f}s"])

    return True