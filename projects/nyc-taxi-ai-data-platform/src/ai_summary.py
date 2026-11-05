"""Optional LLM narrative over aggregate metrics only."""

from __future__ import annotations

import json
import os


def summarize(daily_records: list[dict], anomalies: list[dict]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    from openai import OpenAI

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    payload = json.dumps({"daily_metrics": daily_records, "anomalies": anomalies})
    response = OpenAI(api_key=api_key).responses.create(
        model=model,
        instructions=(
            "You are a data quality analyst. Explain the supplied daily NYC taxi metrics "
            "and robust statistical outliers in 3-5 concise bullets. Distinguish observations "
            "from possible explanations. Do not invent causes or claim causal relationships."
        ),
        input=f"Analyze these aggregate metrics only:\n{payload}",
    )
    return response.output_text.strip()
