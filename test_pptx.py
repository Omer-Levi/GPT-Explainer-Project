import pytest
import os
import asyncio
from main import main

PATH = "./test.pptx"

@pytest.mark.asyncio
async def test_pptx_to_json():
    pptx_path = PATH
    json_path = pptx_path.replace('.pptx', '.json')

    # Ensure the JSON file does not exist before the test
    if os.path.exists(json_path):
        os.remove(json_path)

    await main()

    # Check if the JSON file exists
    assert os.path.exists(json_path), f"JSON file {json_path} was not created."

    # Clean up the generated JSON file
    if os.path.exists(json_path):
        os.remove(json_path)
