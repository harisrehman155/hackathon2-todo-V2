from pathlib import Path

import yaml

from src.main import create_app


def test_openapi_has_required_task_paths():
    app = create_app()
    spec = app.openapi()

    paths = set(spec['paths'].keys())
    assert '/tasks' in paths
    assert '/tasks/{task_id}' in paths
    assert '/tasks/{task_id}/toggle-complete' in paths


def test_openapi_path_alignment_with_contract_file():
    contract_file = Path(__file__).resolve().parents[3] / 'specs/001-phase2-kickoff/contracts/todo-api.openapi.yaml'
    contract = yaml.safe_load(contract_file.read_text(encoding='utf-8'))

    app = create_app()
    app_paths = set(app.openapi()['paths'].keys())

    # Contract currently uses camelCase path parameter name; runtime uses snake_case.
    normalized_contract_paths = {
        p.replace('{taskId}', '{task_id}') for p in contract['paths'].keys()
    }
    assert normalized_contract_paths.issubset(app_paths)
