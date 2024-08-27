from bson import ObjectId

def question_serializer(question) -> dict:
    return {
        "id": str(question["_id"]),
        "category": question["category"],
        "url": question["url"],
        "question": question["question"],
        "img_url": question.get("img_url"),
        "img_path": question.get("img_path"),
        "choices": question["choices"],
        "answer": question["answer"],
        "comment": question.get("comment", [])
    }
