from __future__ import annotations

from re import sub
from typing import Dict
from typing import Optional

from dotenv import dotenv_values  # type: ignore[import-not-found]
from dotenv.main import DotEnv  # type: ignore[import-not-found]

from dynamic_importer.processors import BaseProcessor


class DotEnvProcessor(BaseProcessor):
    def __init__(self, default_values: str, file_path: str) -> None:
        super().__init__(default_values, file_path)
        self.raw_data = dotenv_values(file_path)

    def encode_template_references(
        self, template: Dict, config_data: Optional[Dict]
    ) -> str:
        de_template = DotEnv("")
        de_template.from_dict(template)
        template_body = de_template.dumps()
        if config_data:
            for _, data in config_data.items():
                if data["type"] != "string":
                    reference = rf"(\\{{\\{{\s+cloudtruth.parameters.{data['param_name']}\\s+\\}}\\}})"
                    template_body = sub(reference, r"\1", template_body)

        return template_body
