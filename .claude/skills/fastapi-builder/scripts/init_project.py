#!/usr/bin/env python3
"""
Initialize a new FastAPI project from a template.

Usage:
    python init_project.py <project-name> --template <minimal|standard|auth|production>
"""

import shutil
import sys
from pathlib import Path
import argparse


def init_project(project_name: str, template: str, output_dir: str = "."):
    """Initialize a new FastAPI project from a template."""
    # Get the script's directory
    script_dir = Path(__file__).parent.parent
    template_dir = script_dir / "assets" / "templates" / template

    if not template_dir.exists():
        print(f"❌ Error: Template '{template}' not found")
        print(f"Available templates: minimal, standard, auth, production")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir) / project_name
    if output_path.exists():
        print(f"❌ Error: Directory '{output_path}' already exists")
        sys.exit(1)

    # Copy template
    print(f"📦 Creating FastAPI project: {project_name}")
    print(f"📋 Template: {template}")
    shutil.copytree(template_dir, output_path)

    print(f"\n✅ Project created successfully at: {output_path}")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  python -m venv venv")
    print(f"  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print(f"  pip install -r requirements.txt")

    if template != "minimal":
        print(f"  cp .env.example .env  # Configure your environment")

    if template == "production":
        print(f"\nOr use Docker:")
        print(f"  docker-compose up --build")
        print(f"\nRun tests:")
        print(f"  pytest")

    print(f"\nStart the server:")
    print(f"  fastapi dev main.py")
    print(f"\nAPI docs will be at: http://127.0.0.1:8000/docs")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new FastAPI project")
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument(
        "--template",
        "-t",
        choices=["minimal", "standard", "auth", "production"],
        default="minimal",
        help="Template to use (default: minimal)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()
    init_project(args.project_name, args.template, args.output)


if __name__ == "__main__":
    main()
