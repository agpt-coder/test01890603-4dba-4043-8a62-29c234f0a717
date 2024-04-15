import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Acknowledges the receipt of user feedback with a simple success message and optionally, the ID of the feedback record for tracking.
    """

    success: bool
    message: str
    feedback_id: str


async def submit_feedback(user_id: str, feedback: str) -> SubmitFeedbackResponse:
    """
    Allows users to submit feedback about the toolkit.

    Args:
        user_id (str): The unique identifier for the user submitting the feedback. While the user is authenticated, this field ensures we capture who is making the submission.
        feedback (str): The detailed feedback provided by the user. This text field should allow sufficient length for users to express their thoughts fully.

    Returns:
        SubmitFeedbackResponse: Acknowledges the receipt of user feedback with a simple success message and optionally, the ID of the feedback record for tracking.
    """
    feedback_entry = await prisma.models.UserFeedback.prisma().create(
        data={"userId": user_id, "feedback": feedback}
    )
    return SubmitFeedbackResponse(
        success=True,
        message="Feedback successfully submitted.",
        feedback_id=feedback_entry.id,
    )
