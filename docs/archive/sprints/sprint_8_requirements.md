# Sprint 8 Requirements — Explanation Layer

## Objective
Enable users to understand the reasoning behind signals, allocation, and confidence in the dashboard.

## Functional requirements
1. Each trade must include a clear explanation of its quality tier
2. Funded trades must include a reason for being selected
3. Unfunded trades must include a clear reason for exclusion
4. Confidence labels must be explained in plain language
5. Warnings must include explanation text (not just labels)
6. Explanations must map to real system logic

## Non-functional requirements
- explanations must be concise
- language must be simple and clear
- no exaggerated claims or guarantees
- UI must remain readable

## Acceptance criteria
- user can explain why a trade was funded or not funded
- user can explain what confidence means
- user can understand warnings without technical knowledge

## Additional functional requirements
7. The system must explain why funded trades were selected ahead of other eligible trades where current fields allow it.
8. The system must explain when a trade was eligible but not funded because it ranked outside funded positions.
9. Selection-order explanations must remain grounded in actual allocation inputs such as quality tier, confidence, and portfolio limits.
