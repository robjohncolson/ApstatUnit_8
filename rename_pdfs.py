import os
import shutil
import re

# Define the mapping from original filenames to new names
filename_mapping = {
    # 8.2 Setting Up a Chi-Square Test for Goodness of Fit
    "TB_SettingUpaChiSquareTestforGoodnessofFitQuiz_67e1f43dceca57.67e1f43fb8c9a1.10871078.pdf": "8-2_quiz.pdf",
    "SG_SettingUpaChiSquareTestforGoodnessofFitQuiz_67e1f445cf5555.67e1f447e824b2.55787567.pdf": "8-2_quiz_answer.pdf",
    
    # 8.3 Carrying Out a Chi-Square Test for Goodness of Fit
    "TB_CarryingOutaChiSquareTestforGoodnessofFitQuiz_67e1f5020d6ed6.67e1f5038d1267.51566684.pdf": "8-3_quiz.pdf",
    "SG_CarryingOutaChiSquareTestforGoodnessofFitQuiz_67e1f5072ffff5.67e1f509757e22.50073226.pdf": "8-3_quiz_answer.pdf",
    
    # 8.4 Expected Counts in Two-Way Tables
    "TB_ExpectedCountsinTwoWayTablesQuiz_67e1f574021f00.67e1f574eb1a05.70223560.pdf": "8-4_quiz.pdf",
    "SG_ExpectedCountsinTwoWayTablesQuiz_67e1f5778e6672.67e1f5788df921.10373687.pdf": "8-4_quiz_answer.pdf",
    
    # 8.5 Setting Up a Chi-Square Test for Homogeneity or Independence
    "TB_SettingUpaChiSquareTestforHomogeneityorIndependenceQuiz_67e1f5a75a0967.67e1f5a8738183.02934607.pdf": "8-5_quiz.pdf",
    "SG_SettingUpaChiSquareTestforHomogeneityorIndependenceQuiz_67e1f5ab24fbf7.67e1f5ac4ba347.11899047.pdf": "8-5_quiz_answer.pdf",
    
    # 8.6 Carrying Out a Chi-Square Test for Homogeneity or Independence
    "TB_CarryingOutaChiSquareTestforHomogeneityorIndependenceQuiz_67e1f5ec645481.67e1f5ed962a30.95289020.pdf": "8-6_quiz.pdf",
    "SG_CarryingOutaChiSquareTestforHomogeneityorIndependenceQuiz_67e1f5f0bbd845.67e1f5f27f9e81.27088614.pdf": "8-6_quiz_answer.pdf",
    
    # Unit 8 Progress Check
    "TB_Unit8ProgressCheckFRQ_67e1f6a026b902.67e1f6a1090df0.96540970.pdf": "8-PC_FRQ_quiz.pdf",
    "SG_Unit8ProgressCheckFRQ_67e1f6a38b5305.67e1f6a49b57f7.37591501.pdf": "8-PC_FRQ_answer.pdf",
    "SG_Unit8ProgressCheckMCQPartA_67e1f670d38838.67e1f672b83cd3.01930225.pdf": "8-PC_MCQ_A_answer.pdf",
    "SG_Unit8ProgressCheckMCQPartB_67e1f6845366a0.67e1f6863edcf1.62827587.pdf": "8-PC_MCQ_B_answer.pdf"
}

def main():
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create backup directory if it doesn't exist
    backup_dir = os.path.join(current_dir, "original_pdfs_backup")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")
    
    # Track files we found and renamed
    files_found = []
    files_renamed = []
    
    # List all files in the current directory
    all_files = os.listdir(current_dir)
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF files in the current directory.")
    
    # Process each file
    for pdf_file in pdf_files:
        # Find matching file in our mapping
        # Using flexible matching to handle potential variations in filenames
        matching_file = None
        for original_name in filename_mapping.keys():
            # Create a pattern that ignores case and matches the main parts of the filename
            # This makes the matching more resilient to small differences
            pattern_parts = original_name.split('_')
            if len(pattern_parts) >= 3:
                # Match the prefix (TB/SG), the main name part, and the beginning of the hash
                prefix = pattern_parts[0]
                main_part = pattern_parts[1]
                hash_start = pattern_parts[2].split('.')[0][:10]  # First 10 chars of hash
                
                pattern = f"{prefix}.*{main_part}.*{hash_start}"
                if re.search(pattern, pdf_file, re.IGNORECASE):
                    matching_file = original_name
                    break
            
        if matching_file:
            files_found.append(pdf_file)
            new_name = filename_mapping[matching_file]
            
            # Back up the original file
            backup_path = os.path.join(backup_dir, pdf_file)
            shutil.copy2(pdf_file, backup_path)
            
            # Rename the file
            os.rename(pdf_file, new_name)
            files_renamed.append((pdf_file, new_name))
            print(f"Renamed: {pdf_file} -> {new_name}")
    
    # Print summary
    print("\nSummary:")
    print(f"Total PDF files: {len(pdf_files)}")
    print(f"Files matching our mapping: {len(files_found)}")
    print(f"Files successfully renamed: {len(files_renamed)}")
    
    if len(files_found) < len(pdf_files):
        print("\nUnmatched PDF files:")
        for pdf_file in pdf_files:
            if pdf_file not in files_found:
                print(f"  - {pdf_file}")

if __name__ == "__main__":
    print("Starting PDF renaming process...")
    main()
    print("\nRenaming process completed. Original files backed up in 'original_pdfs_backup' directory.") 