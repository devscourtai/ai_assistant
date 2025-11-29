"""
Simple test script for the AI Document Assistant API.

This script demonstrates how to:
1. Upload a document
2. Ask questions about the document
3. Use tool calling

Usage:
    python test_api.py
"""
import requests
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test if the API is running."""
    print("=" * 60)
    print("Testing API Health Check...")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        print("✅ API is healthy!")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        print("Make sure the API is running: uvicorn app.main:app --reload")
        return False


def test_upload_document(file_path: str):
    """Test document upload."""
    print("\n" + "=" * 60)
    print(f"Testing Document Upload: {file_path}")
    print("=" * 60)

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("\nTo test upload, create a sample text file:")
        print("echo 'This is a test document about our company refund policy. Customers can return products within 30 days.' > sample.txt")
        return None

    try:
        # Upload the file
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(f"{BASE_URL}/upload/", files=files)
            response.raise_for_status()

        data = response.json()
        print("✅ Document uploaded successfully!")
        print(f"   Filename: {data['filename']}")
        print(f"   Chunks created: {data['chunks_created']}")
        print(f"   Document ID: {data['document_id']}")

        return data['document_id']

    except requests.exceptions.RequestException as e:
        print(f"❌ Upload failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Error details: {e.response.text}")
        return None


def test_ask_question(question: str, use_tool_calling: bool = False):
    """Test question answering."""
    print("\n" + "=" * 60)
    print(f"Testing Question Answering")
    print("=" * 60)
    print(f"Question: {question}")
    print(f"Tool calling: {use_tool_calling}")

    try:
        # Ask a question
        payload = {
            "question": question,
            "max_results": 3,
            "use_tool_calling": use_tool_calling
        }
        response = requests.post(f"{BASE_URL}/ask/", json=payload)
        response.raise_for_status()

        data = response.json()
        print("\n✅ Answer received!")
        print(f"\nAnswer:\n{data['answer']}")

        print(f"\nRetrieved {len(data['retrieved_chunks'])} chunks:")
        for i, chunk in enumerate(data['retrieved_chunks'], 1):
            print(f"\n--- Chunk {i} ---")
            print(f"Source: {chunk['metadata'].get('source', 'Unknown')}")
            print(f"Similarity: {chunk.get('similarity_score', 'N/A')}")
            print(f"Content preview: {chunk['content'][:150]}...")

        if data.get('tool_calls'):
            print(f"\n🛠️  Tool calls made: {len(data['tool_calls'])}")
            for tool_call in data['tool_calls']:
                print(f"   - {tool_call['tool_name']} with args: {tool_call['arguments']}")
                print(f"     Result: {tool_call['result']}")

        print(f"\nTokens used: {data.get('tokens_used', 'N/A')}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Question failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Error details: {e.response.text}")
        return False


def test_stats():
    """Test stats endpoint."""
    print("\n" + "=" * 60)
    print("Testing Stats Endpoint")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/upload/stats")
        response.raise_for_status()
        data = response.json()
        print("✅ Stats retrieved!")
        print(f"   Total documents: {data.get('total_documents', 0)}")
        print(f"   Table name: {data.get('table_name', 'N/A')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Stats failed: {e}")
        return False


def create_sample_document():
    """Create a sample test document."""
    sample_file = "sample_test_document.txt"

    content = """
    Company Policies and Procedures

    Refund Policy
    Our company offers a flexible refund policy. Customers can return any product
    within 30 days of purchase for a full refund. Products must be in original
    condition with packaging intact. To initiate a refund, contact customer service
    with your order number.

    Vacation Policy
    Full-time employees accrue 15 days of paid vacation per year. After 5 years
    of service, this increases to 20 days per year. Vacation days must be approved
    by your direct manager at least 2 weeks in advance.

    Remote Work Policy
    Employees may work remotely up to 3 days per week with manager approval.
    Remote work requires a stable internet connection and a dedicated workspace.
    Employees must be available during core hours (10 AM - 3 PM) for meetings.

    Expense Reimbursement
    Business expenses must be submitted within 30 days with receipts attached.
    Approved expenses will be reimbursed within 2 weeks. Common reimbursable
    expenses include travel, meals during business trips, and office supplies.
    """

    with open(sample_file, "w") as f:
        f.write(content)

    print(f"✅ Created sample document: {sample_file}")
    return sample_file


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "AI DOCUMENT ASSISTANT - API TEST SUITE" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")

    # Test 1: Health check
    if not test_health_check():
        print("\n❌ API is not running. Please start it first.")
        print("Run: uvicorn app.main:app --reload")
        return

    # Test 2: Stats (before upload)
    test_stats()

    # Test 3: Create sample document
    print("\n" + "=" * 60)
    print("Creating Sample Document")
    print("=" * 60)
    sample_file = create_sample_document()

    # Test 4: Upload document
    doc_id = test_upload_document(sample_file)

    if not doc_id:
        print("\n⚠️  Skipping question tests due to upload failure")
        return

    # Test 5: Ask questions
    questions = [
        "What is the refund policy?",
        "How many vacation days do employees get?",
        "Can employees work remotely?",
    ]

    for question in questions:
        test_ask_question(question, use_tool_calling=False)

    # Test 6: Ask question with tool calling
    test_ask_question(
        "What is the company's vacation policy?",
        use_tool_calling=True
    )

    # Test 7: Stats (after upload)
    test_stats()

    # Summary
    print("\n" + "═" * 60)
    print("TEST SUITE COMPLETED!")
    print("═" * 60)
    print("\n✅ All tests completed. Check the results above.")
    print("\nNext steps:")
    print("1. Try uploading your own documents")
    print("2. Experiment with different questions")
    print("3. Check out the interactive API docs: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
