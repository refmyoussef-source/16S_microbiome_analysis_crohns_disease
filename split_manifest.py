import os

# --- الإعدادات ---
INPUT_MANIFEST = 'data/manifest.final_PRO.tsv'
OUTPUT_DIR = 'data/manifest_batches'
BATCH_SIZE = 10
# ------------------

# تأكد أن مجلد المخرجات موجود
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    with open(INPUT_MANIFEST, 'r') as f_in:
        # قرا الـ Header
        header = f_in.readline().strip()

        # قرا السطور ديال البيانات لي باقين
        lines = f_in.readlines()

    print(f"لقينا {len(lines)} عينة. غانقسموهم لدفعات ديال {BATCH_SIZE}...")

    batch_num = 1
    for i in range(0, len(lines), BATCH_SIZE):
        # خود 10 سطور
        batch_lines = lines[i : i + BATCH_SIZE]

        # صايب السمية ديال الملف
        batch_filename = os.path.join(OUTPUT_DIR, f'batch_{batch_num:02d}.tsv')

        with open(batch_filename, 'w') as f_out:
            # كتب الـ Header هو الأول
            f_out.write(header + '\n')
            # كتب الـ 10 سطور
            f_out.writelines(batch_lines)

        print(f"صايبنا الملف: {batch_filename} (فيه {len(batch_lines)} عينة)")
        batch_num += 1

    print(f"\nتم بنجااح! قسمنا كلشي لـ {batch_num - 1} ملف في المجلد: {OUTPUT_DIR}")

except FileNotFoundError:
    print(f"Error: ما لقيتش الملف الرئيسي: {INPUT_MANIFEST}")
    print("واش نتا متأكد أنك خدمتي السكريبت ديال 'create_manifest.py' لول؟")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
