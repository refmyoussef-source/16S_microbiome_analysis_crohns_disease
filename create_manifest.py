import os
import glob
import sys

# --- الإعدادات ---
# المسار لي فيه البيانات
fastq_dir = 'data/raw_fastq'

# المسار ديال المشروع (لي غانبدلوه بـ /data)
# (تأكد أن هاد المسار صحيح 100%)
project_root_path = '/home/refm_youssef/16S_microbiome_analysis_crohns_disease'

# الملف الجديد لي غانصايبو
output_manifest = 'data/manifest.final_PRO.tsv'
# ------------------

# تأكد أن المسار ديال المشروع صحيح
if not os.path.exists(project_root_path):
    print(f"Error: المسار ديال المشروع غالط: {project_root_path}")
    sys.exit(1)

# قلب على جميع ملفات R1
forward_reads = sorted(glob.glob(os.path.join(fastq_dir, '*_1.fastq')))

print(f"لقينا {len(forward_reads)} ملف ديال R1. دابا غانقلبو على R2...")

total_written = 0
with open(output_manifest, 'w') as f:
    # كتابة الـ Header (بصيغة TSV)
    f.write('sample-id\tforward-absolute-filepath\treverse-absolute-filepath\n')
    
    for r1_path in forward_reads:
        # صايب المسار ديال R2 لي كنتسناو
        r2_path = r1_path.replace('_1.fastq', '_2.fastq')
        
        # تأكد أن R2 فعلاً كاين
        if os.path.exists(r2_path):
            # إلى كاين، جيب السمية ديال العينة
            sample_id = os.path.basename(r1_path).replace('_1.fastq', '')
            
            # جيب المسارات المطلقة (Absolute paths) ديال الـ VM
            r1_abs_vm = os.path.abspath(r1_path)
            r2_abs_vm = os.path.abspath(r2_path)
            
            # --- ترجمة المسارات لـ Docker ---
            r1_abs_docker = r1_abs_vm.replace(project_root_path, '/data')
            r2_abs_docker = r2_abs_vm.replace(project_root_path, '/data')
            
            # أكتب السطر في الملف
            f.write(f'{sample_id}\t{r1_abs_docker}\t{r2_abs_docker}\n')
            total_written += 1
        else:
            # إلى مالقيناش R2، علمنا
            print(f"!!! تنبيه: تخطينا العينة {os.path.basename(r1_path)} - الملف R2 ديالها ناقص.")

print(f"\nتم بنجاح!")
print(f"كتبنا {total_written} عينة (sample) في الملف الجديد: {output_manifest}")

