import os
import uuid
from git import Repo


# --------------------------------------------------
# SOURCE CODE FILE TYPES
# --------------------------------------------------

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".html",
    ".css",
    ".sql",
}


# --------------------------------------------------
# DOCUMENTATION / PROJECT INFORMATION
# --------------------------------------------------

CONTEXT_FILES = {
    "README.md",
    "README.txt",
    "requirements.txt",
}


# --------------------------------------------------
# DIRECTORIES TO IGNORE
# --------------------------------------------------

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "target",
    "bin",
    "obj",
}


# --------------------------------------------------
# CLONE REPOSITORY
# --------------------------------------------------

def clone_repository(
    github_url,
    destination="temp_repos"
):

    os.makedirs(destination, exist_ok=True)

    repo_name = github_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    # Create a unique folder every time
    unique_id = uuid.uuid4().hex[:8]

    unique_repo_name = (
        f"{repo_name}_{unique_id}"
    )

    repo_path = os.path.join(
        destination,
        unique_repo_name
    )

    print()
    print("=" * 60)
    print("CLONING GITHUB REPOSITORY")
    print("=" * 60)

    print(f"GitHub URL : {github_url}")
    print(f"Repository : {repo_name}")
    print(f"Local path : {repo_path}")

    try:

        Repo.clone_from(
            github_url,
            repo_path
        )

        print()
        print("Repository cloned successfully!")
        print("=" * 60)

        return repo_path

    except Exception as error:

        print()
        print("Repository cloning failed.")
        print(f"Error: {error}")
        print("=" * 60)

        raise Exception(
            f"Could not clone GitHub repository: {error}"
        )


# --------------------------------------------------
# EXTRACT SOURCE CODE + DOCUMENTATION
# --------------------------------------------------

def extract_code(repo_path):

    code_files = []
    context_files = []

    print()
    print("=" * 60)
    print("SCANNING REPOSITORY")
    print("=" * 60)

    for root, directories, files in os.walk(
        repo_path
    ):

        # Ignore unnecessary directories
        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for file in files:

            file_path = os.path.join(
                root,
                file
            )

            relative_path = os.path.relpath(
                file_path,
                repo_path
            )

            extension = os.path.splitext(
                file
            )[1].lower()

            # ------------------------------------------
            # SOURCE CODE
            # ------------------------------------------

            if extension in SOURCE_EXTENSIONS:

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        code = f.read()

                    code_files.append({
                        "file": relative_path,
                        "code": code
                    })

                    print(
                        f"Source code: {relative_path}"
                    )

                except Exception as error:

                    print(
                        f"Could not read {file_path}: {error}"
                    )

            # ------------------------------------------
            # README / REQUIREMENTS
            # ------------------------------------------

            elif file.lower() in {
                "readme.md",
                "readme.txt",
                "requirements.txt"
            }:

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()

                    context_files.append({
                        "file": relative_path,
                        "code": content
                    })

                    print(
                        f"Project context: {relative_path}"
                    )

                except Exception as error:

                    print(
                        f"Could not read {file_path}: {error}"
                    )

    print()
    print(
        f"Source files found: {len(code_files)}"
    )

    print(
        f"Context files found: {len(context_files)}"
    )

    print("=" * 60)

    return code_files, context_files


# --------------------------------------------------
# PREPARE EVERYTHING FOR LOCAL LLM
# --------------------------------------------------

def prepare_code_for_llm(
    code_files,
    context_files=None,
    max_characters=40000
):

    if context_files is None:
        context_files = []

    combined_code = ""

    print()
    print("=" * 60)
    print("PREPARING REPOSITORY FOR LOCAL LLM")
    print("=" * 60)

    # ------------------------------------------
    # ADD PROJECT CONTEXT FIRST
    # ------------------------------------------

    for item in context_files:

        file_section = (
            "\n\n"
            "========================================\n"
            f"PROJECT CONTEXT FILE: {item['file']}\n"
            "========================================\n\n"
            f"{item['code']}"
        )

        if (
            len(combined_code)
            + len(file_section)
            > max_characters
        ):

            print(
                "Character limit reached while "
                "adding context files."
            )

            break

        combined_code += file_section

        print(
            f"Added context: {item['file']}"
        )

    # ------------------------------------------
    # ADD SOURCE CODE
    # ------------------------------------------

    for item in code_files:

        file_section = (
            "\n\n"
            "========================================\n"
            f"SOURCE CODE FILE: {item['file']}\n"
            "========================================\n\n"
            f"{item['code']}"
        )

        if (
            len(combined_code)
            + len(file_section)
            > max_characters
        ):

            print(
                "Character limit reached while "
                "adding source files."
            )

            break

        combined_code += file_section

        print(
            f"Added source: {item['file']}"
        )

    print()
    print(
        f"Characters sent to LLM: "
        f"{len(combined_code)}"
    )

    print("=" * 60)

    return combined_code