import os

def rename_files_in_directory(directory_path, new_name_prefix):
    # 디렉토리 내의 파일 목록 가져오기
    files = os.listdir(directory_path)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    # 파일 이름 변경
    for i, filename in enumerate(image_files):
        # 확장자 추출
        file_extension = os.path.splitext(filename)[1]
        # 새로운 파일 이름 생성
        new_filename = f"{new_name_prefix}_{i}{file_extension}"
        # 파일 경로 생성
        old_file_path = os.path.join(directory_path, filename)
        new_file_path = os.path.join(directory_path, new_filename)
        # 파일 이름 변경
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_filename}'")

# 예시 사용
directory_path = "C:/Temp/custom_training/train"  # 폴더 경로를 지정하세요
new_name_prefix = "object"  # 새로운 파일 이름의 접두사를 지정하세요
rename_files_in_directory(directory_path, new_name_prefix)