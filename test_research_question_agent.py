from slrresearch.agents.research_question_agent import (
    ResearchQuestionAgent,
)


def main():
    agent = ResearchQuestionAgent()

    response = agent.run(
        topic="Agentic AI in Education",
        objective=(
            "Analyze the applications, architectures, roles, "
            "benefits and challenges of agentic AI in education."
        ),
        context=(
            "Focus on scientific literature and "
            "educational environments."
        ),
    )

    print("\n========== AGENT RESULT ==========")
    print(f"Status: {response['status']}")
    print(f"Repair attempts: {response['repair_attempts']}")

    if response.get("errors"):
        print("\nErrors:")
        for error in response["errors"]:
            print(f"- {error}")

    if response.get("repair_error"):
        print(f"\nRepair error: {response['repair_error']}")

    result = response["result"]

    print(f"\nTopic: {result.topic}")
    print(f"Objective: {result.objective}")

    print("\nResearch Questions:")
    for rq in result.research_questions:
        print(f"\n{rq.id}: {rq.question}")
        print(f"Rationale: {rq.rationale}")

    print("\n==================================")


if __name__ == "__main__":
    main()