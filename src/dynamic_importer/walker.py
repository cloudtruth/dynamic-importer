from __future__ import annotations

import os
from typing import Dict
from typing import List

import click
from dynamic_importer.processors import get_supported_formats


# mime types think .env and tf files are plain text
EXTENSIONS_TO_FILE_TYPES = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".env": "dotenv",
    ".tf": "tf",
    ".tfvars": "tfvars",
}


def walk_files(
    root: str, files: str, file_types: List[str]
) -> Dict[str, Dict[str, str]]:
    walked_files = {}
    last_project = None
    for file in files:
        file_path = f"{root}/{file}"
        name, file_extension = os.path.splitext(file)
        if name.startswith(".env"):
            file_extension = ".env"
        if data_type := EXTENSIONS_TO_FILE_TYPES.get(file_extension):
            confirmed_type = click.prompt(
                f"File type {data_type} detected for {file_path}. Is this correct?",
                type=click.Choice(get_supported_formats(), case_sensitive=False),
                default=data_type,
            )
            if confirmed_type not in file_types:
                click.echo(
                    f"Skipping {confirmed_type} file {file_path} as "
                    f"it is not included in the supplied file types: {', '.join(file_types)}"
                )
                continue
            project = click.prompt(
                f"Enter the CloudTruth project to import {file_path} into",
                default=last_project,
            )
            if project:
                last_project = project
            env = click.prompt(
                f"Enter the CloudTruth environment to import {file_path} into",
            )
            walked_files[file_path] = {
                "type": confirmed_type,
                "path": file_path,
                "project": project,
                "environment": env,
            }

    return walked_files
